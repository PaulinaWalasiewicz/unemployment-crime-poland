"""
fetch_data.py
Downloads unemployment, population and crime data for Polish voivodeships
from the GUS Local Data Bank (BDL) API and saves them as CSV files in data/raw/.
"""
import requests
import pandas as pd

BASE_URL = "https://bdl.stat.gov.pl/api/v1/data/by-variable/"

VARIABLES_UNP = {
    # unemployment and population
    60270: "unemployment_rate",
    60641: "population",
}
VARIABLES_CRIME ={
    # crimes
    58559: "crimes_total",
    77215: "crimes_criminal",
    77216: "crimes_economic",
    58561: "crimes_road",
    58564: "crimes_property",
    58562: "crimes_life_health",

    # crimes - per 1000
    398594: "crimes_total_per_1000",
    498627: "crimes_criminal_per_1000",
    498626: "crimes_economic_per_1000",
    498625: "crimes_road_per_1000",
    498623: "crimes_property_per_1000",
    498624: "crimes_life_health_per_1000",
}

def fetch_variable(var_id):
    url = f"{BASE_URL}{var_id}"
    params = {
        "unit-level":2,
        "page-size":100,
        "format":"json",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if len(data["results"]) != data["totalRecords"]:
        raise ValueError(
            f"Variable {var_id}: got {len(data['results'])} of {data['totalRecords']} units"
        )

    rows=[]
    for unit in data["results"]:
        for value in unit["values"]:
            rows.append({
                "unit_id": unit["id"],
                "voivodeship": unit["name"],
                "year": int(value["year"]),
                "value": value["val"],
            })
    return pd.DataFrame(rows)


# df = fetch_variable(60270)
# print(df.head())
# print(len(df))


all_tables_unp = []
for id,name in VARIABLES_UNP.items():
    print(f"Fetching {name}...")
    df = fetch_variable(id)
    df["variable"] = name
    all_tables_unp.append(df)
    
combined = pd.concat(all_tables_unp,ignore_index=True)
combined.to_csv("data/raw/bdl_data_unemployment.csv",index=False)
print(combined.shape)

all_tables_crime = []
for id,name in VARIABLES_CRIME.items():
    print(f"Fetching {name}...")
    df = fetch_variable(id)
    df["variable"] = name
    all_tables_crime.append(df)
    
combined2 = pd.concat(all_tables_crime,ignore_index=True)
combined2.to_csv("data/raw/bdl_data_crime.csv",index=False)
print(combined.shape)