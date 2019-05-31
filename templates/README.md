# Template
we use templates for make questions, you can read how ...

# Question template example
```json
{
    "values": {
        "value": "db(dataset_name[query])"
    },
    "&bool": {
        "title": {}
    },
    "&choose": {
        "title": {},
        "answer": {},
        "choice": {}
    },
    "&write": {
        "title": {},
        "answer": {}
    },
    "&select": {
        "title": {},
        "choice": {},
        "answer": {}
    },
    "datasets": [],
    "tags": [],
    "usage": ["contest"],
    "__state": "idea",
    "__test_info": {
        "duplication": { "similars": [] },
        "acceptance": { "votes": [] },
        "data": { "datasets": [] },
        "structure": { "sections": [] },
        "generation": { "result": [] }
    },
    "__idea": [""]
}
```

# Template cheat sheet
you can make question templates with following cheat sheet

### Load Data
this commands must use in "values" part of templates

Command | Description
------- | -------
db( dataset_name ) | load a dataset by it's name
db( loaded_dataset[ condition ] ) | filter a loaded dataset and get subdata from it
rand( dataset , number_of_elements ) | choose randomly from a dataset (or list) of data by numbers that we want
listSub(loaded2.property, loaded1.propery) | subtract two dataset: loaded2 data that not have loaded1.property in it

### Choosing Data
Command | Description
------- | -------
var.loaded_dataset.choose( number_of_elements ).property | select number of duc from loaded dataset and get a list of properties
var.loaded_dataset.one.property | select one doc from loaded dataset and get a list of properties


--------------------------------------------------------------------------------
  
# Data Catalogs
you can find data catalogs in here
  
[data-catalog dir](../data_catalogs)
