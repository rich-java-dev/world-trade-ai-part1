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

python&nbsp; src\main.py&nbsp; --help<br />
usage:&nbsp; main.py&nbsp; [-h]&nbsp; [--model&nbsp; MODEL]&nbsp; [--depth&nbsp; DEPTH]&nbsp; [--gamma&nbsp; GAMMA]&nbsp; [--k&nbsp; K]&nbsp; [--threshold&nbsp; THRESHOLD]&nbsp; [--schedule_threshold&nbsp; SCHEDULE_THRESHOLD]&nbsp; [--soln_set_size&nbsp; SOLN_SET_SIZE]&nbsp; [--initial_state_file&nbsp; INITIAL_STATE_FILE]<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [--beam_width&nbsp; BEAM_WIDTH]&nbsp; [--max_solutions&nbsp; MAX_SOLUTIONS]&nbsp; [--max_nodes&nbsp; MAX_NODES]<br />
<br />
CLI&nbsp; args&nbsp; to&nbsp; fine-tuning/running&nbsp; variants&nbsp; on&nbsp; the&nbsp; World&nbsp; Trade/Game&nbsp; Search<br />
<br />
optional&nbsp; arguments:<br />
&nbsp; &nbsp; -h,&nbsp; --help&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; show&nbsp; this&nbsp; help&nbsp; message&nbsp; and&nbsp; exit<br />
&nbsp; &nbsp; --model&nbsp; MODEL,&nbsp; --m&nbsp; MODEL,&nbsp; -m&nbsp; MODEL<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Choosing&nbsp; Search&nbsp; Model-&nbsp; DFS&nbsp; (greedy-local-depth-first-search&nbsp; UCS&nbsp; (uniform-cost&nbsp; search&nbsp; (Djikstra)<br />
&nbsp; &nbsp; --depth&nbsp; DEPTH,&nbsp; --d&nbsp; DEPTH,&nbsp; -d&nbsp; DEPTH<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Search&nbsp; Depth&nbsp; of&nbsp; the&nbsp; model<br />
&nbsp; &nbsp; --gamma&nbsp; GAMMA,&nbsp; --g&nbsp; GAMMA,&nbsp; -g&nbsp; GAMMA<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Decay&nbsp; constant&nbsp; gamma,&nbsp; which&nbsp; dampens/discounts&nbsp; the&nbsp; quality&nbsp; function:&nbsp; domain&nbsp; [0-1]<br />
&nbsp; &nbsp; --k&nbsp; K,&nbsp; -k&nbsp; K&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Logistic&nbsp; Curve&nbsp; Steepness&nbsp; constant<br />
&nbsp; &nbsp; --threshold&nbsp; THRESHOLD,&nbsp; --t&nbsp; THRESHOLD,&nbsp; -t&nbsp; THRESHOLD<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Probability&nbsp; Threshold:&nbsp; Do&nbsp; not&nbsp; pursue&nbsp; schedules&nbsp; which&nbsp; are&nbsp; less&nbsp; likely&nbsp; than&nbsp; desired&nbsp; likelihood:&nbsp; domain&nbsp; [0-1]<br />
&nbsp; &nbsp; --schedule_threshold&nbsp; SCHEDULE_THRESHOLD,&nbsp; --st&nbsp; SCHEDULE_THRESHOLD,&nbsp; -st&nbsp; SCHEDULE_THRESHOLD<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Probability&nbsp; Threshold:&nbsp; Do&nbsp; not&nbsp; pursue&nbsp; schedules&nbsp; which&nbsp; are&nbsp; less&nbsp; likely&nbsp; than&nbsp; desired&nbsp; likelihood:&nbsp; domain&nbsp; [0-1]<br />
&nbsp; &nbsp; --soln_set_size&nbsp; SOLN_SET_SIZE,&nbsp; --s&nbsp; SOLN_SET_SIZE,&nbsp; -s&nbsp; SOLN_SET_SIZE<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Number&nbsp; of&nbsp; Solutions&nbsp; (Depth&nbsp; achieved)&nbsp; to&nbsp; track&nbsp; in&nbsp; the&nbsp; best&nbsp; solutions&nbsp; object<br />
&nbsp; &nbsp; --initial_state_file&nbsp; INITIAL_STATE_FILE,&nbsp; --i&nbsp; INITIAL_STATE_FILE,&nbsp; -i&nbsp; INITIAL_STATE_FILE<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; enum&nbsp; 1-4.&nbsp; initial&nbsp; state&nbsp; file&nbsp; for&nbsp; loading&nbsp; the&nbsp; simulation/search:&nbsp; 1)&nbsp; resource&nbsp; rich&nbsp; country&nbsp; in&nbsp; world&nbsp; with&nbsp; uneven&nbsp; resource&nbsp; distribution&nbsp; (NORMAL&nbsp; MODE)&nbsp; 2)&nbsp; resource&nbsp; poor&nbsp; country&nbsp; in&nbsp; world&nbsp; with&nbsp; uneven&nbsp; resource<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; distribution&nbsp; (BRUTAL&nbsp; MODE)&nbsp; 3)&nbsp; resource&nbsp; moderate&nbsp; country&nbsp; in&nbsp; world&nbsp; with&nbsp; even&nbsp; resource&nbsp; distribution&nbsp; (EASY&nbsp; MODE)&nbsp; 4)&nbsp; resource&nbsp; poor&nbsp; country&nbsp; in&nbsp; world&nbsp; with&nbsp; even&nbsp; resource&nbsp; distribution&nbsp; (HARD&nbsp; MODE)<br />
&nbsp; &nbsp; --beam_width&nbsp; BEAM_WIDTH,&nbsp; --b&nbsp; BEAM_WIDTH,&nbsp; -b&nbsp; BEAM_WIDTH<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; used&nbsp; to&nbsp; prune/reduce&nbsp; search&nbsp; size&nbsp; by&nbsp; limiting&nbsp; the&nbsp; maximum&nbsp; number&nbsp; of&nbsp; successor&nbsp; nodes&nbsp; placed&nbsp; on&nbsp; the&nbsp; stack&nbsp; at&nbsp; each&nbsp; step<br />
&nbsp; &nbsp; --max_solutions&nbsp; MAX_SOLUTIONS,&nbsp; --c&nbsp; MAX_SOLUTIONS,&nbsp; -c&nbsp; MAX_SOLUTIONS<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; set&nbsp; a&nbsp; fundamental&nbsp; cap&nbsp; on&nbsp; how&nbsp; many&nbsp; satisfiable&nbsp; schedules&nbsp; searched.&nbsp; NOTE:&nbsp; node/state&nbsp; must&nbsp; not&nbsp; only&nbsp; be&nbsp; viable/non-zero&nbsp; probability,&nbsp; but&nbsp; must&nbsp; satisfy&nbsp; schedule&nbsp; needs<br />
&nbsp; &nbsp; --max_nodes&nbsp; MAX_NODES,&nbsp; --n&nbsp; MAX_NODES,&nbsp; -n&nbsp; MAX_NODES<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; set&nbsp; a&nbsp; fundamental&nbsp; cap&nbsp; on&nbsp; States&nbsp; to&nbsp; explore.&nbsp; NOTE:&nbsp; node/state&nbsp; need&nbsp; only&nbsp; be&nbsp; viable<br />


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
