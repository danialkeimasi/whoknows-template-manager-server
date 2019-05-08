Field |  type   | Regex | Descereption
----- |---------|-------|--------------
name |  string  | [\D]{3,20} | نام بازیکن ، که او را با آن نام میشناسند. مانند Lionel Messi , Hulk
club_team |  string  | .{2,20} | نام کامل تیم مانند FC Barcelona
club_number |  string  | [1-9][0-9] | شماره ی پیراهن بازیکن در تیم باشگاهی اش
nationality |  string  | [A-Z][A-Z a-z\(\)]{3,40} | ملیت بازیکن
national_team |  string  | [\D]{4,35} | ملیت بازیکن
height_in_cm |  int  | [1,2]\d\d | قد بازیکن به سانتی متر
age |  int  | [1,2,3,4][1-9] | سن بازیکن
foot |  string  | Left\|Right | پای تخصصی بازیکن (چپ یا راست) 
birth_date |  string  | \d{1,2}/\d{1,2}/[1,2][0,1,9]\d\d | تاریخ تولد بازیکن
photo_link |  string  | [a-z]{4,100} | لینک عکس بازیکن
release_clause |  int  | [\d]{3,10} | مبلغ فسخ قرارداد بازیکن به یورو
value_in_euro |  int  | [\d]{4,10} | ارزش بازیکن در سایت ترانسفرمارکت بازیکن به یورو
wage |  int  | [\d]{4,9} | حقوق هفتگی بازیکن به یورو
club_join_date |  string  | \d{1,2}/\d{1,2}/[1,2][0,1,9]\d\d | تاریخ پیوستن بازیکن به تیم باشگاهی اش
contract_valid_until |  string  | [1,2][0,1,9]\d\d | سال اتمام قرارداد بازیکن با تیم