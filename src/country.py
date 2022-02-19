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
        nl = '\n' if not self.printer == print else ''
        self.printer(f'Country: {self.name} {nl}')
        [self.printer(f'{r.name}:{r.quantity}{nl}')
         for r in self.resources.values()]
