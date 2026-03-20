# Catalogs & Table Formats :

## Overview
This session dives into the metadata layer that sits above raw files in a data
lake or warehouse.  Before we talk about individual systems, start by thinking
about the big picture: what is a *data warehouse* versus a *data lake* versus a
*lakehouse*, and why do teams care about catalogs and table formats in each
case?  (Hint: consistency, governance, and performance are the common threads.)

We’re not going to install or run Spark/Trino/etc. (If you don’t know what those are, no worries you will soon.);
the material stays at themetadata level.  That said, good formats enable optimizations such as
partition pruning, predicate push‑down, and efficient file compaction, all of
which have a dramatic impact on execution even though we won’t be executing
anything here.

**We’ll examine why catalogs exist, how they differ from Hive’s metastore
(which is itself just one implementation of a catalog), and the design goals of
modern table formats such as Iceberg, Delta Lake, and Hudi.  Examples of
catalog implementations include Hive Metastore, AWS Glue, Databricks Unity
Catalog, and even simple relational databases;

## Goals
- Clarify what catalogs and table formats actually manage and why teams put
  them on top of object storage.
- Sketch the difference between a warehouse, a lake, and the newer lakehouse
  idea so you have context for why metadata matters.
- Learn about emerging formats that implement ACID, schema evolution, time
  travel and other optimizations, and why those features make life easier for
  query engines.
- Build on previous lessons by focusing on interoperability and metadata
  management rather than specific execution engines.

:warning: **Note:**
- Keep the focus on metadata and format, and on optimizations derived from those rather than on query engines or execution.
- Ask your mentor if you're unsure about scope.

### ⏳ Timeline
Estimated Duration: 1 Day
- Day 1: Learn the concepts of catalogs and table formats; spend the day.
    - Have a Q&A session the same day

## Core Concepts

1. **Data warehouse / lake / lakehouse:**  What are the defining
   characteristics of each?  Why do architects care about a separate metadata
   layer in a lakehouse versus a traditional warehouse?

נפריד בין שלושת סוגי האחסון:
- הdata warehouse : אחסון שנועד לכמות גדולה של נתונים מובנים, המטרה שלו זה בעיקר לאפשר ניתוח נתונים בעזרת שאילתות SQL פשוטות (בניגוד לdata lakes). בדרך כלל מידע בdata warehouse יהיה מסודר לפי נושאים\תכונות וניתן לעשות אינטגרציה לנתונים ממקורות שונים. הנתונים בdata warehouse ישמרו לזמן ארוך (בגלל שהמטרה פה היא ניתוח אז רלוונטיות היא לא בהכרח הדבר הכי חשוב) והם לא ישתנו לעולם, כלומר ברגע שעושים עדכון או מחיקה לנתון זה לא באמת נעלם מהdata warehouse אלא רק נוצר נתון חדש עם העדכון הזה (אבל כן יש מתודות למחוק כפילויות\שגיאות). hive לדוגמה הוא data warehouse.
- הdata lake : אוסף של נתונים מכל סוגיהם, זה יכול להיות מובנה כמו טבלה, חצי מובנה כמו JSON ולא מובנה בכלל כמו סרטון או קובץ txt. זאת צורה אחסון מאוד גמישה שבדרך כלל משמשת לרשתות ולדברים כמו למידת מכונה. הdata lake יכול לאחסן כמות עצומה של נתונים, והאחסון יהיה זול יותר מאשר data warehouse נגיד, אבל הניתוח נתונים יהיה מסובך יותר וגם השמירה על שלמות ואמינות הנתונים. HDFS, S3 הם דוגמאות לdata lake.
- הlakehouse : שילוב של הdata warehouse והdata lake, הוא מאפשר אחסון של כמויות גדולות של מידע (גם לא מובנה) וגם מאפשר ניתוח של מידע מובנה ושמירה על אמינות ושלמות הנתונים. המטא-דאטה בו נשמר בצורה מובנה נפרדת ובמתודת ETL, אפשר לתשאל אותו בצורת SQL וגם בניתוח מתקדם של ML. לדוגמה databricks וapache iceberg יכולים לשמש כdata lakehouse.

  בdata warehouse כל המטא דאטה בין אם זה על האחסון עצמו, על התהליכים או על הנתונים, נשמר בmetadata repository בשליטת המערכת ובתצורת schema-on-write. 
  בdata lakehouse לעומת זאת נשמר בשכבה אחרת בפורמט פתוח מה שנותן גישה לכל כלי שתומך בפורמט הזה למטא דאטה ובכך מאפשר לעשות שאילתות וניתוח על נתונים בצורה המדמה data warehouse. 

