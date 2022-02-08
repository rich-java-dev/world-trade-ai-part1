
'''
Resources structure:

The fundamental 'material' commodities which Countries aim to use to optimize their Goals/agenda/state quality.

Resources have the following properties:

utility:            A measure of "raw usefullness" of a given resource.
                    A sort of object heuristic
                    (not to be confused with our State Quality heuristic).

construction:       A resources ability to be used to expand "general infrastructure"

infrastructure:     A resources ability to be used to expand "general infrastructure"
                    This could be as simple as Wood for building housing/structures/furnature
                    Other higher order resources may include steel or cement for various uses
                    such as energy producing systems.

energy:             A measure of a resources raw 'energy' or 'combustible' useage.
                    Coal for power plants which with a high infrastructure provide high utility
                    to workers/business

r&d:                Resources consumed Leading to better technologies

technology:         Prereqs: R&D level leads to high utility resources, and

sustainability:     Measure of a resources ability to "self replenish" over time.
                    This kind of factor

liquidity:          value defining the weight of transactional "reasonableness" with other countries.
                    A high liquidity means its inherently valueable/easy to transfer with other countries.
                    Gold has high liquidity because its universally valueable and easily transferrable resource

culture:            The impact this resource has on Culture.
                    Very broadly defined, but
                    generally "higher order" resources such as food, art (music, visual, performance, etc)
                    forming a band from people and instruments for instance has high culture value

Resources also have a function which gives an aggregate admissible heuristic
(metric based on its "least useful" attribute based on how a resource gets utiltized in the least useful way)
This is also akin to a Mini-Max search, in which the "opponent" is minimizing the value I can get out of a resource.

'''


class Resource:

    def __init__(self):
        self.resource_id: int = 0
        self.name: str = ""
        self.quantity: int = 0
        self.weight: float = .7
        self.construction: int = 0
        self.infrastructure: int = 0
        self.energy: int = 0
        self.rnd: int = 0
        self.technology: int = 0
        self.nutrition: int = 0
        self.liquidity: int = 0
        self.culture: int = 0
        self.descript: str = ""
        self.critical_resource: bool = False
        self.price: int = 0

    def heuristic_value(self) -> float:
        return self.unit_price * self.quantity_on_hand

    def calc_utility_to_cost_ratio(self, utility_function) -> float:
        utility_function(self)
