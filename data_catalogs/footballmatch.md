Field |  type   | Regex | Descereption
----- |---------|-------|--------------
home |  string  | .{2,30} | نام کامل تیم میزبان مانند FC Barcelona
away |  string  | .{2,30} | نام کامل تیم میهمان مانند FC Barcelona
home_logo |  string  | .{4,1000} | لینک عکس لوگو تیم
away_logo |  string  | .{4,1000} | لینک عکس لوگو تیم
competion |  string  | .{4,30} | نام لیگ و یا تورنمنت مثل Premier League یا UEFA Champions League
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

