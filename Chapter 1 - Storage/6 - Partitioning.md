# Data Partitioning :

## Overview
This session isolates the concept of data partitioning. Rather than bundle it with Hive or other systems, we’ll treat partitioning as a fundamental data modeling and storage optimization technique. Expect five deep questions that cover motivation, strategies, pruning, bucketing, and real-world considerations.

**The focus is on understanding why and how data is partitioned across storage systems.**

## Goals
- Learn what partitioning means in the context of databases and data lakes.
- Explore different partitioning strategies and their trade-offs.
- Examine how partitioning interacts with query optimization and maintenance.

:warning: **Note:**
- This day is strictly theoretical; no specific software or engines are required.
- Discuss unclear points with your mentor.

### ⏳ Timeline
Estimated Duration: 0.5 Days
- Day 1: Learn what partitioning is and the core concepts; spend half a day.
    - Have a Q&A session the same day

## Core Questions

1. **Motivation & Definitions:** What problems does partitioning solve? Distinguish between horizontal and vertical partitioning, and between logical and physical partitions.

הpartitioning זה הפעולה של חלוקת טבלה לסקשנים קטנים יותר שקל לנהל.
במאגרי מידע עם כמויות מאוד גדולות של נתונים הטבלאות יכולות לגדול בצורה משמעותית ולהפוך את כל הפעולות והגישה אליהן למאוד כבדות ולא יעילות, הpartitioning פותר את זה ובעזרתו אין לנו צורך לסרוק טבלה ענקית שלמה כדי לחפש נתון ואין לנו צורך לטעון כל פעם את כל הטבלה.
יש 2 שיטות partition :
- אנכי - חלוקת הטבלה לפי עמודות , שמיש כנרצה ליצור הפרדות לפי סוגי תכונות (מזכיר column families).
- אופקי - חלוקה לפי שורות - מתחלק לrange, list, hash, composite ועוד סוגי חלוקה.
יש גם 2 סוגים של partition :
- לוגי - הפרדה של הטבלה עצמה באופן לוגי כלומר בחירת שורות או עמודות והפרדה שלהם לחלקים, נועד כדי לשפר ביצועי מערכת ולהקל.
- פיזי - ממש הפרדה של אותם חלקים ושמירה נפרדת שלהם באחסון, כלומר אין טבלה אחת גדולה שומרים רק פרטישנים שלה.
 

2. **Strategies:** Describe common partitioning techniques (range, list, hash, composite) and when each is appropriate. Include considerations for time-series data.

פרטישן אופקי מתחלק לכמה סוגים:
- פרטישן range : מחלקים את הטבלה לפי תחום ערכים של שורות לדוגמה שורות 0-500 בפרטישן אחד וכו.. טוב נגיד למידע עם timestamp אם רוצים לחלק לזמנים.
- פרטישן list : מחלקים לפי סט תכונות מסויים, נגיד בpartition אחד כל השורות בהם X=ערך מסויים.
- פרטישן hash : פרטישן שמשתמשים בו כשאין תחום או תכונות מסויימות, מפעילים פונקציית hash על שורות ומתאימים לפי ערך הhash של שורה את הpartition בה תהיה, זה יוצר באלאנס.
- פרטישן composite : שילוב של שיטות פרטישן, לדוגמה range ביחד עם list. 

3. **Pruning & Optimization:** Explain how partition pruning works and why it’s critical for performance. How do query planners determine which partitions to scan?

הpartition pruning זה שיטה לייעול שאילתות SQL על הטבלה בכך שמזהים מאיפה ולאן השאילתה ומתעלמים בpartitions שאינם רלוונטים. ככה מפחיתים I/O , מייעלים שאילתות והופכים שליפות למהירות יותר.
לדוגמה אם ביקשו נתון מ2023 ויש פרטישנים לפי שנים, נתעלם מכל הפרטישנים שאינם של השנה 2023 או בטווח הזה.
סורקים רק partitions שרלוונטים לנתון.
בפרטישן סטטי צריך לדעת בזמן הקומפילציה איזה תכונות של פרטישנים צריך לסנן, כלומר יש תנאי סינון מוגדר מראש, בעוד שבפרטישן דינאמי זה בזמן ריצה, כלומר הquery optimizer אחראי לשים לב לסינון האפשרי.

