
'''
World State Object
'''
from country import Country
from resource import Resource
import pandas as pd


class WorldState:

    countries: list = []

    def __init__(self):

        # load in world state
        print(f"loading countries file...")
        df = pd.read_csv('resources/example-initial-countries.csv')
        resource_cols = ["R1", "R2", "R3", "R21", "R22", "R23"]

        for idx, row in df.iterrows():

            country_name = row['Country']

            c: Country = Country()
            c.name = country_name

            for res_name in resource_cols:
                r: Resource = Resource()
                r.name = res_name
                r.quantity = int(row[res_name])
                c.resources.append(r)

            self.countries.append(c)

        print("Countries Loaded: ")
        [country.print() for country in self.countries]
