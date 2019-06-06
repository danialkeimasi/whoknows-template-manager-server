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
    نام کامل مسابقه بدون سال
    </td>
  </tr>
 
 
  <tr>
    <td>champ</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    اسم تیم قهرمان
    </td>
  </tr>
 
 
  <tr>
    <td>second_place</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    نام تیم دوم مسابقات
    </td>
  </tr>
 
 
  <tr>
    <td>third_place</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    نام تیم سوم مسابقات
    </td>
  </tr>
 
 
  <tr>
    <td>fourth_place</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    نام تیم چهارم مسابقات
    </td>
  </tr>
 
 
  <tr>
    <td>champ_coach</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    نام سرمربی تیم قهرمان
    </td>
  </tr>
 
 
  <tr>
    <td>second_place_coach</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    نام سرمربی تیم دوم مسابقات
    </td>
  </tr>
 
 
  <tr>
    <td>third_place_coach</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    نام سرمربی تیم سوم مسابقات
    </td>
  </tr>
 
 
  <tr>
    <td>fourth_place_coach</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    نام سرمربی تیم چهارم مسابقات
    </td>
  </tr>
 
 
  <tr>
    <td>captain</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    نام کاپیتان تیم قهرمان
    </td>
  </tr>
 
 
  <tr>
    <td>cup_pic</td>
    <td>string</td>
    <td>.{3,3000}</td>
    <td>
    لینک عکس کاپ مسابقات
    </td>
  </tr>
 
 
  <tr>
    <td>logo</td>
    <td>string</td>
    <td>.{3,2000}</td>
    <td>
    لینک عکس لوگو مسابقات
    </td>
  </tr>
 
 
  <tr>
    <td>number_of_teams</td>
    <td>unsignint</td>
    <td>\d\d{1,2}</td>
    <td>
    تعداد تیمهای شرکت کننده در مسابقات
    </td>
  </tr>
 
 
  <tr>
    <td>all_teams</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    اسم تمامی تیم های شرکت کننده در مسابقات بصورت لیست 
    </td>
  </tr>
 
 
  <tr>
    <td>top_16</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    اسم تیمهای راه یافته به 16 تیم نهایی
    </td>
  </tr>
 
 
  <tr>
    <td>top_8</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    اسامی تیمهای راه یافته به 8 تیم برتر
    </td>
  </tr>
 
 
  <tr>
    <td>top_4</td>
    <td>list</td>
    <td>.{1,30}</td>
    <td>
    اسم تیمهای راه یافته به 4 تیم برتر
    </td>
  </tr>
 
 
  <tr>
    <td>top_2</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    تیم های راه یافته به مرحله پایانی
    </td>
  </tr>
 
 <tr>
    <td>year</td>
    <td>unsignint</td>
    <td>\d{4}</td>
    <td>
    سال برگزاری مسابقه
    </td>
  </tr>
 
 <tr>
    <td>ball</td>
    <td>string</td>
    <td>.{3,3000}</td>
    <td>
    لینک عکس توپ جام
    </td>
  </tr>
 
 <tr>
    <td>song</td>
    <td>string</td>
    <td>.{3,3000}</td>
    <td>
    لینک آهنگ رسمی جام
    </td>
  </tr>
 
 
 
  <tr>
    <td>top_scorer</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    آقای گل مسابقات
    </td>
  </tr>
 
 <tr>
    <td>top_scorer_goals</td>
    <td>unsignint</td>
    <td>\d{1,2}</td>
    <td>
    تعداد گلهای آقای گل
    </td>
  </tr>
 
 <tr>
    <td>top_assist</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    اسم بهترین پاسور مسابقات
    </td>
  </tr>
 
 <tr>
    <td>best_gk</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    بهترین دروازه بان مسابقات
    </td>
  </tr>
 
 
  <tr>
    <td>best_player</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    بهترین بازیکن مسابقات
    </td>
  </tr>
 
 <tr>
    <td>final_result</td>
    <td>string</td>
    <td>.{3,47}</td>
    <td>
    نتیجه مسابقه فینال 
    </td>
  </tr>
  
  
  
 <tr>
    <td>final_stadium</td>
    <td>string</td>
    <td>.{3,47}</td>
    <td>
    استادیوم مسابقه فینال 
    </td>
  </tr>
  
  
  
  
 <tr>
    <td>final_ref</td>
    <td>string</td>
    <td>.{3,27}</td>
    <td>
    داور مسابقه فینال 
    </td>
  </tr>
  
  
  
  
 <tr>
    <td>play_off</td>
    <td>string</td>
    <td>.{3,47}</td>
    <td>
    تیمهای مسابقه رده بندی 
    </td>
  </tr>
  
  
 <tr>
    <td>play_off_result</td>
    <td>string</td>
    <td>.{3,47}</td>
    <td>
    نتیجه مسابقه رده بندی 
    </td>
  </tr>
  
  
  
 <tr>
    <td>play_off_stadium</td>
    <td>string</td>
    <td>.{3,47}</td>
    <td>
    استادیوم مسابقه رده بندی 
    </td>
  </tr>
  
  
  
  
 <tr>
    <td>play_off_ref</td>
    <td>string</td>
    <td>.{3,27}</td>
    <td>
    داور مسابقه رده بندی 
    </td>
  </tr>
  
  
 
 <tr>
    <td>first_semifinal</td>
    <td>string</td>
    <td>.{3,47}</td>
    <td>
    تیمهای اولین مسابقه نیمه نهایی 
    </td>
  </tr>
  
  
 <tr>
    <td>first_semifinal_result</td>
    <td>string</td>
    <td>.{3,47}</td>
    <td>
    نتیجه اولین مسابقه نیمه نهایی 
    </td>
  </tr>
  
 
 
 <tr>
    <td>first_semifinal_stadium</td>
    <td>string</td>
    <td>.{3,47}</td>
    <td>
    استادیوم اولین مسابقه نیمه نهایی 
    </td>
  </tr>
  
  
  
  
 <tr>
    <td>first_semifinal_ref</td>
    <td>string</td>
    <td>.{3,27}</td>
    <td>
    داور مسابقه اولین نیمه نهایی 
    </td>
  </tr>
  
 
 
  
 <tr>
    <td>second_semifinal</td>
    <td>string</td>
    <td>.{3,47}</td>
    <td>
    تیمهای دومین مسابقه نیمه نهایی 
    </td>
  </tr>
  
  
 <tr>
    <td>secon_semifinal_result</td>
    <td>string</td>
    <td>.{3,47}</td>
    <td>
    نتیجه دومین مسابقه نیمه نهایی 
    </td>
  </tr>
  
  
 
 <tr>
    <td>second_semifinal_stadium</td>
    <td>string</td>
    <td>.{3,47}</td>
    <td>
    استادیوم دومین مسابقه نیمه نهایی 
    </td>
  </tr>
  
  
  
  
 <tr>
    <td>second_semifinal_ref</td>
    <td>string</td>
    <td>.{3,27}</td>
    <td>
    داور مسابقه دومین نیمه نهایی 
    </td>
  </tr>
  
  
  
  
 
 <tr>
    <td>top_11</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    اسامی 11 نفر تیم منتخب جام
    </td>
  </tr>
 
 
 <tr>
    <td>group_A</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    تیمهای حاضر در گروه A
    </td>
  </tr>
 
 
 <tr>
    <td>group_B</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    تیمهای حاضر در گروه B
    </td>
  </tr>
 
 
 <tr>
    <td>group_C</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    تیمهای حاضر در گروه C
    </td>
  </tr>
 
 
 <tr>
    <td>group_D</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    تیمهای حاضر در گروه D
    </td>
  </tr>
 
 
 <tr>
    <td>group_E</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    تیمهای حاضر در گروه E
    </td>
  </tr>
 
 
 <tr>
    <td>group_F</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    تیمهای حاضر در گروه F
    </td>
  </tr>
 
 
 <tr>
    <td>group_G</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    تیمهای حاضر در گروه G
    </td>
  </tr>
 
 
 <tr>
    <td>group_H</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    تیمهای حاضر در گروه H
    </td>
  </tr>
 
 
 <tr>
    <td>group_I</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    تیمهای حاضر در گروه I
    </td>
  </tr>
 
 
 <tr>
    <td>group_J</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    تیمهای حاضر در گروه J
    </td>
  </tr>
 
 
 <tr>
    <td>group_K</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    تیمهای حاضر در گروه K
    </td>
  </tr>
 
 
 <tr>
    <td>group_L</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    تیمهای حاضر در گروه L
    </td>
  </tr>
 
 
 
  <tr>
    <td>number_of_matches</td>
    <td>unsignint</td>
    <td>.{3,30}</td>
    <td>
    تعداد کل بازی های این جام
    </td>
  </tr>
 
 <tr>
    <td>number_of_goals</td>
    <td>unsignint</td>
    <td>\d{1,3}</td>
    <td>
    تعداد گلها در کل جام
    </td>
  </tr>
 
 <tr>
    <td>best_young_player</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    اسم بهترین بازیکن جوان
    </td>
  </tr>
 
 <tr>
    <td>fair_play</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    اسم تیم(های) برنده جایزه بازی جوانمردانه
    </td>
  </tr>
 
 
 
 <tr>
    <td>host_country</td>
    <td>list</td>
    <td>.{3,30}</td>
    <td>
    اسم کشور(های) میزبان
    </td>
  </tr>
 
 
 <tr>
    <td>final_city</td>
    <td>string</td>
    <td>.{3,30}</td>
    <td>
    اسم شهر میزبان فینال مسابقات
    </td>
  </tr>
 
 
 
 <tr>
    <td>dates</td>
    <td>string</td>
    <td>.{8,40}</td>
    <td>
    تاریخ دوره برگزاری مسابقات (شروع و پایان)
    </td>
  </tr>
 
 
 
 
 
</table> 
