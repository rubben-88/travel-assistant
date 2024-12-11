import pandas as pd

df = pd.read_csv('app/city_checker/worldcities.csv')

# to a set for fast lookup
city_set = set(df['city'].str.lower().str.strip())

def is_city(keyword):
    return keyword.lower().strip() in city_set