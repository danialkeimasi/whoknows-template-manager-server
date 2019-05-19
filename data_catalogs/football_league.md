 <table>
  <tr>
    <th>Field</th>
    <th>Type</th>
    <th>Regex</th>
    <th>Descereption</th>
  </tr>
 
  <tr>
    <td>club</td>
    <td>string</td>
    <td>.{2,30}</td>
    <td>
    نام کامل تیم
    </td>
  </tr>
 
  <tr>
    <td>logo</td>
    <td>string</td>
    <td>.{4,1000}</td>
    <td>
    لینک عکس لوگو تیم
    </td>
  </tr>

league |  string  | .{4,30} | نام لیگ

  <tr>
    <td>league</td>
    <td>string</td>
    <td>.{4,30}</td>
    <td>
    نام لیگ
    </td>
  </tr>


  <tr>
    <td>rank</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    رتبه تیم در جدول
    </td>
  </tr>

  <tr>
    <td>point</td>
    <td>unsignint</td>
    <td>\d{1,3}</td>
    <td>
    امتیاز تیم در جدول
    </td>
  </tr>

  <tr>
    <td>gf</td>
    <td>unsignint</td>
    <td>\d{1,3}</td>
    <td>
    تعداد گل زده تیم
    </td>
  </tr>

  <tr>
    <td>ga</td>
    <td>unsignint</td>
    <td>\d{1,3}</td>
    <td>
    تعداد گل خورده تیم در لیگ
    </td>
  </tr>
 
  <tr>
    <td>gd</td>
    <td>int</td>
    <td>\d{1,3}</td>
    <td>
    تفاضل گل خورده تیم در لیگ
    </td>
  </tr>

  <tr>
    <td>wins</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    تعداد بردهای تیم در لیگ
    </td>
  </tr>

  <tr>
    <td>losts</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    تعداد باخت های تیم در لیگ
    </td>
  </tr>
  
  <tr>
    <td>draws</td>
    <td>unsignint</td>
    <td>\d{1,3}</td>
    <td>
    تعداد مساوی های تیم در لیگ
    </td>
  </tr>


  <tr>
    <td>player</td>
    <td>string</td>
    <td>.{2,30}</td>
    <td>
    نام بازیکن در جدول گلزنان لیگ
    </td>
  </tr>

  <tr>
    <td>player_goal_rank</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    رتبه بازیکن در جدول گلزنان لیگ
    </td>
  </tr>

  <tr>
    <td>player_club</td>
    <td>string</td>
    <td>.{2,30}</td>
    <td>
    نام تیم بازیکن
    </td>
  </tr>

  <tr>
    <td>player_goals</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    تعداد گل های بازیکن در لیگ
    </td>
  </tr>


  <tr>
    <td>player_penalty_goals</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    تعداد گل های بازیکن از روی نقطه پنالتی در لیگ
    </td>
  </tr>


</table> 
