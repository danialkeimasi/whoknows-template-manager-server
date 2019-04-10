# Guessit Question Manager
generates questions by the given data and templates.  
for a big question game.

# Question template example
```
[
  {
    "values"	: {
      "team"          : "db( footballTeam )",
      "team_same"     : "db( footballTeam[ footballTeam.league == var.team.league ] )",
      "leagues"       : "DataContainer(list( set(footballTeam.league)- set([var.team.league]) ))",
      "CL"            : "var.leagues",
      "True_or_False" : "rand( [True,False] )"
    },

    "title_true_false"      : ["تیم `var.team.name` در لیگ `var.team.league` فعالیت میکند" , "تیم `var.team.name` در لیگ `var.CL.choose(1)` فعالیت میکند"], 
    "title_multichoices"    : ["تیم `var.team.name` در کدام لیگ فعالیت میکند" , "تیم `var.team.name` و `var.team_same.name` در کدام لیگ فعالیت میکنند؟" ],
    "title_writing"         : ["تیم `var.team.name` در کدام لیگ فعالیت میکند"],
    "answer_multichoices"   : ["var.team.league"],
    "answer_writing"        : ["var.team.league"],
    "answer_true_false"     : ["var.True_or_False"],
    "choices_multichoices"  : ["var.CL.choose(NOC)"],
    "__usage"               : ["contest"],
    "__number"              : 1,
    "__level"               : 1
  }
]
```

# Cheat sheet
you can make question templates with following cheat sheet

## Load
this commands must use in "values" part of templates

Command | Description
------- | -------
db( dataset_name ) | load a dataset by it's name
db( loaded_dataset[ condition ] ) | filter a loaded dataset and get subdata from it
rand( dataset , number_of_elements ) | choose randomly from a dataset (or list) of data by numbers that we want
listSub(loaded2.property, loaded1.propery) | subtract two dataset: loaded2 data that not have loaded1.property in it

## Choosing
Command | Description
------- | -------
var.loaded_dataset.choose( number_of_elements ).property | select number of duc from loaded dataset and get a list of properties
