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
  
  
  <tr>
    <td>home_coach</td>
    <td>string</td>
    <td>\D{3,20}</td>
    <td>
    نام مربی تیم میزبان
    </td>
  </tr>
  
  <tr>
    <td>away_coach</td>
    <td>string</td>
    <td>\D{3,20}</td>
    <td>
    نام مربی تیم میهمان
    </td>
  </tr>
  
  <tr>
    <td>ref</td>
    <td>string</td>
    <td>[A-Z .a-z]{1,25}</td>
    <td>
    نام داور وسط بازی
    </td>
  </tr>
  
  <tr>
    <td>assistants</td>
    <td>list</td>
    <td>[A-Z .a-z]{1,25}</td>
    <td>
    نام کمک داوران اول و دوم
    </td>
  </tr>
  
  
  <tr>
    <td>fourth_ref</td>
    <td>list</td>
    <td>[A-Z .a-z]{1,25}</td>
    <td>
    نام داور چهارم بازی
    </td>
  </tr>
  
  <tr>
    <td>home_corners</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    تعداد کرنر تیم میزبان
    </td>
  </tr>
  
  <tr>
    <td>away_corners</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    تعداد کرنر تیم میهمان
    </td>
  </tr>
  
   <tr>
    <td>home_shots</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    تعداد شوت تیم میزبان
    </td>
  </tr>
  
  <tr>
    <td>away_shots</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    تعداد شوت تیم میهمان
    </td>
  </tr>
  
  <tr>
    <td>home_shots_on_target</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    تعداد شوت در چارچوب تیم میزبان
    </td>
  </tr>
  
  <tr>
    <td>away_shots_on_target</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    تعداد شوت در چارچوب تیم میهمان
    </td>
  </tr>
  
  <tr>
    <td>home_fouls</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    تعداد خطای تیم میزبان
    </td>
  </tr>
  
  <tr>
    <td>away_fouls</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    تعداد خطای تیم میهمان
    </td>
  </tr>
  
  
  <tr>
    <td>home_offside</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    تعداد آفساید تیم میزبان
    </td>
  </tr>
  
  <tr>
    <td>away_offside</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    تعداد آفساید تیم میهمان
    </td>
  </tr>
  
  
  <tr>
    <td>home_lineups</td>
    <td>list</td>
    <td>\D{3,20}</td>
    <td>
    11 نغر اولیه تیم میزبان
    </td>
  </tr>
  
  <tr>
    <td>away_lineups</td>
    <td>list</td>
    <td>\D{3,20}</td>
    <td>
    11 نفر اولیه تیم میهمان
    </td>
  </tr>
  
  
  <tr>
    <td>home_subs</td>
    <td>list</td>
    <td>\D{3,20}</td>
    <td>
    لیست بازیکنان ذخیره تیم میزبان
    </td>
  </tr>
  
  <tr>
    <td>away_subs</td>
    <td>list</td>
    <td>\D{3,20}</td>
    <td>
    لیست بازیکنان ذخیره تیم میهمان
    </td>
  </tr>
  
  <tr>
    <td>home_subs_in</td>
    <td>list</td>
    <td>\D{3,20}</td>
    <td>
    لیست بازیکنان ذخیره ورودی (تعویض شده) تیم میزبان
    </td>
  </tr>
  
  <tr>
    <td>away_subs_in</td>
    <td>list</td>
    <td>\D{3,20}</td>
    <td>
    لیست بازیکنان ذخیره ورودی (تعویض شده) تیم میهمان
    </td>
  </tr>
  
  
  <tr>
    <td>home_subs_out</td>
    <td>list</td>
    <td>\D{3,20}</td>
    <td>
    لیست بازیکنان خروجی (تعویض شده) تیم میزبان
    </td>
  </tr>
  
  <tr>
    <td>away_subs_out</td>
    <td>list</td>
    <td>\D{3,20}</td>
    <td>
    لیست بازیکنان خروجی (تعویض شده) تیم میهمان
    </td>
  </tr>
  
  
  
  
  
</table> 
