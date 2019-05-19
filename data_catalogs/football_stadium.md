 <table>
  <tr>
    <th>Field</th>
    <th>Type</th>
    <th>Regex</th>
    <th>Descereption</th>
  </tr>
 
  <tr>
    <td>name</td>
    <td>string</td>
    <td>.{3,40}</td>
    <td>
    نام کامل استادیوم
    </td>
  </tr>
 
  <tr>
    <td>club</td>
    <td>string</td>
    <td>.{2,20}</td>
    <td>
    نام کامل تیم مانند FC Barcelona
    </td>
  </tr>

  <tr>
    <td>capacity</td>
    <td>unsignint</td>
    <td>\d{3,6}</td>
    <td>
    گنجایش ورزشگاه
    </td>
  </tr>

  <tr>
    <td>city</td>
    <td>string</td>
    <td>\D{3,30}</td>
    <td>
    شهری که استادیوم در آن قرار دارد
    </td>
  </tr>

  <tr>
    <td>country</td>
    <td>string</td>
    <td>[\D]{4,35}</td>
    <td>
    کشوری که استادیوم در آن قرار دارد
    </td>
  </tr>

  <tr>
    <td>field_size</td>
    <td>string</td>
    <td>.{1,20}</td>
    <td>
    اندازه ی زمین
    </td>
  </tr>

  <tr>
    <td>opened</td>
    <td>unsignint</td>
    <td>\d{4}</td>
    <td>
    سال بازگشایی استادیوم
    </td>
  </tr>
 
</table> 
