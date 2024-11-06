import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.api import nlp, events, weather
from app.api.opentripmap import query_opentripmap

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the request body model
class QueryRequest(BaseModel):
    user_input: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel Assistant"}

# endpoint accepts a JSON body via Pydantic model
@app.post("/query/")
def process_query(query: QueryRequest):
    print(f"Query: {query}")
    try:
        # Step 1: NLP extraction (city, date, keywords)
        info = nlp.extract_info(query.user_input)  # Use query.user_input from the model
        print(f"NLP extraction: {info}")

        # Step 2: Check if any pinned events exist
        city = info.get('city')
        date = info.get('date')
        keywords = info.get('keywords')

        pinned_events = events.check_pinned_events(city, date)

        if pinned_events:
            return {"result": f"Prioritized event: {pinned_events}"}

        # Step 3: Fetch events from OpenTripMap
        event_results = query_opentripmap(city, kinds=keywords)

        # Step 4: Fetch weather from OpenWeatherMap
        weather_info = weather.query_weather(city, date)

        # Step 5: Return the compiled response
        return {
            "events": event_results,
            "weather": weather_info
        }
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)  # Log the error details
        raise HTTPException(status_code=500, detail="Internal Server Error")
