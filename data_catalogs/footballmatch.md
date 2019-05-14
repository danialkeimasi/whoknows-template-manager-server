<table>
  <tr>
    <th>Field</th>
    <th>Type</th>
    <th>Regex</th>
    <th>Descereption</th>
  </tr>
 
  <tr>
    <td>home</td>
    <td>string</td>
    <td>.{2,30}</td>
    <td>
    نام کامل تیم میزبان مانند FC Barcelona
    </td>
  </tr>
 
  <tr>
    <td>away</td>
    <td>string</td>
    <td>.{2,30}</td>
    <td>
    نام کامل تیم میزبان مانند FC Barcelona
    </td>
  </tr>


  <tr>
    <td>home_logo</td>
    <td>string</td>
    <td>.{4,1000}</td>
    <td>
    لینک عکس لوگو تیم میزبان
    </td>
  </tr>

  <tr>
    <td>away_logo</td>
    <td>string</td>
    <td>.{4,1000}</td>
    <td>
    لینک عکس لوگو تیم میهمان
    </td>
  </tr>




  <tr>
    <td>competion</td>
    <td>string</td>
    <td>.{4,30}</td>
    <td>
    نام لیگ و یا تورنمنت مثل Premier League یا UEFA Champions League
    </td>
  </tr>

  <tr>
    <td>game_week</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    شماره ی هفته ی بازی در لیگ
    </td>
  </tr>

  <tr>
    <td>half_time_scores</td>
    <td>string</td>
    <td>\d{1,2}\-\d{1,2}</td>
    <td>
    نتیجه مسابقه در نیمه اول بصورت 2-1 
    </td>
  </tr>
  
  
  <tr>
    <td>scores</td>
    <td>string</td>
    <td>\d{1,2}\-\d{1,2}</td>
    <td>
    نتیجه مسابقه بصورت 2-1 
    </td>
  </tr>

  <tr>
    <td>stadium</td>
    <td>string</td>
    <td>.{30}</td>
    <td>
    استادیومی که مسابقه در آن برگزار شده است
    </td>
  </tr>
 
  <tr>
    <td>attendance</td>
    <td>unsignint</td>
    <td>\d{1,6}</td>
    <td>
    تعداد تماشاگران حاضر در استادیوم
    </td>
  </tr>
  
  
</table> 
