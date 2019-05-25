## Template Manager
a flask server that implements API and functionality for writing and testing templates and generating question from them, that used in a question game named whoknows


## How to install?
Setting up is simple, just follow these steps.

#### Python :

1. Install python and pip and git:
```sh
apt install git python3 python3-pip
```

2. Clone the repository:
```sh
git clone ...
```

3. Go to repository folder:
```sh
cd guessit-template-manager
```

4. Install dependencies:
```sh
pip install -r requirements.txt
```

5. Start server:
```sh
python3 app.py
```

####  Docker :

1. Clone the repository:
```sh
git clone ...
```

2. Go to repository folder:
```sh
cd guessit-template-manager
```

3. Build image from dockerfile:
```sh
docker build -t guessit-template-manager
```

4. Run docker image:
```sh
docker run -it guessit-template-manager
```


## What it does?
Template manager implements functionality for the followings concepts:

- Write template:

- Test template:

- generate question:


## How to use?
API documentation url : 


## Who is in charge: 
- Mohammad Parsian
- Danial Keimasi
- Moein Samadi

--------------------------------------------------------------------------------


# Whoknows Template Manager
generates questions by the given data and templates.  
for a big question game.

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

### Load
this commands must use in "values" part of templates

Command | Description
------- | -------
db( dataset_name ) | load a dataset by it's name
db( loaded_dataset[ condition ] ) | filter a loaded dataset and get subdata from it
rand( dataset , number_of_elements ) | choose randomly from a dataset (or list) of data by numbers that we want
listSub(loaded2.property, loaded1.propery) | subtract two dataset: loaded2 data that not have loaded1.property in it

### Choosing
Command | Description
------- | -------
var.loaded_dataset.choose( number_of_elements ).property | select number of duc from loaded dataset and get a list of properties

  
  
# Data Catalogs
you can find data catalogs in here
  
[data-catalog dir](https://github.com/danialkeimasi/whoknows-template-manager/blob/master/data_catalogs/)
