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
    <td>[\D]{3,20}</td>
    <td>
    نام کامل مربی
    </td>
  </tr>
 
  <tr>
    <td>club</td>
    <td>string</td>
    <td>.{2,20}</td>
    <td>
    نام کامل تیمی که در آن مربیگری میکند مانند FC Barcelona
    </td>
  </tr>

  <tr>
    <td>nation</td>
    <td>string</td>
    <td>\D{3,40}</td>
    <td>
    ملیت مربی
    </td>
  </tr>


  <tr>
    <td>birthyear</td>
    <td>unsignint</td>
    <td>\d{4}</td>
    <td>
    سال تولد مربی
    </td>
  </tr>

</table> 
