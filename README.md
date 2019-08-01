# ConceptNet offline API

This is the API for ConceptNet to use offline, e.g. if you want to work on a part of data it is much faster to use offline version than to query web API.

## Offline version of ConceptNet

ConceptNet provides offline database at [the following link](https://s3.amazonaws.com/conceptnet/downloads/2019/edges/conceptnet-assertions-5.7.0.csv.gz "ConceptNet csv")

## Usage

API provides some basic functionality to load csv database into memory (requires ~10GB of RAM), filter the language at the beginning in order to free some memory (and save smaller version of database) and query for edges according to start and/or end node along with relation.

### Example
For a quick example just go for:
```
python example.py -p database_path
```

### Loading

In order to load the database into memory just import the ConceptNet class and provide the path to the file you have downloaded and unpacked.
```python
from conceptNet import ConceptNet

conceptnet = ConceptNet('assertions.csv', language='english', save_language=True)
# or
conceptnet = ConceptNet('assertions_english.pkl')
```
Arguments:
 - `data_path` - path to the csv or pkl file with database
 - `language` - list of languages (or single language) to filter from database
 - `save_language` - flag to save new database under the old name with __first_language_on_the_list.pkl_

### Querying

Query your database by:
```python
query_result = database.get_query(start=['start'], end=['end1', 'end2'], relation='relation')
```
Arguments:
 - `start` - word to be found in the starting node
 - `end` - word to be found in the end node
 - `relation` - relation type (take a look at ConceptNet documentation for the list of possibilities)

All the arguments take either string or list of strings for the query.
