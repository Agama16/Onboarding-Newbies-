# Hive on MapReduce and Tez 🐝

## Overview
Today’s session introduces how Hive queries are executed using distributed compute engines. While Hive defines the table format, schema, and metadata through the Hive Metastore (HMS), the actual query execution is performed by an underlying processing engine.

Historically, Hive executed queries using MapReduce. Later, Apache Tez was introduced to significantly improve performance and efficiency.

**The emphasis is on understanding how Hive queries are translated into distributed execution jobs and how MapReduce and Tez differ as execution engines.**

## Goals
- Understand how Hive queries are executed in a distributed environment.
- Learn the basic execution model of MapReduce.
- Understand how Apache Tez improves Hive query execution.
- Build intuition about how SQL queries translate into distributed jobs.

:warning: **Note:**
- This is a self-study day; independence and time management are crucial.
- Focus on understanding the concepts rather than memorizing implementation details.
- If you cannot explain how a Hive query becomes a distributed job, revisit the material.
- Ask your mentor if something is unclear.

### ⏳ Timeline
Estimated Duration: 1 Day

- Day 1: Learn the basics of Hive query execution and how MapReduce and Tez are used as execution engines.

---

### Guide Questions❓

Answer these five questions to understand how Hive queries are executed using MapReduce and Tez.

1. **Hive as a Query Platform:**  
   Hive provides tables, schemas, and SQL querying on top of distributed storage systems such as HDFS. Explain Hive’s role as a platform layer that sits above storage and relies on external compute engines to execute queries.

כמו שראינו, hive מחולק ל3 חלקים, הhive table, הmetastore וhive כמנוע עיבוד שהופך שאילתות SQL למשימות מבוצעות. הוא לא מאחסן בעצמו את המידע אלא רק מהווה חיבור בין האחסון לשאילתות.
השכבה שלו מעל האחסון והפורמט טבלאות שלו מאפשר חיבור בין נתונים לא מובנים לבין שאילתות דומות SQL שעובדות על דאטה בייס רלציוני.
הhive משתמש בניב שנקרא hiveQL והוא אחראי על תרגום שאילתות לשלבים לוגים וגם למשימות ממש שיעבדו על מנועים חיצוניים כמו ספארק, tez, mapreduce וכו..
הhive לא באמת מבצע את המשימות, הוא בסך הכל מתרגם אותם למנועים החיצוניים שיבצעו אותם במקום שהמשימה תפנה ישירות נגיד לmapreduce וזה מצריך בכתיבת קוד java.
הקומפיילר של hive והדרייבר אחראי על לעשות parsing, למצוא את המטא-דאטה המתאים מהmetastore וליצור גרף של משימות (במקרה של ספארק או tez) או לסדרת משימות במקרה של mapreduce.

2. **Hive Query Stages and Task Execution:**  
When Hive translates a SQL query into a distributed job, how is the work divided into stages and tasks?  
Explain how Hive breaks a query into execution stages, how tasks are distributed across the cluster, and how intermediate results are passed between stages.

הדרייבר יקבל את הhiveQL ויצור לו סשן (הוא גם יאחסן את המטא-דאטה או תוצאות שנוצרות בביצוע המשימות) ואז הוא יעביר את השאילתה לקומפיילר.
הקומפיילר יעשה לשאילתה parsing, כלומר יפרק אותה ויבדוק שהיא תקינה ומה המשמעות שלה ויצור ממנה Abstract syntax tree .
לאחר מכן הקומפיילר יבקש מהמטא דאטה את כל המידע שהוא צריך עבור השאילתה, ובעזרת המטא-דאטה הזה הוא יפרק את השאילתה לתוכנית בצורת DAG (direct acylic graph) בעזרת mapReduce שיעשה פילטרים וסורטים.
הmapreduce יבצע את המשימות בעזרת YARN שיתזמן זמני מעבד ומאבים.
כל mapReduce job מפורקת לtasks שונים שרצים במקביל על datanodes שונים, קוראים לזה input splits. בדרך כלל מנסים לעשות את הmap task על הdata node שבו הנתונים שמורים בHDFS.
כל map task דואג לקרוא את הנתונים שהוא צריך ולבצע את השאילתה על החלק הלוקלי שלו, ואז הmapReduce עושה shuffel ומיון לפי key שצריך בין כל התוצאות.
כל תוצאה של map tasks נכתבות לדיסק (אבל בתכלס קודם לmemory buffer בגודל 100MB) והreducers משתמשים בהם, אם הmap task נכשל באמצע, האדופ יריץ אותו על data node אחר. התוצאה של הreducer תיכתב בHDFS.
יכול להיות יותר מreducer אחד ואם יש יותר מאחד אז יוצרים פרטישן (בדרכ hash bucketing, אבל יכול להיות מוגדר עי הלקוח).
אפשר שיהיה גם 0 reducers אם אין צורך בshuffle.
ה stages:
-הmap tasks שעושים סריקות פשוטות, כותבים תוצאות לדיסק 
-הshuffle שעושה מיון לתוצאות ו join/group by לתוצאות שלהם
-הreduce tasks שעושים צבירה של הנתונים (ופעולות אחרונות אם צריך) וכותבים אותם לHDFS


