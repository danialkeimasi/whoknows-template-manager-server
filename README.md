## Template Manager
this repository contains a flask server that implements REST API and functionality for writing and testing templates and generating question from the given templates and data. this questions used in a question game named [whoknows](http://whoknows.ir)

![whoknows logo](http://s8.picofile.com/file/8361648192/logo_5_3.png)

## :minidisc: How to install?
Setting up is simple, just follow these steps.

- ### Python :
    
    1. Install python and pip and git:
        ```
        apt install git python3 python3-pip
        ```
    
    2. Clone the repository:
        ```
        git clone https://github.com/danialkeimasi/whoknows-template-manager
        ```
    
    3. Go to repository folder:
        ```
        cd whoknows-template-manager
        ```
    
    4. Install dependencies:
        ```
        pip install -r requirements.txt
        ```
    
    5. Start server:
        ```
        python3 app.py
        ```

- ### Docker :
    
    1. Clone the repository:
        ```
        git clone https://github.com/danialkeimasi/whoknows-template-manager
        ```
    
    2. Go to repository folder:
        ```
        cd whoknows-template-manager
        ```
    
    3. Build image from dockerfile:
        ```
        docker build . -t whoknows-template-manager
        ```
    
    4. Run docker image:
        ```
        docker run -it whoknows-template-manager
        ```

## :mag: What it does?
Template manager implements functionality for the followings concepts:

- Write template:

- Test template:

- generate question:

    
## :question: How to use?
- ### API Documentation

1. [question generate](routes/documents/question_generate.md)
2. [template edit](routes/documents/template_edit.md)
3. [template find](routes/documents/template_find.md)
4. [template new](routes/documents/template_new.md)
5. [template test](routes/documents/template_test.md)
  
- ### Templates Documentation
    1. you can read about templates and learn how to write a template [here](templates/).
    2. if you need to know about data-catalogs click [here](data_catalogs/)
## :bust_in_silhouette: Who is in charge: 
- Mohammad Parsian
- Danial Keimasi
- Moein Samadi