2. **The Concept Of Catalog**  Describe the purpose of a metadata catalog.  How
   does it compare to Hive Metastore (hint: the metastore *is* a catalog)
   and why might systems introduce separate catalog layers (e.g. AWS Glue,
   Databricks Unity Catalog, in‑house catalog backed by PostgreSQL)?

הmetadata catalog הוא אחסון מובנה (בדרכ טבלאי) של נתונים על הנתונים שמטרתו לאפשר ניווט קל בין הנתונים, קביעה וסידור של הרשאות ושמירה על שלמות הנתונים ושקיפות במיוחד בארגונים עם כמויות גדולות מאוד של מידע, הhive metastore לדוגמה הוא metastore catalog כי הוא מאחסן את כל המטא דאטה של hive, אבל לא רק הוא נחשב כmetadata catalog, גם לdelta lake, AWS glue יש data catalogs ללא קשר לHMS.
בdatabricks המטא-דאטה שמור בunity catalog שנשמר בשכבה שונה בכל הנתונים, כך גם AWS glue שומר את המטא-דאטה ברפוסיטורי נפרד, וpostgreeSQL ששומרים אותם בסכמה נפרדת.
בדומה למה שכתבנו בשאלה קודמת, חברות יצרו שכבה נפרדת לmetadata catalogs כדי שלכלים חיצוניים יהיה גישה אליהם, לדוגמה לשלב spark/trino כדי לעשות ניתוח מתקדם ושאילתות מתקדמות על הנתונים, וגם כדי לעקוב ו"למשול" על הנתונים בצורה מסודרת שנפרדת מהנתונים עצמם.


3. **Catalog Architecture:**  Explain typical components of a catalog service
   (namespace management, table and partition metadata, permissions).  What
   backend storage is used?  Is the catalog itself just a database, or does it
   also manage pointers to objects in a blob store?

בדרך כלל הcatalogs יכילו את המרכיבים הבאים :
- הnamespace management : מכיל מטא-דאטה על המבנה ההיררכי והnamespaces שמערכת בהם נמצאות הטבלאות וכו..
- הטבלאות: שמות הטבלאות, מיקום, מתי נוצרו וכל המטא-דאטה הקשור לכך כמו פורמטים בסכמות ושמות עמודות.
- הpartitions : מטא-דאטה אודות כל הפרטישנים שיש בטבלאות, מזהה פרטישן, מתי נוצר ועוד..
- הרשאות : מי יכול לגשת למה (לא לרמת יוזרים אלא תפקידים).
  בדומה למה שראינו בhive metastore בדרך כלל נעשה שימוש בדאטה בייס רלציוני כמו oracle , postgreSQL כדי לשמור על אמינות ושלמות הנתונים (מה שקשה יותר בדאטה בייס לא רלציוני) וכדי שפעולות של טרנזקציות לדוגמה יהיו אטומיות ועקביות.
  בנוסף לכך בדומה למה שראינו בhive metastore הcatalog שומר גם פוינטרים לקבצים ממש ולא רק את המטא דאטה, במקרה כמו שראינו זה פוינטר לאובייקטים בS3/HDFS וכו.. ובמקררה של cloud based זה פוינטרים לאובייקטים בblob store . 

4. **Table Formats Overview:**  Define what a table format is in the context of
   a data lake.  How do formats like Iceberg, Delta, and Hudi differ from
   simple Hive/Parquet tables?  What features do they add ?

