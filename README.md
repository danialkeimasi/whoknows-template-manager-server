# Guessit Question Manager
generates questions by the given data and templates.
for a big question game.

# Cheat sheat
you can make question templates with following cheat sheet

## load
Command | Description
------- | -------
db( dataset_name ) | load a dataset by it's name
db( loaded_dataset[ condition ] ) | filter a loaded dataset and get subdata from it
rand( dataset , number_of_elements ) | choose randomly from a dataset (or list) of data by numbers that we want
DataHelper( list( set(loaded2.property) - set(loaded1.propery) ) ) | subtract two dataset: loaded2 data that not have loaded1.property in it

## choosing
Command | Description
------- | -------
var.loaded_dataset.choose( #number_of_elements ).property | select #number of duc from loaded dataset and get a list of properties
