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
    نام کامل جایزه بدون سال (توپ طلاfifa ballon dor)
    </td>
  </tr>
 
 
  <tr>
    <td>year</td>
    <td>string</td>
    <td>\d{4,9}</td>
    <td>
    سال یا فصلی که جایزه متعلق به آن است
    </td>
  </tr>
 
 
  <tr>
    <td>winner</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    نام برنده(برندگان) جایزه
    </td>
  </tr>
 
  <tr>
    <td>winner_N</td>
    <td>unsignint</td>
    <td>\d{1,4}</td>
    <td>
    تعداد رای(گل یا ...) برنده(برندگان) جایزه
    </td>
  </tr>
 
 
  <tr>
    <td>second</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    نام نفر(نفرات) دوم
    </td>
  </tr>
 
 
  <tr>
    <td>second_N</td>
    <td>unsignint</td>
    <td>\d{1,4}</td>
    <td>
    تعداد رای(گل یا ...) نفر(نفرات) دوم
    </td>
  </tr>
 
 
 
  <tr>
    <td>third</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    نام نفر(نفرات) سوم
    </td>
  </tr>
 
 
  <tr>
    <td>third_N</td>
    <td>unsignint</td>
    <td>\d{1,4}</td>
    <td>
    تعداد رای(گل یا ...) نفر(نفرات) سوم
    </td>
  </tr>
 
 
  <tr>
    <td>pic</td>
    <td>string</td>
    <td>.{3,4000}</td>
    <td>
    لینک عکس جایزه
    </td>
  </tr>
 
 
  <tr>
    <td>area</td>
    <td>string</td>
    <td>.{3,40}</td>
    <td>
     منطقه یا کشوری که جایزه متعلق به آن است مثل جهانی ، اروپا ، اسپانیا و یا ...
    </td>
  </tr>
 

 
</table> 
