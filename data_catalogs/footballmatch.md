Field |  type   | Regex | Descereption
----- |---------|-------|--------------
home |  string  | .{2,30} | نام کامل تیم میزبان مانند FC Barcelona
away |  string  | .{2,30} | نام کامل تیم میهمان مانند FC Barcelona
home_logo |  string  | .{4,1000} | لینک عکس لوگو تیم
away_logo |  string  | .{4,1000} | لینک عکس لوگو تیم
competion |  string  | .{4,30} | نام لیگ و یا تورنمنت مثل Premier League یا UEFA Champions League
game_week



date |  string  | \d{1,2} | رتبه تیم در جدول
point |  unsignint  | \d{1,3} | امتیاز تیم در جدول
gf |  unsignint  | [\d]{1,2,3} | تعداد گل زده تیم
ga |  unsignint  | [\d]{1,2} | تعداد گل خورده تیم
gd |  int  | [\d]{1,2,3} | تفاضل گل تیم
wins |  unsignint  | [\d]{1,2} | تعداد برد تیم
losts |  unsignint  | [\d]{1,2} | تعداد باخت تیم
draws |  unsignint  | [\d]{1,2} | تعداد مساوی تیم
player |  string  | [\D]{3,20} | نام بازیکن در جدول گلزنان
player_goal_rank |  unsignint  | [\d]{1,2} | رتبه در جدول گلزنان لیگ
player_club |  string  | .{2,30} | نام تیم بازیکن در جدول گلزنان
player_goals |  unsignint  | [\d]{1,2} | تعداد گلهای بازیکن در این فصل در لیگ
player_penalty_goals |  unsignint  | [\d]{1,2} | تعداد گلهای بازیکن از روی نقطه پنالتی در این فصل لیگ

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
    <td>height_in_cm</td>
    <td>unsignint</td>
    <td>[1,2]\d\d</td>
    <td>
    قد بازیکن به سانتی متر
    </td>
  </tr>

  <tr>
    <td>age</td>
    <td>unsignint</td>
    <td>[1,2,3,4,5][0-9]</td>
    <td>
    سن بازیکن
    </td>
  </tr>
 
  <tr>
    <td>foot</td>
    <td>string</td>
    <td>Left|Right</td>
    <td>
    پای تخصصی بازیکن (چپ یا راست)
    </td>
  </tr>
  
  <tr>
    <td>birth_date</td>
    <td>string</td>
    <td>[1,2][0,9]\d\d/\d{1,2}/\d{1,2}</td>
    <td>
    تاریخ تولد بازیکن
    </td>
  </tr>

  <tr>
    <td>photo_link</td>
    <td>string</td>
    <td>.{4,100}</td>
    <td>
    لینک عکس بازیکن
    </td>
  </tr>
  
  <tr>
    <td>release_clause_euro</td>
    <td>unsignint</td>
    <td>[\d]{3,10}</td>
    <td>
    مبلغ فسخ قرارداد بازیکن به یورو
    </td>
  </tr>

  <tr>
    <td>value_in_euro</td>
    <td>unsignint</td>
    <td>[\d]{4,10}</td>
    <td>
    ارزش بازیکن در سایت ترانسفرمارکت به یورو
    </td>
  </tr>

  <tr>
    <td>wage_euro</td>
    <td>unsignint</td>
    <td>[\d]{4,9}</td>
    <td>
    حقوق هفتگی بازیکن به یورو
    </td>
  </tr>

  <tr>
    <td>club_join_date</td>
    <td>string</td>
    <td>[1,2][0,9]\d\d/\d{1,2}/\d{1,2}</td>
    <td>
    تاریخ پیوستن بازیکن به تیم باشگاهی اش
    </td>
  </tr>

  <tr>
    <td>contract_valid_until</td>
    <td>string</td>
    <td>[1,2][0,9]\d\d</td>
    <td>
    سال اتمام قرارداد بازیکن با تیم
    </td>
  </tr>

</table> 
