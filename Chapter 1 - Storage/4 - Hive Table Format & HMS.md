# Hive Metastore & Table Format :

## Overview
Today’s session zeroes in on two foundational pieces of Hive: the metastore that holds metadata and the table formats that define how data is structured on disk. We will avoid any discussion of Hive’s execution engines (MapReduce, Tez, etc.) or query processing. The goal is to understand the storage and metadata layers that other tools in the ecosystem rely on.

**Focus only on metadata management and table/format semantics.**

## Goals
- Understand what the Hive Metastore is and why it exists.
- Learn how Hive tables are defined and how formats describe their physical layout.
- Practice self-directed study and time management.

:warning: **Note:**
- Independence is essential; plan your study day accordingly.
- If you can’t explain a concept clearly, revisit the documentation.
- Review the [Exercise](#exercise) before diving into research.
- Ask your mentor for clarification on scope if needed.

### ⏳ Timeline
Estimated Duration: 1 Day
- Day 1: Learn the concepts of Hive both metastore and table format; spend the day.
    - Have a Q&A session the same day

## Hive Metastore

Answer the following questions to explore the metastore:

1. **Purpose & Function:**  What is the Hive Metastore and what types of metadata does it store (databases, tables, columns, partitions, locations, statistics)? Why is a centralized metadata service necessary in a distributed data platform?

הapache hive הוא data warehouse שבנוי על האדופ במטרה לתת כלי לשאילתות ולניתוח בצורה דומת SQL למידע שמאוחסן בדאטה בייסים שונים (HQL).
הmetastore זה כלי שמאחסן את כל המטא דאטה של Hive שנחלקת בין כלים שונים כמו spark, trino...
הapache hive מחולק לכמה חלקים -  הmetastore שמורכבת מהדאטה בייס (דאטה בייס רלציוני כמו postgreSQL / oracle / mySQL) שמאחסן בפועל את המטא דאטה, הhive tables שמאחסנים רפרנסים לקבצים שבHDFS בפורמט טבלאי ומהמנוע עיבוד שמכיל את  הhive server שמאפשר תקשורת מול הלקוח. 
הmetastore שומר מיקומי טבלאות, שמות טבלאות, שמות עמודות, partitions ועוד..
לכל metastore יש דאטה בייס אחד המורכב מכמה טבלאות, השימוש בדאטה בייס אחד מאפשר אמת אחת מוסכמת לכל הכלים שניגשים למטא דאטה, ומהווה מקור אחד לחיפוש מיקומים כך שאין צורך בעוד טבלאות מעליו.


2. **Architecture & Backend:**  Describe how the metastore is implemented as a standalone service backed by a relational database. What are common backend databases, and how does the service scale and handle concurrent clients?

הmetastore לא תלויה בhive, ניתן לעשות בה שימוש גם בלי התקנה שלו כל עוד יש דאטה בייס רלציוני חיצוני שהוא תומך בJDBC driver כדי לאפשר תקשורת מול הלקוח.
ההתקנה שלו כstandalone תתבצע בעזרת קוברנטיס או דוקר.
הדאטה בייסים שנעשה בהם שימוש לרוב הם mySQL, Oracle, postgreSQL ...
איך מנהלים קליינטרים רבים במקביל?
- בעזרת scaling - ניצור יותר מhiveserver אחד שיתמודד עם בקשות של לקוחות, הhive serverים יפתחו סשן לכל לקוח ובו הוא יוכל לשאול יותר משאילתה אחת (כי קונקשן לכל שאילתה זה לא יעיל) או ניצור כמה instances של הHMS כדי לטפל בבקשות במקביל ולא להעמיס על שרת אחד.
- נגביל את מספר החיבורים האפשריים במקביל (fixed size thread pool) לקוחות שונים שרוצים לתשאל באותו זמן יקבלו תהליכים שונים שיעבדו "במקביל".
- כל השאילתות שלא יכולות להיות מנוהלות כרגע כי יש עומס יכנסו לתור ויחכו שיגיע תורן, מתבצע חלוקת CPU בתור לפי אלגוריתם מסויים (RR/FCFS/וכו) .
- לשים locks על נתונים כדי למנוע סתירה בין נתונים כששני לקוחות עושים פעולות במקביל, הlocks הם לקריאה, כלומר כמה שאילתות יכולות לקרוא נתון באותו זמן אבל לא לכתוב באותו זמן, אפשר לנעול פרטישן, טבלה או את כל הDB. זה תנאי הכרחי לACID ולמנוע קונפליקטים.
  

3. **Schema & Tables:**  What are the key tables in the metastore schema (e.g. DBS, TBLS, SDS, PARTITIONS)? How do they relate to Hive objects?

הטבלאות העיקריות בmetastore הן:
- הTBLS - שומרת מידע שקשור לטבלאות hive tables כגון שם טבלה, הזמן שנוצרה וכו..
- הDBS - מידע אודות הדאטה בייס עצמו, המיקום שלו וכו..
- הSDS - מידע אודות אחסון פיזי ממש, פורמטים ולאן לפנות בHDFS.
- הpartitions - מידע אודות כל הpartitions שיש על הטבלאות.
- הcolumns_v2 - מידע אודות כל העמודות בטבלאות, שם עמודה, פורמט וכו...

  הטבלאות האלה אחראיות לוודא שכל אובייקט בhive שמור במבנה מסויים לפי הפורמט שצריך ובמיקום שצריך.

4. **Extensibility & Clients:**  How do external engines such as Apache Spark, Trino, and other tools interact with the metastore? What APIs and protocols are used?

איך apache/trino מתקשרים עם hive?
הם פונים לconnector שלהם או ישירות לmetastore (בדרך כלל טרינו ישירות וספארק ישירות).
אם הפנייה היא ישירות אז היא לא עוברת דרך hiveserver2 אלא רק דרך הthrift api and protocol , הhive server מתרגם בקשת SQL לRPC ומקוד אותה ודרך פרוטוקול thrift לmetastore.
הmetastore יפנה לדאטה בייס ויחפש את המידע הנדרש אותו הוא יחזיר גם בבקשת RPC.
בעת גישה דרך HS2 אז נשלח שם משתמש וסיסמה בדרך כלל והHS2 מבצע גם אותנטיקציה, הJDBC ימיר את הבקשה לRPC וישתמש בפרוטוקול thrift.
הHS2 הוא זה שיעדכן את הmetastore.


5. **Administration:**  What are common administrative tasks (backup, schema upgrades, migration, repair)? What happens if the metastore becomes unavailable, and why is it considered a critical dependency in data platforms?

משימות מנהלתיות נפוצות:
- עדכון סכמות - משתמשים בschematool כדי לעדכן את סכמת הRDBMS כשעושים עדכון גרסה כדי שיהיה עקביות.
- גיבוי - שמירת גיבוי לDB בעזרת dump, שמירת גיבוי תקופתי (cron) ושמירת snapshots של המטא סטור.
- הגירה - העברת המטא סטור בין DB שונים בעזרת dump וrestore ועדכון הקונפיגורציות.
- תיקונים - כשהמטא דאטה לא תואם לנתונים עושים repair שסורק את HDFS והpartitions ומסנכרן את הדאטה עם המטא סטור.
- ניקוי - לעשות cleanup כדי למחוק טבלאות ישנות/ partitions לא רלוונטים.
- טיונינג - לעשות scaling/caching כדי להקל על שרת הHMS.
  *בdump עושים EXPORT לאחסון לוקלי/HDFS.
  *במהלך restore עוצרים את hive.
  אם המטא סטור תיפול הספארק וטרינו יקבלו שגיאות על שאילתות ולא יהיה אפשר לבצע שליפות, שרת HMS אחד יכול להוות single point of failure. 

## Hive Table Formats

Answer the following questions to understand table formats:

1. **Definition & Role:**  What does a “table format” mean in Hive? How does it differ from table metadata stored in the metastore? Explain the relationship between logical schema and physical file layout.

הכוונה בhive table format היא סידור הקבצים מHDFS לפולדרים לפי partitions בצורה היררכית לפי מבנה מסויים.
זה מהווה מין מבנה פיזי למידע שקובע איך זה מסודר ממש על הדיסק בניגוד למטא סטור שרק מאחסן את המטא דאטה של הכל ולא בהכרח בשום מבנה היררכי.
הטבלאות של Hive formats ממופות והתיקיות שלהן נשמרות בהיררכיה בפורמט הזה, הpartitions של הסכמות הלוגיות בפועל יהווה חלוקה בדיסק הפיזי.

2. **Common Formats:**  Describe popular formats such as Text/CSV, Parquet, ORC, Avro. How do they differ in encoding, compression, columnar storage, and query performance?

פורמטים:
- הCSV - שומר מספרים וטקסט כשכל ערך מופרד בפסיק,משומש לשמירת מידע טבלאי. נשתמש כשנרצה מידע לא מקודד כי אנשים צריכים להבין את הקבצים.
- הORC - שמירה בעמודות וחלוקת המידע לקבצים של עד 64MD, שליפות מהירות וקל מאוד לדחיסה, ניתן לקרוא עמודה אחד ואין צורך לעבור על כולן בשביל נתון מסויים (מה שלא רלוונטי אפשר לדלג), נשתמש בו כשיש צורך בACID והרבה פעולות קריאה כי הוא יודע להתמודד איתם טוב מאוד בעזרת הIndexing.
- הparquet - שמירה בעמודות , מהיר לניתוח, מפריד מטא דאטה מהנתונים, קל לדחיסה. נשתמש כשיש צורך בגישה להרבה פלטפורמות (קבצי parquet ידועים בכך שהם נגישים לפלטפורמות שונות, הם לא צריכים לעשות המרה כדי לקרוא ולכתוב אליהם), הם מעולים לפעולות אנליטיקה.
- הavro - שמירה בשורות, במבנה של JSON והנתונים בפועל נשמרים בפורמט בינארי מה שמקטין את הקובץ, נשתמש אם יש עומס בפעולות כתיבה או לסטרימינג נגיד כי הכתיבה בשורות גורמת לכך שאין אוברהד כמו בשאר הפורמטים.

3. **Schema & Tables:**  Explain the difference between managed and external tables, including ownership, lifecycle, and storage location semantics. How does the metastore map logical tables to physical data in storage systems like HDFS or object storage?

שני סוגי הטבלאות:
טבלאות managed - הhive אחראי ובעלים גם של המטא דאטה וגם של הנתונים עצמם, בעת פעולת load הנתונים מועברים ל/warehouse ויושבים בFS שיצרנו, בעת drop גם המטא דאטה וגם הנתונים עצמם נמחקים.
טבלאות external - בעלים רק של המטא דאטה ולא מאחסים שום נתונים בפועל. שומרים רק רפרנס למיקום של הקובץ עצמו, בעת פעולת load יצרו פוינטר אליו, בעת drop רק המטא דאטה ימחק והנתונים עצמם ימשיכו להתקיים כרגיל בHDFS/S3..
כל הקבצים ממופים ע"י ORM מהאחסון (HDFS/S3/כל דבר אחר) אל הטבלאות הלוגיות.

4. **Integration with Storage:**  How do table formats map to physical storage (directories, files)? What conventions does Hive use for partitions, buckets, and file naming?

הפורמט נראה כך:
דאטה בייס
| - טבלה
   | - טבלה partition 1
   | - טבלה partition 2
         | - פרטישן 2 באקט 1

עבור פרטישנים - הנתיב יראה בעצם ככה :   
.../warehouse/company_name.db/sales/year=2026 
כשsales זה שם הטבלה וyear=2026 זה הpartition, תחת זה נראה את כל הbuckets תחת אותו פרטישן או הקבצים בו.
עבור bucket זה יראה כך:
.../warehouse/company_name.db/sales/year=2026/00000_0
וכך מספר שונה לכל באקט.
אפשר להגביל את מספר הבאקטים, הפפרדה לבאקטים ושיבוץ עדכון בבאקט נעשית בעזרת פונקציית hash ועם עמודה של clustered by.
לכל באקט מחשבים את ההאש שלו ומאזנים אותם.


### 🔄 Alternatives
Assignment: You are required to research and write a comparative analysis between Hive table format and HMS and an industry alternative.
- Deliverable: A written summary (minimum 1 or 2 sentences).
- Focus: Compare performance, architecture, and specific "pain points" this tool solves compared to legacy systems or competitors.
- Goal: You must be able to justify why the department uses this tool for our specific environment.

  אלטרנטיבות לmetastore וhive table format - הAWS glue data , הוא גם מאחסן מטא דאטה באותה צורה שמטא סטור מאחסנת רק שהוא cloud based וגם serverless כלומר בניגוד למטא סטור אנחנו לא צריכים "לתחזק" אותו, אין צורך לעשות קינפוג או scaling או בכללי שום דבר שקשור לניהול השרתים שלו. אופציה נוספת היא databricks unity catalog שבכללי הביצועים שלה הרבה יותר טובים מhive, שליפות מהירות יותר ומטפל במקביליות של לקוחות יותר טוב, היא לא per-workspace אלא multi-cloud cross-workspace.
  במה מטא סטור יותר טוב מaws glue ? זה לא עולה כסף :)


