## Template Manager
this repository contains a flask server that implements REST API and functionality for writing and testing templates and generating question from the given templates and data. this questions used in a question game named [whoknows](http://whoknows.ir)

![whoknows logo](http://s8.picofile.com/file/8361648192/logo_5_3.png)

## How to install?
Setting up is simple, just follow these steps.

### Python :

1. Install python and pip and git:
```sh
apt install git python3 python3-pip
```

2. Clone the repository:
```sh
git clone https://github.com/danialkeimasi/whoknows-template-manager
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

### Docker :

1. Clone the repository:
```sh
git clone https://github.com/danialkeimasi/whoknows-template-manager
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
### :cloud:API documentation url : 

1. [template new](server/documents/template_new.md)
2. [template find](server/documents/template_find.md)


## Who is in charge: 
- Mohammad Parsian
- Danial Keimasi
- Moein Samadi
