# world-trade-ai-part1

## Intro: 
This Repository describes an AI Agent capable of performing Transforms and Transfers/Trades with other World Trade AI agents, as well as predict in advanced 'N' steps based on its cost function and optimization strategy


## Structures:

Primary data structures implementing this search include the:
- World State: Collections of Countries/their resource destribution
- Node: implementation/state container for search
- Country: Entity/Controller of resources
- Resource: representation of material resources Countries can use/trade
- Solutions: Node/tree search resulting in achieving specified depth
- Frontier: structure holding the actively searched states