בהקשר של data lakes , הtable formats הם שכבה שעוזרת להתנהל עם האובייטקטים בdata lake שנורא מפוזרים, בצורה המזכירה טבלה בכך שמגדירים סכמות.
לדוגמה הHDFS הוא data lake, והhive tables הוא הtable format שלו, הוא מסדר את המידע בצורה טבלאית שמאפשרת להתנווט בקבצים (מבלי באמת לשמור את המידע). בין הtable formats הכי מפורסמים:
- הapache hudi : משתמש בHMS ומוסיף יכולות של טרנזקציות ACID , כלומר פעולות שנעשות הן אטומיות, עקביות ,שרידות ולא מקביליות. מאפשר לעשות time travel כלומר לתשאל סנאפשוטים ישנים, ומאפשר שכתוב של נתונים בטבלאות בשיטת COW וMOR.
- הiceberg : משתמש בREST catalog שמקביל לפרוטוקול הthrift שבHMS. הוא מאפשר טרנזקציות ACID, ניהול פרטישנים במקביל, שכתוב טבלאות, time travel ודוחס קבצים קטנים לקובץ אחד. הiceberg עובד בפורמט טבלאי והוא עובד עם מספר קטלוגים שונים, ביניהם יכול לעבוד גם עם HMS כקטלוג.
- הdeltaTable : מאפשר ACID, time travel ושכתוב טבלאות.

  שלושתם מתנהלים יותר מהר וביעילות על מקביליות של לקוחות. 

5. **Metadata & Transaction Log:**  How do modern formats store their own
   metadata?  Discuss the concept of a transaction log or manifest file, and
   the distinction between file level metadata (e.g. Iceberg data file footers)
   and catalog entries.  When would you even need to think about files if the
   catalog abstracts them away?  

גם iceberg גם hudi וגם deltalake כוךם מאחסנים את הmetadata שלהם בקבצים היררכים ומשתמשים בסנאפשוטס, manifest files וtransaction logs בשביל לאחסן את המטא דאטה.
בtransaction logs כל פעולה נרשמת כקובץ חדש בצורה אטומית (בדרך כלל כקובץ JSON), ובmanifest files בעצם שומרים קבצים שהם נתיב למיקום האחסון האמיתי של הקובץ. נגיד ויש לי פרטישן מסויים, אז יהיה לו manifest list ובו manifest files שמתעדים את רשימת הקבצים בפרטישן בעזרת נתיב לכל קובץ.
המטא דאטה של כל קובץ עצמו לא נשמר שם, אלא הוא נשמר בfooter של אותם קבצי parquet ובכללי אין עיסוק בdata files עצמם כי הם "מוחבאים" מאיתנו, רק אם צריך לעשות תיקונים, מחיקות או דברים שקשורים לפרטישן נתעסק בהם. 