### 🎯 User Story & Scenario
Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.
- Deliverable: A written summary example/story (two paragraphs approx.).
- Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.
- Data Flow: Map out the data flow and explain how this tool integrates with other components in the Data Pipeline.

*********************** שאלות סקילה ***************************************************
1. האם סדר העמודות חשוב בטבלה? כן כי זה יוצר בעיה עם partitions אם לא (לא הבנתי מה).
2. האם hive אוכף את הסכמה ואם כן מתי? hive אוכף את הסכמה רק כשנעשה read, ואז אם יש אי התאמה בין הנתונים יוחזר null, אחרת זה אחראיות הלקוח.
3. הבדל בין thrift לJDBC - הJDBC הוא מין connector בין הלקוח לHS2 , מאפשר שאילתות בצורת SQL ומשתמש בthrift protocol. הthrift API מתקשר ישירות עם המטא סטור סרבר ומשתמש גם הוא בthrift protocol אבל יותר low level מאשר JDBS.
4. הבדל בין thrift לRPC - הthrift מבצע את הבקשות RPC ומתרגם אותם אל ומSQL. הוא מהווה בתור השכבת תעבורה בערך של הRPC.
5. שימוש בREST ובRPC - הREST מבוסס HTTP, איטי יותר מRPC. נשתמש בRPC כשצריך לבצע משימה אחת ולא שיש צורך במשאבים.
6. איך מבזרים עומסים על שרתי HMS? בעזרת שיטת round robin או כלי חיצוני שמבזר עומס (עולה כסף, מנחשת שלא משתמשים אצלנו).
7. מהם metastore locks? יש dbLockManager שמאחסן מידע על המנעול במטא סטור בטבלה בשם HIVE_LOCKS שמים מנעול על טבלה בעת שמעדכנים או מוחקים בה נתונים וברגע שמסיימים משחררים את המנעול.
8. מה זה MSCK repair? פקודה שמסנכרת את המטא סטור עם הHDFS/S3 ממש . יכול גם לעדכן וגם למחוק מהמטא דאטה נתונים שהתשתנו (בגרסאות קודמות לא היה אפשר למחוק) ואפשר לעשות זאת אוטומאטית אם מוסיפים אותו לETL pipeline.
9. לבדוק לגבי שורה עם אובייקט בtable? אפשר לאחסן גם array/map/struct.
10. מתי עדכון יופיע בשליפה? אם מדובר בהוספת קבצים לHDFS אז השינויים לא יושמו עד שיעשו MSCK REPAIR, אם השינוי הוא דרך hive אז הmetastore יתעדכן.
11.  אפשר להגביל partitions? כן.
12.  שני טבלאות hive יכולות להצביע על אותו נתיב? כן בטבלאות EXTERNAL.
13.  איפה הcaching נשמר? יכול להיות גם על צד לקוח (JVM) וגם על צד שרת (HMS) 

## Wrapping Up :trophy:
Review your answers with your mentor and make sure you can articulate how the metastore and formats enable interoperability across Hadoop tools.

## Action Items
- Identify areas of metadata or format behavior you want to explore further.
- Prepare questions for the mentor Q&A session.
- Continue linking these ideas to other chapters as part of the Day 01 challenge.

## Recommended Resources
- [Hive Metastore Documentation](https://cwiki.apache.org/confluence/display/Hive/Metastore+Overview)
- [Hive Language Manual – Table Formats](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL)

