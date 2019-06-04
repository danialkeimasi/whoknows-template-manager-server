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
    نام بازیکن ، که او را با آن نام میشناسند. مانند Lionel Messi , Hulk
    </td>
  </tr>
 
  <tr>
    <td>club_team</td>
    <td>string</td>
    <td>.{2,20}</td>
    <td>
    نام کامل تیم مانند FC Barcelona
    </td>
  </tr>

  <tr>
    <td>club_number</td>
    <td>string</td>
    <td>[1-9][0-9]{0,1}</td>
    <td>
    شماره ی پیراهن بازیکن در تیم باشگاهی اش
    </td>
  </tr>

  <tr>
    <td>nationality</td>
    <td>string</td>
    <td>[A-Z][A-Z a-z\(\)-,]{3,40}</td>
    <td>
    ملیت بازیکن
    </td>
  </tr>

  <tr>
    <td>national_team</td>
    <td>string</td>
    <td>[\D]{4,35}</td>
    <td>
    تیم ملی بازیکن
    </td>
  </tr>


  <tr>
    <td>national_number</td>
    <td>string</td>
    <td>[1-9][0-9]{0,1}</td>
    <td>
    شماره ی پیراهن بازیکن در تیم ملی اش
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
