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
    <td>.{3,20}</td>
    <td>
    نام کامل تیم
    </td>
  </tr>
 
 
  <tr>
    <td>league</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    لیگی که تیم در آن حضور دارد
    </td>
  </tr>
 
 
  <tr>
    <td>coach</td>
    <td>string</td>
    <td>\D{3,20}</td>
    <td>
    نام مربی تیم
    </td>
  </tr>
 
 
  <tr>
    <td>country</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    نام کشوری که تیم متعلق به آن است
    </td>
  </tr>
 
 
  <tr>
    <td>captain</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    نام کاپیتان تیم
    </td>
  </tr>
 
 
  <tr>
    <td>stadium</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    نام استادیوم تیم
    </td>
  </tr>
 
 
  <tr>
    <td>homekit</td>
    <td>string</td>
    <td>.{3,200}</td>
    <td>
    لینک عکس پیراهن اول تیم
    </td>
  </tr>
 
 
  <tr>
    <td>awaykit</td>
    <td>string</td>
    <td>.{3,200}</td>
    <td>
    لینک عکس پیراهن دوم تیم
    </td>
  </tr>
 
 
  <tr>
    <td>thirdkit</td>
    <td>string</td>
    <td>.{3,200}</td>
    <td>
    لینک عکس پیراهن سوم تیم 
    </td>
  </tr>
 
 
  <tr>
    <td>gkkit</td>
    <td>string</td>
    <td>.{3,200}</td>
    <td>
    لینک عکس پیراهن دروازه بان تیم
    </td>
  </tr>
 
 
  <tr>
    <td>logo</td>
    <td>string</td>
    <td>.{3,200}</td>
    <td>
    لینک عکس لوگو تیم
    </td>
  </tr>
 
 
  <tr>
    <td>founded</td>
    <td>unsignint</td>
    <td>\d{4}</td>
    <td>
    تاریخ تاسیس باشگاه
    </td>
  </tr>
 
 
  <tr>
    <td>rival</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    نام تیم رقیب سنتی
    </td>
  </tr>
 
 <tr>
    <td>players</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    اسامی بازیکنان تیم
    </td>
  </tr>
 
 <tr>
    <td>players_on_loan</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    اسامی بازیکنان تیم که به تیم دیگری قرض داده شده اند
    </td>
  </tr>
 
 <tr>
    <td>loan_players</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    بازیکنان قرضی تیم _ بازیکنانی که بصورت قرضی برای تیم بازی میکنند
    </td>
  </tr>
 
 
 
 
</table> 