6. **Interoperability & Ecosystem:**  Describe how catalogs and formats enable
   multiple compute engines to work on the same data (Spark, Trino, Flink).
   Why is standardization important?  What role do open specifications
   (e.g. Apache Iceberg spec) play?

   העובדה שהcatalogs והtable formats הם על layer אחר בopen table כלומר כל הכלים כמו ספארק וטרינו יכולים לגשת אליהם מאפשר להם לפנות לאותה טבלה אחת כדי לנווט בין קבצים.
   הקטלוג כתוב בסטנדרט בו כל המנועים כל עוד הם מבינים את המבנה והארגון יכולים להתמצא בו לא משנה מה השפה.

    *********************** שאלות סקילה ********************************************************
   1.מה ההבדל בין data warehouse קלאסי לhive? היעוד שלהם שונה, data warehouse קלאסי נועד לאסוף מידע מובנה בשביל ניתוח אנליטי בצורה נוקשה יחסית תוך שמירה על שלמות נתונים, ACID וכו... hive לעומת זאת נועד במטרה לתשאל כמויות גדולות של מידע (מובנה או לא מובנה) בצורת SQL, הנתונים בו לא חייבים לעמוד באותם תנאי סכמה שחייבים בdata warehouse משום שכשהם נטענים לHDFS או S3 אין שום קריטריונים, זה יכול להיות סרטון או טבלה.
   2. האם כל הקטלוגית תומכים בטרנזקציות ACID ובהרשאות? לא, גרסאות ישנות יותר של HIVE לדוגמה לא תומכות בזה. HIVE בפורמט קבצי AVRO/CSV/PARQUET לא ממשים טרנזקציות ACID.
   3. האם קטלוגים נוספים coupled לשכבת אחסון מסוימת? כן נגיד metadataIQ הוא coupled לoneFS (אחסון לנתונים לא מובנים), databricks unity catalogs מקושר לcloud object storage כמו AWS S3' GEN2 ועוד. הרוב לא (iceberg,hive ועוד מכילים קטלוגים שיכולים לעבוד עם HDFS, S3 ואחסונים אחרים אבל השימוש על האדופ מחייב שימוש באחסונים שעובדים עם האדופ)
   4. אם אני שומרת את הקבצים בפורמט txt האם יש footers? לא, אין את זה בשום פורמט שהוא human readable.
   5. באיזה סוג partition הhive תומך? horizontal partition (אופקי).
   6. מה ההבדל בין hash bucketing לhash partitioning? הhash bucketing קורא בתוצאות של hash partitioning, התהליך עצמו זהה.
   7. מה זה partition evaluation ? הערכה של האיכות של הפרטישנים כדי לוודא שההתנהלות היא באמת תקינה ויעילה , נעשה בכך שמודדים את איכות הפרטישנים, גודלם מספרם והpartition keys, ואת הסוג פרטישן. כלומר בדיקה שנבחר partition key אפקטיבי, מספר פרטישנים תקין ויעיל, וסוג פרטישן שמתאים לסוג נתונים.
   8. מתי אפשר להפעיל ACID בתור hive table formats עם HMS? כשיש גרסת hive לפחות של 0.14 , הטבלה חייבת להיות managed ולא external, וחייב להיות בה bucketing, הפורמט קצבים חייב להיות ORC.
   9. מה השכבות של הdata lakehouse? יש חמש שכבות עיקריות : - שכבת העיבוד בה מחלצים נתונים מכל מני מאכרים או אחסונים אחרים לlakehouse, בדרכ בעזרת שימוש בקפקה וכלים דומים - שכבת האחסון בה מאחסנים את כל הנתונים שחילצנו - שכבת המטאדאטה בה מאחסנים את כל המטא דאטה של הנתונים שמאוחסנים ודואגים לדברים כמו תמיכה בACID, גרסאות, caching וכל מה שקשור להתנהלות הנתונים וממשל עליהם - שכבת הAPI שמאפשרת לכלים אחרים לבצע שאילתות על הנתונים בעזרת אינטגרציה או API call - שכבת הצריכה שמאפשרת לכלים כמו power bi ועוד לגשת לגמרי לכל הנתונים ולמטא דאטה ולהשתמש בהם (בדרכ למטרות אנליטיות, תשאול ניתוח וכו) 

## Wrapping Up :trophy:
Review your answers with your mentor, focusing on how catalogs and formats enable a consistent data platform across tools.

## Action Items
- Identify catalogs or formats you’d like to try in practice.
- Prepare questions for the mentor Q&A session.
- Link these ideas back to the [intro chapter](../Chapter%200%20-%20Intro/1%20-%20Big%20Data%20Core%20Concepts.md).
### 📚 Resources
Use the resources listed below and practice searching the internet for questions not answered by the provided documentation.
- [Apache Iceberg Definitive Guide](http://103.203.175.90:81/fdScript/RootOfEBooks/E%20Book%20collection%20-%202024%20-%20F/CSE%20%20IT%20AIDS%20ML/Apache%20Iceberg%20(2024).pdf) Use this resource only for warehouse vs lake vs lakehouse (Iceberg will be learned on a different day)