3. **Hive Query Execution Pipeline:**  
   What happens when a user runs a query in Hive? Describe the main stages of execution: SQL parsing, logical planning, physical planning, and submitting jobs to an execution engine such as MapReduce or Tez.

תהליך השאילתה:
- השאילתה מגיעה לדרייבר שיוצרת לו סשן
- משם היא מועברת לקומפיילר שעושה parsing
- הקומפיילר עושה semantic analization ובודק שכל הטבלאות קיימות וכו ואז מפרק את הפקודות לפילטר,JOIN,scan וכו...
- הקומפיילר מבקש את המטא דאטה הנדרש ובהתאם לנתונים יוצרים תוכנית לוגית.
- הקומפיילר יבחר מנוע עיבוד (taz/mapReduce) ויקבע איפה נעשה הmap tasks, איפה הreduce tasks ואיפה הshuffle נעשה ועל מה.
- הקומפיילר ישלח את הjobs לtez/mapreduce. 

4. **MapReduce Fundamentals:**  
   What is the MapReduce programming model? Explain the roles of the `map phase`, `shuffle and sort`, and `reduce phase`. Why was MapReduce originally used as Hive’s execution engine?

מודל הmap reduce:
הmappers לוקחים את הdata והופכים אותו לkey value לפי הפילטר שדרוש, לדוגמה (פעולות סריקה, SELECT לדוגמה) והreducers הופכים אותם לתוצאה סופית.
- הmap phase : החלק הראשוני יותר של העיבוד, מחלקים את המידע לsplits שונים , וכל אחד לdata node שונה. מבצעים את הפעולה על הנתונים כך שהם הופעים לערכי key-value בהתאם לסריקה שצריך לעשות, את התוצאות רושמים בדיסק ומעדכנים את הapplication manager.
- הshuffle and sort : כשהמידע נכתב לדיסק, ערכי המפתחות עוברים פרטישנים לפי פונקציית hash, ואז בכל פרטישן ממיינים אותו.
- הreducer phase : מקבל את המידע מהapplication manager צובר את כל הkeys-values לערך סופי וכותב את התוצאה לHDFS.
- הapplication master יוצר application master job לכל map job שנוצר ומת ביחד איתו, הוא אחראי על לדעת באיזה data node נמצא כל map task.
-  
הhive השתמש בmapReduce כמנוע ביצוע שלו בגלל שהוא ידע לעשות scalability בצורה טובה וhive משומש לאינטגרציה עם האדופ שמצריך את זה, בנוסף mapreduce בא עם הרבה מנגנונים לטיפול בכשלים ותקלות.

5. **Introduction to Apache Tez:**  
   What is Apache Tez, and how does it improve Hive query execution? Explain how Tez replaces chains of MapReduce jobs with a Directed Acyclic Graph (DAG) of tasks, reducing unnecessary disk I/O and improving query performance.

הapache tez הוא גם מנוע ביצוע בדומה לmapreduce שעובד בצורה שונה טיפה, גם הוא עובד עם hive ועל גבי האדופ.
בtez משתמשים בDAG כלומר יוצרים מודל של עץ ישיר ללא מעגלים בו מיוצגות הjobs כתחליף לשרשרת של jobs בmapreduce, כידוע map-reduce task יכולים לכסות צבירה אחת של נתונים, ועבור שאילתות מסובכות יותר תיווצר שרשרת של משימות כאלה.
הtez הוא בעצם אלטרנטיבה לmapreduce, הוא משוכלל יותר ורץ מהר יותר.
ביצוג של DAG כל mapper או reducer הוא בעצם קודקוד וכל shuffle and sort הוא קשת ביניהם, בעץ כל משימה יכולה להתחיל כשהinput שלה מוכן, לעומת זאת בmap reduce חייב לחכות לכל המשימות הקודמות, בגלל זה tez מספק ביצועים יותר מהירים . tez מאפשר לעשות map/reduce tasks על אותו data node וגם לא מבצע כתיבה לHDFS עד הreducer האחרון ביותר, מה שמפחית I/O . בנוסף tez עושה reuse לקונטיינרים של JVM ומשתמש במשאבים שלהם למשימות הבאות מה שמקטין את הlatency.


************** הערות *******************
לספארק יש query optimizer בשם catalyst שעושה pruning לעמודות בוחר אסטרטגיות JOIN יעילות
ויש לו את הtungsten שעובד על שמירה בעמודות ויעול cache locality.
הhive בכללי נוצר כמנוע עיבור בשביל batch processing וETL, בהתחלה נוצר על map reduce מה שכן גרר high latency, שימוש בטז גרם לlatency נמוך הרבה יותר.

