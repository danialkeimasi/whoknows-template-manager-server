Field |  type   | Regex | Descereption
----- |---------|-------|--------------
club |  string  | .{2,20} | نام کامل تیم مانند FC Barcelona
logo |  string  | .{4,1000} | لینک عکس لوگو تیم
league |  string  | .{4,30} | نام لیگ
rank |  string  | \d{1,2} | رتبه تیم در جدول
point |  string  | \d{1,3} | امتیاز تیم در جدول
gf |  string  | [\d]{1,2} | تعداد گل زده تیم
ga |  string  | [\d]{1,2} | تعداد گل خورده تیم
gd |  string  | [\d]{1,2} | تعداد گل خورده تیم
wins |  string  | [\d]{1,2} | تعداد برد تیم
losts |  string  | [\d]{1,2} | تعداد باخت تیم
draws |  string  | [\d]{1,2} | تعداد مساوی تیم
