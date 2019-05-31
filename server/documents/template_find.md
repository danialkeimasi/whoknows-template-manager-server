# New Template

Returns json data about a single user.

* ##### URL

  /template/find

* ##### Method:

  `POST`

* ##### Data Params

     **Optional:**

   `count=int`

* ##### Success Response:

  * **Code:** 200 <br />
    **Content:** `[{...}, ...]`

* ##### Error Response:

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "User doesn't exist" }`
