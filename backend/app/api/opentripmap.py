"""
This script contains the logic for interacting with the OpenTripMap API using FastAPI.
(https://rapidapi.com/opentripmap/api/places1/playground/apiendpoint_c92ce138-db30-4713-9058-752835430bc7)
It can be seen as an extension of the events.py file.

Author: Ruben Vandamme
Date: 04 November 2024
Usage:
    - Call the query_opentripmap function with a name of a city to get a list of relevant Events.
"""

import requests
from app.models.event_model import Event
from pathlib import Path
from app.config import OPENTRIPMAP_API_KEY
from pydantic import BaseModel, PositiveInt, model_validator
import copy
from app.api.translation import translate_text

HOST = "opentripmap-places-v1.p.rapidapi.com"
VALID_KINDS_FILE_PATH = Path(__file__).resolve().parents[2] / 'app' / 'api' / 'opentripmap_valid_kinds.txt'

def make_request(endpoint: str, query_params: dict) -> dict:
    """General request function for OpenTripMap API"""

    # variables
    headers = {
        "X-RapidAPI-Key": OPENTRIPMAP_API_KEY,
        "X-RapidAPI-Host": HOST
    }
    full_url = f"https://{HOST}/{endpoint}"

    # make request
    response = requests.get(
        url=full_url, 
        headers=headers, 
        params=query_params
    )

    # parse request if valid
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"""
            Error {response.status_code} in make_request 
            for url {full_url} 
            with headers {headers} 
            and params {query_params}
            : {response.text}
        """)

class OpenTripMapModel(BaseModel):
    placename:      str
    radius:         PositiveInt | None  = None
    walking_time:   PositiveInt | None  = 5
    kinds:          list[str]           = []
    limit:          PositiveInt | None  = 10
    filter:         str | None          = None

    @model_validator(mode='after')
    def check_if_model_is_valid(self):
        if self.radius is not None and self.walking_time is not None:
            raise Exception(f"""
            ParamError in query_opentripmap.
            Please specify a radius or walking_time, but not both.
            Radius was {self.radius} and walking_time was {self.walking_time}.
            """)
        if self.radius is None and self.walking_time is None:
            raise Exception("""
            ParamError in query_opentripmap.
            Please specify a radius or walking_time.
            """)
        if self.walking_time is not None:
            self.radius = (self.walking_time * 60) * 3   # assume 3m/s in bird flight distance
        
        if self.limit is not None and self.limit <= 0:
            raise Exception(f"""
            ParamError in query_opentripmap.
            Please specify a positive integer for limit instead of {self.limit}. 
            """)
        if self.filter is not None and len(self.filter) < 3:
            print(f"Filter was {self.filter}, but it has to be at least 3 characters. It will be ignored.")
            self.filter = None
        return self

def load_valid_kinds(query_kinds: list[str]):
    # TODO cache it
    with open(VALID_KINDS_FILE_PATH, 'r') as file:
        valid_set = set(line.strip() for line in file)

    kinds = [kind.lower().replace(" ", "_") for kind in query_kinds]
    valid_kinds: list[str] = []
    for kind in kinds:
        if kind in valid_set:
            valid_kinds.append(kind)
        else:
            print(f"{kind} is not a valid kind. It will be ignored.")
    return valid_kinds

def query_opentripmap(query: OpenTripMapModel):
    """Fetch events from OpenTripMap API.
    https://dev.opentripmap.org/docs#/Objects%20list/getListOfPlacesBySuggestions.

    Attributes:
        placename:      eg. Paris
        radius:         in meters (ór radius ór walking_time is mandatory)
        walking_time:   in minutes (ór radius ór walking_time is mandatory)
        kinds:          eg. ['foods', 'fountains'] (empty list means all kinds)
        limit:          Maximum number of returned objects.
        filter:         String to filter on (eg. 'don' for McDonalds) (at least 3 chars)

    >>> type(query_opentripmap('Paris', limit=1, kinds=['foods']))
    <class 'list'>
    """

    print(f"""Querying OpenTripMap for: 
    placename={query.placename}, 
    radius={query.radius}, 
    walking_time={query.walking_time},
    kinds={query.kinds},
    limit={query.limit},
    filter={query.filter}""")
    
    # first get location coordinates
    result = make_request(
        endpoint="en/places/geoname",
        query_params={"name": query.placename.capitalize()}
    )
    if result['status'] != 'OK':
        raise Exception(f"""
            Error status not OK in query_opentripmap
            for placename {query.placename}.
            Full result: {result}
        """)
    
    valid_kinds = load_valid_kinds(query.kinds)
        
    query_params = {
        "lon":      str(result['lon']),
        "lat":      str(result['lat']),
        "radius":   str(query.radius),
        "limit":    str(query.limit),
        "format":   'json'
    }

    if len(valid_kinds) != 0:
        query_params["kinds"] = ','.join(valid_kinds)
    
    # next, get the POI
    if query.filter is not None:
        query_params["name"] = query.filter
        endpoint = "en/places/autosuggest"
    else:
        endpoint="en/places/radius"

    result = make_request(
        endpoint=endpoint,
        query_params=query_params
    )
    
    # ID, NAME, LOCATION
    events = [Event(
        id          = obj['xid'],
        name        = obj['name'],
        location    = query.placename,  # opentripmap returns the exact coordinates as well
        #category    = obj['kinds'],    # opentripmap returns a list of relevant categories
    ) for obj in result if obj['name']]

    # post-processing: get more info about the place using the xid
    new_events = []
    for event in events:
        new_event = copy.deepcopy(event)
        try:
            details = make_request(
                endpoint=f"en/places/xid/{str(event.id)}",
                query_params=query_params
            )
            # CATEGORY
            if "kinds" in details:
                new_event.category = details["kinds"].split(",")[0] # pick the first one as the model doesn't allow multiple categories
            # PRIORITY
            if "rate" in details:
                try:
                    new_event.priority = int(details["rate"])
                except:
                    pass # sometimes the rate is not an integer but for example "3h"
            # URL
            if "wikipedia" in details:
                new_event.url = details["wikipedia"]
            
            # DESCRIPTION
            try:
                summary = details["wikipedia_extracts"]["text"]

                # maximum character limit is 500
                sentences = summary.split(".")
                shortened = False
                while len(summary) >= 500:
                    sentences = sentences[:-1]
                    summary = ". ".join(sentences)
                    shortened = True
                if shortened:
                    summary += "."

                try:
                    # use translation if exists (country code)
                    language = details["address"]["country_code"]
                    translated = translate_text(summary, language, "en")
                    new_event.description = translated
                except Exception as e:
                    print(f"Couldn't translate. {e}")
                    try:
                        # use translation if exists (wikipedia tag)
                        language = details["wikipedia_extracts"]["title"].split(":")[0]
                        translated = translate_text(summary, language, "en")
                        new_event.description = translated
                    except:
                        # if translation failed, just use the original
                        new_event.description = summary
            except:
                # if something goes wrong while retrieving a description, just dont use it
                pass
            pass

        except Exception as e:
            print(e)

        finally:
            new_events.append(new_event)

    return new_events
    
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()