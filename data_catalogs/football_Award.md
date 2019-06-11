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
    <td>winner_pic</td>
    <td>list</td>
    <td>.{3,3000}</td>
    <td>
    لینک عکس برنده(برندگان) جایزه
    </td>
  </tr>
 
 
  <tr>
    <td>winner_team</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    نام تیم برنده(برندگان) جایزه
    </td>
  </tr>
 
 
  <tr>
    <td>winner_N</td>
    <td>int</td>
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
    <td>second_pic</td>
    <td>list</td>
    <td>.{3,3000}</td>
    <td>
    لینک عکس نفر(نفرات) دوم
    </td>
  </tr>
 
 
 
  <tr>
    <td>second_team</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    نام تیم نفر(نفرات) دوم
    </td>
  </tr>
 
 
 
  <tr>
    <td>second_N</td>
    <td>int</td>
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
    <td>third_pic</td>
    <td>list</td>
    <td>.{3,3000}</td>
    <td>
    لینک عکس نفر(نفرات) سوم
    </td>
  </tr>
 
 
 
  <tr>
    <td>third_team</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    نام تیم نفر(نفرات) سوم
    </td>
  </tr>
 
 
  <tr>
    <td>third_N</td>
    <td>int</td>
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
 
 
  <tr>
    <td>top3</td>
    <td>list</td>
    <td>.{3,40}</td>
    <td>
    نام سه نفر برتر جایزه
    </td>
  </tr>
  
  
  
  <tr>
    <td>place</td>
    <td>string</td>
    <td>.{3,40}</td>
    <td>
    مراسم اهدای جایزه در چه شهری انجام شد
    </td>
  </tr>
  
  
  
  
  <tr>
    <td>pic</td>
    <td>string</td>
    <td>.{3,40000}</td>
    <td>
    مراسم اهدای جایزه در چه شهری انجام شد
    </td>
  </tr>
  
  
 
 
 
  <tr>
    <td>most1_win</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    رکورددار(ان) جایزه در تاریخ مثلا مسی در کفش طلا (که6بار برده)
    </td>
  </tr>
 
 
  <tr>
    <td>most1_win_pic</td>
    <td>list</td>
    <td>.{3,3000}</td>
    <td>
    لینک عکس رکورددار(ان) جایزه
    </td>
  </tr>
 
 
  <tr>
    <td>most1_win_team</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    نام تیم رکورددار(ان) جایزه
    </td>
  </tr>
 
 
  <tr>
    <td>most1_win_N</td>
    <td>int</td>
    <td>\d{1,4}</td>
    <td>
    تعداد رای(گل یا ...) رکورددار(ان) جایزه
    </td>
  </tr>
 
 
 
 
 
  <tr>
    <td>most2_win</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    نام رکورددار(ان) جایزه در رتبه دوم در تاریخ مثلا رونالدو در کفش طلا که 5 بار برده
    </td>
  </tr>
 
 
  <tr>
    <td>most2_win_pic</td>
    <td>list</td>
    <td>.{3,3000}</td>
    <td>
    لینک عکس رکورددار(ان) جایزه در رتبه دوم
    </td>
  </tr>
 
 
  <tr>
    <td>most2_win_team</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    نام تیم رکورددار(ان) جایزه در رتبه دوم
    </td>
  </tr>
 
 
  <tr>
    <td>most2_win_N</td>
    <td>int</td>
    <td>\d{1,4}</td>
    <td>
    تعداد رای(گل یا ...) رکورددار(ان) جایزه در رتبه دوم
    </td>
  </tr>
 
 
 
 
  <tr>
    <td>most3_win</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    نام رکورددار(ان) جایزه در رتبه سوم در تاریخ
    </td>
  </tr>
 
 
  <tr>
    <td>most3_win_pic</td>
    <td>list</td>
    <td>.{3,3000}</td>
    <td>
    لینک عکس رکورددار(ان) جایزه در رتبه سوم
    </td>
  </tr>
 
 
  <tr>
    <td>most3_win_team</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    نام تیم رکورددار(ان) جایزه در رتبه سوم
    </td>
  </tr>
 
 
  <tr>
    <td>most3_win_N</td>
    <td>int</td>
    <td>\d{1,4}</td>
    <td>
    تعداد رای(گل یا ...) رکورددار(ان) جایزه در رتبه سوم
    </td>
  </tr>
 
 
  <tr>
    <td>concept</td>
    <td>string</td>
    <td>.{1,20}</td>
    <td>
    مفهوم جایزه (انتخابی مثل بهترین بازیکن یا بیشترین گلزده و یا ...) به صورتی که برای قالب مشخص باشد که از این دیتا چه نوع سؤالی میتواند بسازد
    </td>
  </tr>
 
 
 
</table> 
