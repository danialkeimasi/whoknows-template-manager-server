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
    <td>genre</td>
    <td>list</td>
    <td>.{3,20}</td>
    <td>
    ژانرهای فیلم
    </td>
  </tr>
 
 
  <tr>
    <td>ages</td>
    <td>string</td>
    <td>.{3,10}</td>
    <td>
    رده سنی فیلم مانند PG-13
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
    <td>based_on</td>
    <td>string</td>
    <td>.{3,60}</td>
    <td>
     برگرفته از (یعنی فیلم از چه کتاب یا ... اقتباس شده است) 
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
    <td>box_office_usa_on_dollar</td>
    <td>unsignint</td>
    <td>\d{1,11}</td>
    <td>
    فروش باکس آفیس 
    </td>
  </tr>
 
 
  <tr>
    <td>opening_weekend_on_dollar</td>
    <td>unsignint</td>
    <td>\d{1,11}</td>
    <td>
    فروش افتتاحیه آخر هفته باکس آفیس 
    </td>
  </tr>
 
 
  <tr>
    <td>color</td>
    <td>string</td>
    <td>.{1,15}</td>
    <td>
    وضعیت رنگ فیلم (رنگی یا سیاه و سفید) 
    </td>
  </tr>
 
 
 
  <tr>
    <td>key_words</td>
    <td>list</td>
    <td>.{1,20}</td>
    <td>
    کلمات کلیدی مرتبط با فیلم 
    </td>
  </tr>
 
 
  <tr>
    <td>tagline</td>
    <td>string</td>
    <td>.{1,100}</td>
    <td>
    برچسب های فیلم بصورت جمله 
    </td>
  </tr>
 
 
 
 
  <tr>
    <td>also_known_as</td>
    <td>list</td>
    <td>.{1,50}</td>
    <td>
    نام های دیگر فیلم در سایر کشورها 
    </td>
  </tr>
 
 
 
  <tr>
    <td>quote</td>
    <td>string</td>
    <td>.{1,1000}</td>
    <td>
    دیالوگ های معروف فیلم 
    </td>
  </tr>
 
 
 
 
 </table>