4. **Maintenance & Evolution:** What challenges arise when partitions grow or have inconsistent metadata? Discuss operations like adding, dropping, or merging partitions.

ברגע שיש גדילה משמעותית בפרטישנים, או הרבה סוגים שונים של מטא-דאטה ואין עקביות. נוצר בעיה בליצור פרטישן או בניהול הפרטישנים הקיימים.
יכול להיות שהנתונים כלליים ושונים מדיי ואין תכונות לסדר אותם לפיהם כי אז יש יותר מדי פרטישנים, או שיש כל כך הרבה מידע שהתחומים או פרטישנים אחריי פונקציות האש לא עומדים בכמויות עדיין.
לדוגמה, אם הפרטישנים מסודרים לפי זמן, יכול להיות שנרצה למחוק פרטישן שהוא ישן מדיי לפי תוקף מסויים.
אם נוספו מלא נתונים חדשים או שנוספים באופן קבוע, יכול להיות שנצטרך להוסיף פרטישנים באופן אוטומטי, זה קורה במיוחד בrange partition או פרטישנים שקורים לפי זמן.
לפעמים כשיש הרבה תכונות ונוצרים הרבה partitionings נרצה לאחד פרטישנים קטנים יותר לפרטישן אחד משותף, נעשה זאת ואז המקוריים ימחקו (צריך לדאוג לגיבוי קודם).

5. **Bucketing & Data Layout:** What is bucketing, and how does it differ from partitioning? When is bucketing useful (e.g., joins, load balancing, reducing shuffle)? How can bucketing complement partitioning in large datasets?

הbucketing זה החלוקה של הנתונים בתוך הפרטישנים עצמם לbuckets, בניגוד לpartitioning לא מחלקים את הטבלה לפי ערכים או טווח אלא מחלקים את הפרטישן עצמו לפי שורה או עמודה ובניגוד לpartitioning יש מספר מוגבל של Buckets שקובעים מראש, זה לא משהו דינאמי שנקבע לפי טווח וגדל עוד.
הבאקטינג שונה מפרטישנינג כי הוא בעצם תהליך בתוך הפרטישנינג, בתוך כל פרטישן מגדירים מספר קבוע מראש של buckets ומחלקים את הנתונים לאותם באקטס, כל קבוצת נתונים ישמרו באותו קובץ.
בניגוד לpartitioning שנועד כדי להפחית עומסים ולייעל פעולות קריאה, הבאקטינג נועד להקל על JOINS, ליצור איזון בשמירת הנתונים ולהפחית skewness (הסתברות לא סימטרית/ לא מאוזנת) כי הוא מונע hot spots.
הbucketing הוא תנאי הכרחי לתמיכה בACID שלא כמו פרטישנינג.
זה יוצר קבצים מאוזנים והרבה פעמים נעשה בעזרת hash.
במה זה עוזר?
- בJOIN במקום לסרוק כל שורה אפשר פשוט לעשות JOIN לbuckets זהים.
- אפשר לעשות bucketing לשני טבלאות על אותו מפתח, בתנאי שיש אותו מספר buckets מה שחוסף העברות (העברה של המידע פיזית הוא מאוד יקר)
- במתודות באקטינג כמו האש העבודה מתחלקת שווה בין שווה בין הבאקטים.

## Wrapping Up :trophy:
Review your answers with your mentor and identify scenarios where partitioning could dramatically improve or hurt a workload.

## Action Items
- Identify storage systems you want to try partitioning in (e.g., Hive, Iceberg, PostgreSQL).
- Prepare questions for the next mentor Q&A.
