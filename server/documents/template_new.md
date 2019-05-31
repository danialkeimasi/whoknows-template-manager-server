# New Template

Returns json data about a single user.

* ##### URL

  /template/new

* ##### Method:

  `POST`
  
* ##### Data Params

     **Required:**
 
   `idea=string`

* ##### Success Response:

  * **Code:** 200 <br />
    **Content:** `[{...}, ...]`
 
* ##### Error Response:

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "User doesn't exist" }`
