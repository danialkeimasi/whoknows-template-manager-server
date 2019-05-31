# New Template

Find a list of templates by given request

* #### URL

  /template/find

* #### Method:

  `POST`

* #### Data Params

     **Optional:**

   `count=int`
   `query=object`
   `tags=[string]`
   

* #### Success Response:

  * **Code:** 200 <br />
    **Content:** `[{...}, ...]`

* #### Error Response:

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "User doesn't exist" }`
