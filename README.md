# Game of Thrones Search


## Prologue

A situation we've almost all found ourselves in is wondering "Which episode did 
I leave off?" when returning to a TV show.

## Task

This search engine aims to answer the question "Which episodes are most 
relevant to my query?" It reads in your query and outputs the most likely 
matches (as Season and Episode pairs)


## Architecture

Three components:
1. A `crawler` to retrieve data and produce documents
2. An `indexer` to store documents for fast and accurate retrieval
3. A `query engine` to faciliate queries for relevant documents


## Comments

The specific search domain here is Game of Thrones. But I certainly hope my
code doesn't suck so much that none of it can be abstracted.

