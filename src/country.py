'''
Country structure:

County Name/Identifier, and Material Listing/Manifest each countries

'''


class Country:

    def __init__(self):
        self.name: str = ""
        self.resources: dict = {}

    # define a print out of the Country and their resource list
    def print(self):
        print("Country: " + self.name)
        [print(r.name + ":" + str(r.quantity)) for r in self.resources.values()]
