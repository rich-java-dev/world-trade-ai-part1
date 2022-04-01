# World-Trade Scheduling AI - Agent 

## Overview

The aim of this project is to demonstrate, build an understanding, 
and engineer an AI agent which is required to solve optimization searches  in a complex/highly-branching environment,
 with the practical aim of building and testing predictive models that allow for a depth-bounded, forward searching to optimize a utility.

Based on the core constraints, namely 
trading templates, 
resource files, 
and varying initial world country/resource distributions,

## Set-up/basic usage

- "git clone https://github.com/rich-java-dev/world-trade-ai-part1.git"
- "pip install -r requirements.txt"
- "python src/main.py"


## Advanced options

"python src/main.py --help"
options: 
- model (--model/--m/-m) - "DFS"(default) / "UCS"
- depth (--depth/--d/-d) - Search Depth of the model (primary model-bound param)
- soln_set_size (--s/-s) - size of "top"/tracked solutions relative to the entire search
- initial_state_file (--i/-i) - 4 coded state files which describe initial world resource allocations
- output (--o/-o) - output file (txt) final/completed search schedule prints to


### samples:
- "python src/main.py" - (default: depth 5, depth-first-search, init file 1, retain top 2 schedules)
- "python src/main.py -d 10" - (depth 10, DFS)
- "python src/main.py -m UCS" (Djikstra/Uniform Cost Search)
- "python src/main.py -i 2 -s 5" (init file 2 ('hard' mode), retain top  2 schedules)
- "python src/main.py -d 10 -i 4" (depth 10, DFS, on initial state 4)

## Structures

### file/module:

- main - driver/entry point for the module/program

- resource 
  - description of a 'thing that has utility'. Resources have 2 major utilities:
  - Transforming/consuming for a given purpose, or traded to another country.

- country 
  - A 'World' Entity which maintains a pool of resources.
  - Countries can either transform or trade their resources.

- world 
  - "World Resource Manifest" - A Collection of Countries, which each have their own resource distributions, including populations, metallic alloys, and timber, and subsequent resultants. This struction is the underlying "Physical System/State" that is tracked (independent/outside of the mathematical abstractions we imposed on it).

- events - 2 Major structs trigger changes in world state: Transformations, and Trades.
  - Transformations: Interal to a single country, transformations take existing resourcing and transform them into new resources.
  - Trades: 2 countries involved, each offer a distinct 1 resource and quantity for a simplified trade

- quality - The Quality/"Unbounded Utility Function" describing the state of given Country based purely resources
  
- goals - Abstraction used to build up the entire "Quality" function- including successfully meeting attributes such as "no homelessness", "balanced electronics", "materials on-hand per capita".
  
- node - Data Structure used to encapsulate the World State, and its evolution/change over time. 
  - Implements the "composite" pattern in a traditional Recursive Data structure, like a Tree. This structure tracks a given countries 'trajectory'/options in the forward search implementation

## Observations/Findings

### Simulations ran:
I modelled 4 initial state files, roughly corresponding to "4 quadrants" on a plane splitting Wealth and Equality...
- Initial State 1: Wealthy Country in a world of Inequality
- Initial State 2: Poor Country in a world of Inequality
- Initial State 3: Wealthy Country in an equally wealthy world
- Initial State 4: Poor Country in an equally poor world

### Additional Notes:
Based on my current implementation, the AI agent LOVES to trade, especially on margins... There is a tendency to think any trade that is ~45-50%% likely- meaning there is a slight advantage for the agent, is the best type of trade, and will pursue those rigoursly before any internal transformations, including alloys, housing, and electronics.

I've noticed this is especially true as a poor country: Based on current quality function implementations, a country that can only make about 5% of a countries needed infrastructure will spend far more time seraching for viable trades for more resources before building any infrastructure.
