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
    نام کامل فیلم
    </td>
  </tr>
 
 
  <tr>
    <td>director</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    نام کارگردان (کارگردانان) فیلم
    </td>
  </tr>
 
 
  <tr>
    <td>cast</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    نام تمام بازیگران فیلم
    </td>
  </tr>


  <tr>
    <td>Producer</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
     نام تهیه کننده(کنندگان) فیلم 
    </td>
  </tr>


  <tr>
    <td>writer</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
     نام نویسنده(نویسندگان) فیلم 
    </td>
  </tr>



  <tr>
    <td>storyline</td>
    <td>string</td>
    <td>.{3,3000}</td>
    <td>
     خلاصه و خط داستانی 
    </td>
  </tr>



  <tr>
    <td>music</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
     آهنگساز 
    </td>
  </tr>
 
 
  <tr>
    <td>Cinematography</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
     فیلمبردار 
    </td>
  </tr>
 
 
  <tr>
    <td>edit</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
     تدوینگر 
    </td>
  </tr>
 
 
 
  <tr>
    <td>company</td>
    <td>string</td>
    <td>.{3,40}</td>
    <td>
     کمپانی(شرکت) تولیدکننده 
    </td>
  </tr>
 
 
 
 
  <tr>
    <td>distribute</td>
    <td>string</td>
    <td>.{3,50}</td>
    <td>
     توزیع کننده 
    </td>
  </tr>
 
 
  <tr>
    <td>release</td>
    <td>string</td>
    <td>====</td>
    <td>
     تاریخ اکران 
    </td>
  </tr>
 
 
  <tr>
    <td>time</td>
    <td>unsignint</td>
    <td>\d{2,3}</td>
    <td>
     زمان فیلم 
    </td>
  </tr>
 
 
  <tr>
    <td>country</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    کشور تولیدکننده فیلم 
    </td>
  </tr>
 
 
  <tr>
    <td>language</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    زبان فیلم 
    </td>
  </tr>
 
 
  <tr>
    <td>budget_on_dollar</td>
    <td>unsignint</td>
    <td>\d{1,10}</td>
    <td>
    بودجه ساخت فیلم 
    </td>
  </tr>
 
 
  <tr>
    <td>box_office_on_dollar</td>
    <td>unsignint</td>
    <td>\d{1,11}</td>
    <td>
    فروش باکس آفیس 
    </td>
  </tr>
 
 
 
 
  <tr>
    <td>box_office_on_dollar</td>
    <td>unsignint</td>
    <td>\d{1,11}</td>
    <td>
    فروش باکس آفیس 
    </td>
  </tr>
 
 </table>
