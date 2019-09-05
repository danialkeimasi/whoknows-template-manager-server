# Template new

add a new template by given name

* #### URL

  /template/new

* #### Method:

  `POST`
  
* #### Data Params

     **Required:**
 
   `name=string`

* #### Success Response:

  * **Code:** 200 <br />
    **Content:** `[{...}, ...]`
 
* #### Error Response:

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "User doesn't exist" }`