********************** שאלות סקילה ****************************
1. מתי הmap job הבא יכול לרוץ בmap reduce? גם בmapreduce הם יכולים לרוץ במקביל.
2. איך מתרגמים מHQL לmapreduce? הparser מפריד חלקי שאילתה, הsemantic analyzer הופך אותם לפעולות כמו פילטר , scan וכו להכנת ממש תוכנית של מה שצריך לעשות. והקומפיילר מחלק אותם לעבודות של map וreduce, הhive serielizer מתרגם את הנתונים בטבלאות לjava שהmap reducer יבין.
3. מתי tez כותב לדיסק? בכל כתיבה אחריי map/reduce job או שאפל אם הבאפר בזיכרון התמלא.
4. מתי נשתמש בmap reduce ולא בtez? במקרים בהם fault tolerance ממש קריטי ואפילו איבוד מידע בזיכרון הוא חמור נעדיף map reduce כי הוא מבצע רישומים לHDFS לעיתים תכופות יותר.
5. מה מבטיח fault tolerance בtez וmap reduce? בtez מזהים את האיזור המדוייק בDAG שבו נכשל התהליך ומריצים אותו מחדש, בנוסף על כך הוא עושה אופטימיזציות לDAG כך שיהיה יותר יעיל בזמן ריצה. map reduce מזהה מה הdata node שנפל ודואג לעשות map job חדש על data node אחר. ובנוסף הוא מזהה משימות איטיות מדיי, משכפל אותן לdatanodes אחרים ולוקח את מי שסיים הכי מהר. 
6. איך JOIN עובד בtez? יש גם JOIN זהה לmap reduce בו אחריי השאפל והסורט של תוצאות הmap tasks עושים JOIN לreducer .
7. איך אפשר כלקוח לייעל שאילתה איטית ? - האם הפרטישנים שלי יעילים - האם אני מבקש שיחזירו יותר נתונים ממה שצריך - האם הנתונים שאני מבקש אוחסנים לוקלית אצלי - האם יש לי יותר מדיי קבצים קטנים וצריך לעשות compaction בהאדופ - האם יש דרך לפשט את השאילתה
8. איך עובדת דחיסה בhive? בכל באקט אנחנו נעשה דחיסה של הקבצים הקטנים לקובץ אחד גדול, הדחיסה תתבצע כtask של map reduce/tez.
9. אופטימיזציות : לtez יש רכיב בשם cost based optimization שעובר על אפשרויות שונות לבצע את המשימה ומחשב להן עלויות ובוחר את הזולה ביותר, נוסף על כך הוא עושה פחות כתיבות לHDFS ובכך חוסך גישות לדיסק . גם tez וגם map reduce שומרים על data locality, כלומר הם מבצעים tasks על הdata nodes שעליהם הנתונים שמורים בHDFS. בtez כל השאילתה רצה כtez job אחד ולכן יש פחות overhead סביב התהליך.
10. מה בא אחריי הphysical plan בשלבי הhiveQL query ? אחריי הphysical plan מעבירים את הjobs לכלי העיבוד (mapreduce/tez) שיוכלו לבצע את המשימות , ניתן לעשות זאת במקביליות. 

---

### 🔄 Alternatives
Assignment: Briefly research another distributed processing framework used for large-scale data processing.

- Deliverable: A written summary (1–2 sentences).
- Add a simple real-life use case.
- Focus: What problem does this framework solve compared to MapReduce or Tez?

אלטרנטיבה נפוצה לmap reduce/tez היא ספארק שזה גם מנוע לעיבוד וביצוע שאילתות SQL שבניגוד לmap refuce / tez במקום לעשות שמירות ביניים בדיסק היא עושה אותן בזיכרון ובגלל זה גם נחשבת הכי מהירה מבין השלוש, היא טובה לstream, batch ולML . בדרך כלל מועדפת על tez וmap reduce. מציעה מתודות מתקדמות יותר לאופטימיזציה כמו column pruning והcatalyst optimizer שהוזכר. נעדיף את map reduce/tez כשלא רוצים להעמיס על הRAM כי ספארק דורשת ממנו הרבה.
---

### 🎯 User Story & Scenario
Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.
- Deliverable: A written summary example/story (two paragraphs approx.).
- Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.
- Data Flow: Map out the data flow and explain how this tool integrates with other components in the Data Pipelin

## Wrapping Up :trophy:
Review your answers with your mentor and make sure you can clearly explain how a simple Hive query becomes a distributed computation job. This knowledge will help you understand later query engines and compute systems used in the data platform.

---

## Action Items
- Identify parts of Hive query execution you want to explore further.
- Look at example Hive query plans to see how jobs are structured.
- Prepare questions for the next mentor Q&A session.

---

### 📚 Resources
Use the resources listed below and practice searching the internet for questions not answered by the provided documentation.
- [Hive Documentation](https://hive.apache.org/docs/latest/)
- [Hadoop: The Definitive Guide (O'Reilly)](https://piazza-resources.s3.amazonaws.com/ist3pwd6k8p5t/iu5gqbsh8re6mj/OReilly.Hadoop.The.Definitive.Guide.4th.Edition.2015.pdf)
- [Apache Tez Documentation](https://tez.apache.org/)
- [Apache MapReduce Docs](https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)
