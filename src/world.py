
'''
World State Object
'''
from country import Country
from resource import Resource
import pandas as pd


class WorldState:

    def __init__(self):

        self.countries: list = []
        self.resource_template: dict = {}

        # load in resource file
        df = pd.read_csv('resources/example-resources.csv')
        resource_cols = ["Resource", "Weight", "Notes"]
        print(f"loading resources file...")
        for idx, row in df.iterrows():
            resource_props = dict(
                zip(resource_cols, [row[v] for v in resource_cols]))
            self.resource_template[row["Resource"]] = resource_props

        print(self.resource_template)

        # load in world state
        print(f"loading countries file...")
        df = pd.read_csv('resources/example-initial-countries.csv')
        resource_cols = ["R1", "R2", "R3", "R21", "R22",
                         "R23", "R21'", "R22'", "R23'"]

        for idx, row in df.iterrows():
            country_name = row['Country']

            c: Country = Country()
            c.name = country_name

            # Countries initial Resources by Quantity
            for res_name in resource_cols:
                r: Resource = Resource()
                r.name = res_name
                r.quantity = int(row[res_name])
                r.weight = self.resource_template[res_name]["Weight"]
                r.descript = self.resource_template[res_name]["Notes"]
                c.resources[res_name] = r

            self.countries.append(c)

        print("Countries Loaded: ")
       # self.countries[0].print()
