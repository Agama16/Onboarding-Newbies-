# Spark Fundamentals:
## Overview
This section will go over the fundamentals of _apache spark_.

**We will focus on general concepts such as the spark architecture, optimizations, caching and data geometry.**

## Goals
- Develop a foundational understanding of how scheduling is done.
- Learn the common terminology used by most schedulers.
- Practice planning a self-study day and estimating time for learning.

:warning: **Note:**
- This is a self-study day. Independence and time management are essential.
- Many newcomers struggle with self-study; take a moment to plan your day and stick to it.
- Understand the **big picture** of each concept. If you can't explain it, you probably haven't learned it.
- Be prepared to describe how concepts relate to one another and to real-world scenarios.
- Review the [Exercise](#exercise) before diving in so you know what to focus on.
- When in doubt about what you need to learn, ask your mentor.

### Core Concepts

Think through the following questions; by answering them you’ll touch every major topic listed above:

1. **Spark Architecture & Execution:** what are the main components of spark? what is the role of each component? what are their roles? what is the difference between a transformation and an action? how does spark achieve fault tolerance? what is lazy execution in spark? go over [this](assets/where_do_i_run.py) and for each line, comment where it runs.

ספארק הוא מנוע לעיבוד נתונים במקביל על קלאסטרים שמאפשר לעשות עיבוד מסוג טעינת נתונים, שאילתות SQL, ועד לML ולstream processing, והכל בצורה אחידה עם סט אחיד של API'S.
ספאר הוא פרוייקט open source שבנוי על בפריות סטנדריות בשילוב עם ספריות שנכתבו ע"י צד שלישי והן כוללות ספריות לנתונים מובנים (spark SQL), ללמידת מכונה (MLlib9) , לאנליטיקות גרפים (graphX) ועוד.
ספארק התחיל כשרצו למצוא מענה לבעיית ביצועים של map reduce בגלל הצורה בה מעבדים נתונים בה, בעיקר בML, כל פעם שהיו צריכים להריץ אלגוריתם על הנתונים זה היה נחשב job חדש שיטעון את הנתונים מ0 וירשום אותם לדיסק שוב כל פעם  מה שהיה מכביד מאוד על המערכת ואיטי.
ספארק מנהלת ומתאמת משימות שמבוזרות על שרתים שונים.
ספארק בנוי מקלאסטר המנוהל ע"י הcluster manager שהוא יכול להיות הspark cluster manager או להיות מנוהל ע"י YARN/קוברניטיס.
הספארק מריץ spark application שהוא בעצם job או רצף של jobs שצריכים לרוץ בסדרה או במקביל שמכיל בו את הdriver process ואת הexecution processes.
הdriver process מריץ את הפונקציית main() ויושב על node מסויים בקלאסטר והוא אחראי על:
- לשמור את כל המידע על הspark application הנוכחי (מצב הapplication - רץ, הסתיים וכו, מצב הexecutore, וכו).
- להחזיר תשובות ללקוח.
- לנתח את העבודה, לבזר ולתאם אותה על גבי הexecutors. הוא יוצר את הlineage, logical/physical plan ומתרגם את הקוד לקוח למשימות.
- יוצר את הspark session שיוצר dataFrames, RDD, ואת כל הפעולות שהזכרנו קודם. sparkcontext הוא הלגסי של זה שהיה רק Low-level API שעשה תכנון דינמי ותיאום משימות אבל לא השתמש באופטימיזציות כמו catalyst ולא היה מאוחד לכל השפות (היה צריך גם SQL CONTEXT). 
הexecutors מבצעים את העבודה שהdriver נותן להם ומדווחים על מצבם לdriver. כל אחד מהם בהאדופ רץ על קונטיינר של YARN.
הcluster manager אחראי לספק משאבים לdriver שמחלק אותם לexecutors.
הdataFrames:
זה structured API שבונה פשוט טבלאות שיכולות להיות פרוסות על כמה מחשבים. הוא בעצם datasets שמסודרים לעמודות
פרטישנים:
הפרטישנים בשילוב מספר הexecutors יקבעו כמה משימות יכולות לרוץ במקביל.
הtransformations:
הdataFrames בספארק הם immutable, לכן כשרוצים לעשות עליהם פעולות בעצם יוצרים dataFrames חדשים בעזרת טרנספורמציות, הן מתחלקות ל-2:
הnarrow - כל פרטישן עובר טרנספורמציה לפרטישן חדש. נשמר על הזיכרון.
הwide - כל פרטישן עובר טרנספורמציה ומופץ לכמה פרטישנים. נשמר על הדיסק.
הטרנספורציות יוצרים בעצם מה שנקרא lazy evolution:
בספארק כשיוצרים טרנספורמציה, בעצם יוצרים תוכנית אבל התוכנית הזאת לא מבוצעת עד הרגע האחרון מה שמאפשר לעשות אופטימיזציה לכל הpipeline שיצרנו ולעשות predicate pushdown נגיד.
הaction:
הטרנספורמציות הן בנייה של תוכנית לוגית מסויימת על הdataFrames אבל הaction הוא הטריגר שגורם להם לקרות, לדוגמה count.
יש 3 סוגי actions:
- פעולות כדי לראות נתונים בקונסול show()
- פעולות לאיסוף נתונים count()
- פעולות לכתיבת נתונים לdata sources כמו write.json()
הaction יוצר job שיריץ את הטרנספורמציות בnarrow transformation ואז יעשה צבירה בwide transformation.
הpipeline של הטרנספורמציות הוא בעצם הlineage שנוצר. אותו אפשר לראות בעזרת explain וזה מופיע כDAG של טרנספורמציות.
כמו בmapreduce , בספארק job הוא DAG של stages שמחולקים למשימות.
ספארק משתמשת בRDD בשביל fault tolerance, שזה פשוט החלקוה של אלמנטים על פרטישנים שונים ושמירת הlineage שלהם כמו שהזכרנו קודם, כל אלה מאפשרים להתמודד עם קריסה של node בעזרת שחזור המידע שהיה עליו. הפרטישן פשוט יועתק לexecutor אחר.
ספארק מתקשרת עם שפות שונות בעזרת API'S כמו:
לפייתון pySpark, לSQL בsparkSQL. בעזרת שרת RPC הם מתקשרים עם הJVM. נגיד בפייתון הpython proccess מתקשר עם הjava proccess בTCP בעזרת py4j.
בגרסה 3 הוצגה הspark connect API שמאפשר ללקוח לתקשר עם הקלאסטר בעזרת הdataFrame API בלי קשר לשפה.
בו התקשורת מוקמת בעזרת gRPC והלקוח עושה parsing עוד בצד שלו לקוד ויוצר את הunresolved plan ואז עושה serializing לprotocol buffers כדי לשלוח אותם לשרת. 

2. **Spark Planning & Optimization:** Logical vs Physical Planning: Walk through the transition from Logical Plan to Physical Plan; What is the fundamental difference between Rule-Based (RBO) and Cost-Based Optimization (CBO), what are the common kinds of optimizations used? What is the AQE? Why is running ANALYZE TABLE recommended for performant CBO? and what is whole-stage code generation?

התכנון הלוגי בספארק הוא ההפיכה של קוד מסויים לסט של משימות המסודר בצורה הכי יעילה לביצוע.
השלב הראשון הוא הפיכה לunresolved logical plan שבו עדיין לא בודקים אם השורות ועמודות שפונים אליהם קיימות.
ואז בעזרת הanalyzer ספארק בודק עם הקטלוג את תקינות העמודות והשורות ויוצר resolved logical plan.
ואז מגיעים לcatalyst optimizer שהוא בנוי מסט של כללים שלפיהם עושים אופטימיזציה ויוצרים את ה optimized logical plan.
התכנון הפיזי מתחיל אחריי זה כשמחליטים איך לבצע את התכנון הלוגי.
בדרך כלל מג'נרטים כמה תוכניות אפשריות ומשווים ביניהם.
בסוף התכנון הפיזי יש סדרת RDD'S וטרנספורמציות.
נעשו כאן שני סוגי אופטימיזציות:
- הRBO שהוא אופטימיזציה על בסיס כללים קבועים מראש, זה לא תלוי בנתונים עצמם שעושים עליהם פעולות אלא יותר predicate pushdown, expression simplification וכו..
- הCBO שהוא אופטימיזציה שכן תלויה בנתונים בטבלה ובסטטיסטיקות לדוגמה סדר הJOINים (תלוי בגודל הטבלה) וכו..
האופטימיזציות הכי נפוצות:
  - הAQE (adaptive query execution) : טכניקה שעושה שימוש בסטטיסטיקות בזמן ריצה לפיהם היא יכולה לעשות re-optimize לשאילתה בצורה הכי יעילה למצב הנוכחי. אפשרי רק בגרסה 3.
  - קאשינג : אפשר לעשות קאשינג לטבלאות שבו עושים caching לעמודות רלוונטיות ודוחסים אותם למינימום האפשרי.
  - אסטרטגיית JOIN : יוסבר בשאלה הבא.
  - הפרסיסט : שמירת תוצאות ביניים לוקלית.
  - הpartition tuning : מאפשר לעשות repartition לנתונים (עם המלצה שפרטישן יהיה בין 100-200 MB).
  - הwhole stage code generation : ממרג'ג' כמה פעולות לstage אחד כדי לחסוך את הoverhead שבכל פעולה.
  בCBO הסטטיסטיקות לקוחות מהקבצים עצמם או מהסטטיסטיקות זמן ריצה אם אפשרו AQE, אם נעשה ANALYZE, האופטימיזציה תעשה גם עם סטטיסטיקות מהקטלוג לשיפור ביצועים. 

3. **Spark Shuffle & Joins:** Compare the different kind of joins, and when will spark use each? how can we tell spark to prefer one over the other? what is join reordering? and why is "broadcasting" considered a high-risk, high-reward optimization? What is a _Narrow_ transformation, and _Wide_ transformation? Why do some operations require shuffle? what exactly is written in shuffle?

סוגי JOINים :
- הLEFT JOIN : מחזיר את כל הערכים בטבלה השמאלית וכל הערכים התואמים בטבלה הימנית.
- הRIGHT JOIN : הפוך מהLEFT JOIN.
- הFULL JOIN : יחזיר את שני הערכים בטבלאות.
- הCROSS JOIN : מחזיר מכפלה קרטזית של הטבלאות.
- הINNER JOIN : מחזיר ערכים מטבלה שמאל שיש להם התאמה עם טבלה ימין.
- הLEFT ANTI JOIN : מחזיר את כל הערכים בטבלה שמאל שאין להם התאמה עם טבלה ימין.

הjoin strategies:
- הbroardcast hash join : הדאטה סט הקטן יותר נשלח לכל האקסקיוטרים שיש להם פרטישן הקשור לדאטה סט הגדול יותר. עושים לדאטה סט הקטן יותר האש ובאקטינג. ואז עושים JOIN בין השורות בטבלה הגדולה לשורות בבאקטס שיש סבירות שיש התאמה. זה JOIN מהיר יחסית כי הוא לא דורש שאפל או סורט. נרצה להשתמש בזה כשיש טבלה קטנה יחסית ולשמור אותה לא יפגע לנו בביצועים וכשאין מספר גדול מדי של nodes.
- הshuffle hash join : עושים שאפל לפרטישנים (כלומר מחלקים בהם את הנתונים מחדש) ובכל Node עושים לצד הקטן יותר hashing ובאקטינג (בלי שידור ברודקאסט) ועושים ביניהם JOIN.* הkeys צריכים להישאר באותו פרטישן. נשתמש בזה כשהטבלאות גדולות מדיי לברואדקאסט
- ה shuffle sort merge join : עושים שאפל וסורט לשני הדאטה סטס ואז עושים להם סוג של מרג' עוברים על שניהם ועושים JOIN. נשתמש בזה כשגם אחריי פרטישן הדאטה סטס גדולים מדיי להישמר בזיכרון. יקר יותר מJOINים אחרים.
- הbroadcast nested loop join : עושים ברודקאסט לדאטה סט אחד ואז JOIN לכל הרקורדס בהם. איטי מאוד, נשתמש בזה בnon equi joins כי שאר המתודות לא עובדות על זה.
- המכפלה קרטזית : דומה לקודם רק שאין שליחת ברודקאסט של הטבלאות. יקר ובדרך כלל לא נבחר.
פעולת JOIN של ברודקאסט יכולה להיות מאוד מסוכנת כי היא יכולה לגרום לשגיאות OOM אבל היא חוסכת את השאפל שהוא נורא יקר תעבורתית לכן יכולה לספק JOIN מהיר מאוד. 

4. **Tungsten & Resources in Spark:** What is an RDD? Why did Spark move away from RDDs in favor of DataFrames/Datasets? Explain how Tungsten uses off-heap memory to avoid Garbage Collection pauses. Why is it a bad idea to give one executor a lot of resources (the "Fat Executor" problem)? What is the difference between Execution/Storage memory and the overhead memory? What happens when a task exceeds its allotted execution memory?

הRDD הוא אוסף נתונים המבוזרים בקלאסטר.
ספארק עברו מהRDDS לdataFrames כי הוא לא מבין את הדאטה, בניגוד אליהם הRDD לא מזהה סכמות ואין לו את הcatalyst והtungsten.
בניגוד אליהם RDD מייצג נתונים גם בצורה לא מובנית לחלוטין, כלומר אין פורמט סכמתי כלשהו.
דאטה סט - קולקשן של דאטה מטייפ מסויים, מעולה לETLים והרבה טרנספורמציות. דאטה פריים - דאטה סט בו הטייפ הוא שורות (לא יודעים מה הסכמה

5. **Spark Skew, Partitioning & Caching:** What is data skew? how can it be solved? what is the difference between `repartition(n)` and `coalesce(n)`? What are the spark `StorageLevel`s? what is the difference between `cache` and `persist`? why are udf's (expecially in python) bad? how does spark solve the serde bottleneck with udf's?


### Real-World Context
Rather than focusing on one technology, think about how these ideas show up in distributed processing frameworks, how they are used by other procerssing frameworks and what are the core concepts of processing.

## 🔄 Alternatives

Assignment: You are required to research and write a comparative analysis between Spark and an industry alternative.

    Deliverable: A written summary (minimum 1 or 2 sentences).
    Focus: Compare performance, architecture, and specific "pain points" this tool solves compared to legacy systems or competitors.
    Goal: You must be able to justify why the department uses this tool for our specific environment.
ספארק הוא יותר לbig data processing וטרינו מתמקד יותר בשאילתות SQL מהירות. ספארק הרבה יותר כבד חישובית בגלל הטרנספורמציות. הוא מתאים יותר לETL וstreaming/batch וטרינו הרבה יותר לad-hoc.
## 🎯 User Story & Scenario

Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.

    Deliverable: A written summary example/story (two sentences approx.).
    Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.

## Wrapping Up :trophy:
Discuss your answers and any areas of confusion with your mentor. Reflect on how these general concepts will help when you later write code and help clients.

## Additional Topics from Review
- A deep dive into spark internals: what are other optimizations that are implemented in spark? what is java off-heap memory? how does spark's memory allocation work?
- What are other well known processing frameworks? what are the use cases spark meets? when should I NOT use spark?

## Action Items
- Review your notes and identify topics you want to explore deeper.
- Collect a list of real-world use cases for apache spark.
- Prepare questions for the upcoming mentor Q&A session.

## Recommemded Resources
- [Apache Spark Documentation](https://spark.apache.org/documentation.html)
