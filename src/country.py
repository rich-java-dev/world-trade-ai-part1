'''
Country structure:

County Name/Identifier, and Material Listing/Manifest each countries

'''


class Country:

    def __init__(self):
        self.name: str = ""
        self.resources: dict = {}
        self.printer = print

    # define a print out of the Country and their resource list
    def print(self):
        self.printer("Country: " + self.name+'\n')
        [self.printer(r.name + ":" + str(r.quantity)+'\n')
         for r in self.resources.values()]
