'''
Country structure:

County Name/Identifier, and Material Listing/Manifest each countries

'''


class Country:
    name: str = ""
    resources: list = []

    # define a print out of the Country and their resource list
    def print(self):
        print("Country: " + self.name)
        [print(r.name + ":" + str(r.quantity)) for r in self.resources]
