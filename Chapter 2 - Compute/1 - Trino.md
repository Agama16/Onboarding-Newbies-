# Introduction to Trino 🐰

## Overview
Today’s session introduces Trino, a distributed SQL query engine designed for high-performance analytics across multiple data sources. Unlike traditional databases, Trino does not store data itself. Instead, it queries data where it already resides, enabling fast interactive analysis across large and diverse datasets.

**The emphasis is on Trino’s architecture, distributed execution model, and how it integrates with modern data platforms.**

## Goals
- Understand what Trino is and where it fits in a modern data architecture.
- Learn how Trino executes distributed queries across workers.
- Explore how Trino connects to multiple data sources and federates queries.
- Improve your ability to research distributed data systems independently.

:warning: **Note:**
- This is a self-study day; independence and time management are crucial.
- If you can’t explain a concept clearly, you probably need to revisit it.
- Ask your mentor if you’re unsure what to research.

### ⏳ Timeline
Estimated Duration: 3 Days

- Day 1: Learn the fundamentals of distributed SQL engines and Trino’s role in the data ecosystem.
- Day 2: Dive deeper into Trino architecture, connectors, and query execution.
- Day 3: Review performance optimization and operational concepts, followed by a Q&A session.

---

## Core Concepts

### Part 1: Distributed SQL Engines (General Concepts)

Answer these questions to understand the broader category of distributed query engines before focusing on Trino specifically.

1. **Role in the Data Architecture:**  
   What is a distributed SQL query engine, and where does it sit in a modern data architecture? How does it differ from storage systems such as data lakes or databases?

2. **Motivation & Use Cases:**  
   Why do organizations use distributed SQL engines? In what scenarios are they preferred (for example: interactive analytics on large datasets, federated queries across multiple systems, or querying data lakes)?

3. **Distributed Query Processing:**  
   How do distributed query engines typically execute queries across multiple nodes? Explain concepts such as parallel processing, data shuffling, and shared-nothing architectures.

---

### Part 2: Trino (Implementation & Operations)

Answer these questions to cover Trino’s major architectural and operational concepts.

1. **Purpose & Position in the Data Stack:**  
   What is Trino, and where does it sit in the data architecture? Explain its role as a distributed MPP SQL engine, how it differs from storage systems, and when it should be used instead of other query engines.

טרינו הוא מנוע לעיבוד שאילתות שנוצר בשביל לתת מענה לאיטיות של hive, הוא פותח במטרה לתת יכולת לבצע שאילתות מהירות (במילישניות) על כמויות גדולות של נתונים ובאופן מבוזר.
הוא מהווה כשכבה נפרדת מעל האחסון, סוג של קומפיילר, הוא לא מאחסן את הנתונים בעצמו אלא מקבל את השאילתה, מריץ אותה ומחזיר תשובה בעזרת שכבת המטא דאטה הנפרדת ושכבת האחסון הנפרדת.
טרינו תומך בכתיבות בזיכרון ולא לדיסק ובגלל זה הוא משמעותית יותר מהיר ממנועים אחרים כמו הייב, נוסף על כך הוא מנוע MPP, כלומר הוא תומך בהרצת משימות במקביל כדי ליעל תהליכים.
טרינו מאפשר להשתמש בכמה אחסונים במקביל ולהריץ שאילתה על כולם במקביל, ולכן מהיר משמעותית משאר המנועים.

2. **Architecture & Query Execution:**  
   How is Trino architected, and how does it execute queries in a distributed environment? Discuss the roles of the Coordinator and Workers, stages and tasks, data exchanges, and the execution model.

טרינו בנוי כך:
- הcoordinator : שרת שמנהל את הworkers, בונה את התכנון הלוגי של שאילתה וממתזמן אותו על הworkers ועוקב אחריי פעילותם, הוא מקבל את התוצאה הסופית מהworkers ומחזיר ללקוח והוא גם מקבל את השאילתה מהלקוח. הקורדינטור בנוי מהparser, הanalyzer, הplanner שעושה תכנון דינאמי DAG ומהschedualer שעושה תזמון למשימות. 
- הworkers : שרתים שמריצים taskים. כל תוצאת ביניים הם מעבירים אחד לשני וכותבים לזיכרון.
- הקטלוג : ממנו לוקחים את המטא-דאטה כדי לדעת איפה הנתונים שצריך
- הקונקטור : מה שמחבר אותנו לקטלוג, פונה למטא דאטה ולנתונים
- הדרייבר : חיבור ללקוח, JDBC לדוגמה, זה לא חובה אפשר גם לפנות ב trino CLI / python client / node.js client ועוד.
- הקלאסטר : בנוי מקורדינטור אחד ועובדים, עליו שאילתה תפוזר.
השאילתה בנויה כך:
- הstatement : השאילתה ממש מאיך שהיא ניתנה.
- הquery : שאילתה אחריי פירוק לעץ AST לפי פעולות עיקריות.
- הstage : פירוק משימה עיקרית לשלבים. רצף של taskים שצריך לעשות.
- הtask : משימות נפרדות, מפורטות יותר.
- הsplits : פירוק המשימות לnodes שונים לפי הדאטה שעליהם.
- דרייבר : הworkers מתקשרים בעזרת דרייבר שמעביר ביניהם מידע ביניים.
- אופרטור : פעולות בסיסיות, עושה consuming/ producing על התוצאות.

3. **Connectors & Catalogs:**  
   How does Trino integrate with external systems through connectors and catalogs? Explain what connectors are responsible for, how catalogs are configured, and how Trino can federate queries across multiple data sources.

לטרינו יש אינטגרציה מצויינת עם מערכות חיוניות בעזרת קונקטורים וקטלוגים.
בקטלוג מדובר על כל קטלוג שאנחנו מכירים (לא כולם אבל הרבה) iceberg, hive וכו.. או קטלוג מותאם אישית.
הקונקטורים הם מה שמחבר את הmanager של טרינו לקטלוג עצמו, הוא מוגדר כproperty בקטלוג ודרכו מועבר כל המטא דאטה שצריך מהקטלוג.
קטלוג מוגדר בתיקיית /etc/catalog/ כנגיד /etc/catalog/hive.properties/ .
בגלל שטרינו יכול לעבוד על כמה סוגי אחסון במקביל, הוא יכול לנהל כמה קטלוגים במקביל, ולכל קטלוג קונקטור משלו.
שאילתה אחת יכולה לרוץ על כמה שטחי אחסון במקביל, זה נקרא federate queries. פונים בעזרת כמה קונקטורים לכמה קטלוגים בשביל מטא דאטה שצריך.

4. **Governance & Workload Management:**  
   How does Trino handle governance and workload management? Discuss resource groups, concurrency control, memory limits, access control (RBAC), and multi-tenant isolation.

טרינו מנהלת resource groups, כלומר הקצאת משאבים לשאילתות, ככה נפטרים מבעיית הnoisy neighbours כששאילתה לוקחת יותר מדיי משאבים וזה בא על חשבון שאר השאילתות.
הטרינו דואג להגביל חיבורים במקביל (להגביל חיבורים של דרייברים לtask במקביל), מגבילה את הזיכרון שמוקצה למשימה\שאילתה עם הresource groups.
הaccess control בטרינו מתחלק:
אותוריזציה נעשית ע"י קרברוס\LDAP .
אפשר לעשות אימפלמינטציה לכמה מערכות access contro במקביל ומחולקות ל:
- allow-all : כל הפעולות מורשות
- read-only : רק פעולות שדורשות קריאה מהמטא-דאטה
- file : הקובץ קונפיג מקצה מה מותר ומה אסור
- OPA: יש תפקידים מוגדרים ולפיהם יש הרשאות ליוזרים
- ranger : שימוש בapache ranger



5. **Query Optimization & Performance:**  
   How does Trino optimize query performance? Explain cost-based optimization, statistics usage, join strategies, predicate pushdown, partition pruning, spilling, and caching behavior.

אופטימיזציה לסביבת טרינו:
עושים scale out ודואגים ליחס תקין בין CPU וזיכרון לworkers
בעזרת caching ובעזרת שמירת matirialized views (שמירה של התוצאות של queries).
לטרינו יש cost-based optimization שדואג לעשות תכנון DAG באופן דינאמי, כלומר הוא מתכנן את מבנה המשימות הכי טוב בהתאם למה הכי "זול".
הוא עושה שימוש בסטטיסטיקות , שזה הסטטיסטיקה שרשומה בקבצים עצמם, לפיהם הוא מחשב כמה יעיל כל תכנון יהיה.
דבר נוסף אליו הוא מתייחס זה הjoin strategies זה מתחלק ל:
- הdistributed join : לפי פרטישן מסויים עושים ביזור לטבלאות על גבי הnodes, כלומר כל node יקבל חלק מהטבלה המלאה לפי קריטריון מסויים עליו יעשו JOIN.
- הbroadcast join : כל node לוקח את הbuild side (החלק של הטבלה הקטנה יותר) שאצלו ושולח אותה לכל שאר הworkers, ככה לכולם יש עותק של הטבלה אצלם.
אופטמיזציה נוספת היא predicate pushdown בה עושים פילטר לרשומות בטבלה עוד בdata source.
כדי לא לעשות kill אוטומאטית לשאילתה שצריכה יותר משאבים ממה שיש בזיכרון, לפעמים עושים spilling (במצב של FTE) בו רושמים את המידע בזיכרון לדיסק כדי שיוכלו להמשיך לכתוב לזיכרון.





6. **High Availability & Multi-Cluster Routing:**  
   How does Trino Gateway enable high availability and workload isolation across multiple Trino clusters? Explain how it provides a single entry point, performs rule-based query routing and load balancing, monitors cluster health, and enables failover and multi-cluster isolation beyond what a single Trino coordinator can support.

בטרינו רגיל לכל קלאסטר יש URL, דרכו הלקוח יכול להתחבר ולראות את הקלאסטר, זה דורך קונפיגורציה שונה לכל קלאסטר בצד לקוח.
טרינו gateway מאפשר להשתמש בURL אחד לכל הקלאסטרים. (single entry point).
הוא מתנהל כload balancer (כלומר שומר על איזון בעומסים בין הקלאסטרים), כproxy (מנטר תעבורה שנכנסת לאתר) וכrouting gateway (מנטב שאילתות).
טרינו תומך בHA , בעזרת שמירה של שני קלאסטרים זהים, הוא מחלק את העבודה ביניהם וברגע שקלאסטר אחד נפל אפשר להפנות את העבודה לקלאסטר השני אוטומאטית.
טרינו מפנה את הבקשות לresource groups, שהן קבוצות של קלאסטרים שהמשאבים שלהן מוקצים לשאילתות שמופנות אליהן.
כשטרינו מפנה שאילתה לקלאסטר בדרכ היא תפנה לrouting-group שנמצא בheader של הבקשה.
קיים routing-rule-engine שמאפשר להכתיב לוגיקה להפניית שאילתות, בנוסף החוקים כתובים בקובץ מקונפג.
כל חוק שכל התנאים שלו התקיימו מבוצע, והם מתייחסים ליוזר, לdata source, ולטגים.
אפשר לעשות routing logic דינאמי מותאם בעזרת external service שזה בעצם API endpoint.
אפשר לבצע שרק חוק אחד יתבצע כל פעם, אבל זה קשה יותר, לכן יש rules priority:
נותנים לכל חוק ערך מספרי, ככל שהוא יותר נמוך החוק יתקיים יותר, אם כמה חוקים עונים על הדרישות כל אחד ידרוס את מי שהתקיים לפניו.
טרינו גם בודקת אם הבקשות קשורות לבקשות קודמות ואם כן שולחת אותם לאותו resource group.
בresource group עצמו בדרך כלל בחירת הקלאסטר תעשה לפי RR או אדפטיבי (תשלח למי שהכי לא עמוס).
הresource groups מוגדרות בטבלה בדאטה בייס בשם resource group manager.
טרינו מסווגת את הקלאסטרים בכך שהיא מסמנת אותם:
- כHEALTHY : הקלאסטר רץ ומקבל שאילתות
- כUNHEALTHY : הhealth check חזר שהקלאסטר לא מתפקד, לא יופנו אליו שאילתות.
- כPENDING : הקלאסטר בהקמה עדיין, לא יופנו אליו שאילתות.
בבדיקות האלו מבררים כמה worker nodes עובדים , האם יש שאילתות רצות, האם יש תור לשאילתות וכו...
דרישות לטרינו gateway:
- תמיכה בjava 25
- דאטה בייס של mySQL/PostgreSQL/Oracle a שם מאחסנים מצבי קלאסטרים, היסטורית שאילתות וכו...
- קלאסטר טרינו ותמיכה בJDBC וREST API
- הגדרת http-server.process-forwarded=true

  התקנה :
  בונים קובץ jar בשם gateway-ha.jar עם כל הrouting rules וכו נשים אותו בdirectory ונוסיף לשם גם את config.yaml.
  או בעזרת דוקר עושים Pull לdocker image ומקשיבים להוראות הגיט.

  טרינו gateway תומך בUI pages הבאים : dashboard, cluster, resource group, selector, history, history, routing-rules .
  
   מצבי שאילתה בUI:
  QUEUED - מחכה לרוץ
  PLANNED - בתכנון
  STARTING - מתחילה הרצה
  RUNNING - יש משימה שרצה
  BLOCKED - מחכה למשאבים
  FINISHING - בתהליכי סיום
  FINISHED - הסתיים
  FAILED - נכשל
---

### 🔄 Alternatives
Assignment: You are required to research and write a comparative analysis between Trino and an industry alternative.

- Deliverable: A written summary (minimum 1–2 paragraphs).
- Add a real-life use case.
- Focus: Compare performance, architecture, and specific "pain points" this tool solves compared to legacy systems or competing technologies.
- Goal: You must be able to justify why the department uses this tool for our specific environment.

---
### 🎯 User Story & Scenario
Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.
- Deliverable: A written summary example/story (two paragraphs approx.).
- Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.
- Data Flow: Map out the data flow and explain how this tool integrates with other components in the Data Pipeline.
---
********************* שאלות סקילה ********************************************************8
1. איזה דיאלקט SQL משתמשים ? ANSI SQL.
2. איזה קליינטים עובדים עם טרינו? דרייברים (JDBC), טרינו CLI , הpython client , node.js.
3. השם של הרכיב בקורדינטור שמדבר עם הworkers? הdiscovery service
4. מה זה אופרטור? כמו בc++, סימן שעושה פעולה (consumer / producer ).
5. מה זה serDe ואיך זה בעייתי עם views ? זה מה שעושה תרגום מהאחסון ממש לmap reduce (לבינארי).
6. הbroadcast Join : במקום שכל worker ישמור את הbuild side של החלק שלו בלבד, הם שולחים את החלק שלהם לכל שאר העובדים. זה טוב כדי להימנע מdistributed join וכשאין פרטישנים או באקטים. ורק כשהטבלה בbuild side קטנה.
7. מהו מנגנון לכשל worker (הfault tolerance execution) ? הFTE הוא מנגנון לכשל, ברגע ששאילתה או משימה קורסים אפשר להריץ אותם שוב, הFTE דואג שיעשו spooling (כלומר ישמרו מידע ביניים על הדיסק) כדי שלא יצטרכו להריץ את הכל מחדש.
8. איך מגדירים קטלוג? בעזרת SQL: עושים CREATE CATALOG XXX USING connectorXXX... או בעזרת התיקייה /etc/catalog/xxx.properties . מגדירים סטטי או דינאמי.
9. למה הquery מתפרק? לdistributed query plan שזה הlogical plan (איך הquery ירוץ) והinterconnected stages שזה האימפלמינטציה הפיזית של זה על הרכיבים שמבצעים את הDAG, סדרה של stages מחוברים על כל worker. 

************************* שאלות סקילה 2 **********************************
1. מה עוד מקביצים בresource groups חוץ מCPU וmemory? מספר השאילתות שיכולות להתקבל במקביל.
2. באיזה קובץ קונפיגורציות מגדירים acl? בקובץ /etc/access-control.properties?
3. איזה אחוז memory מוקצה לJVM? בערך 70% מהheap של node.
4. איזה עוד סוגי caching יש? חוץ מהשמירת קבצים הלוקלית שיש, יש spooling protocol שעל גבי object storage יש שמירה של תוצאות של שאילתות באחסון.
5. מה רואים בדשבורד? סטטיסטיקות - גרסה, רשימת nodes פעילים, שאילתות פעילות וכו..
6. מה ההבדל בין ANALYZE לEXPLAIN לEXPLAIN ANALYZE? הEXPLAIN היא פקודה שמראה את התכונים הלוגי לשאילתה והעלות שלהם, ANALYZE מראה את הסטטיסטיקות לפיהן חישבו עלויות כמו כמות שורות עמודות וכו..., EXPLAIN ANALYZE מבצעת את השאילתה ומביאה ממש את התכנון הלוגי שנעשה עם העלות שלו והסטטיסטיקות מהביצוע.
7. איך משנים את הjoin strategy? בעזרת SET SESSION join_distribution_type משנים לbroadcast או כל סוג אחר.
8. איך לא לבזבז משאבים כשאין שאילתות? אפשר לעשות scaling בעזרת קוברנטיס ובכך להפחית/להגדיל את כמות הworkers בהתאם לכמות השאילתות ואיתם לשחרר/להגדיל משאבים כדי לא לבזבז אותם כשאין "עבודה".
9. איך מונעים ספאם של שאילתות?  הגבלת פעמים ששאילתה יכולה לרוץ, והגבלת זיכרון לשאילתות.
10. מה ההבדל בין שאילתה finishing / abondend ? שאילתה finishing היא שאילתה שמסתיימת (המשימות נסגרו והתשובה מוחזרת ללקוח), שאילתה abondend היא שאילתה שבה לא היה תקשורת עם הלקוח מעבר לtimeout מוגדר.
11. איך יודעים שהאופטימיזציה עבדה בטרינו? עושים EXPLAIN ANALYZE , יראה גם את כל התכנונים הלוגים וגם את מה שבוצע בפועל בשאילתה.
12. איך מחליפים איזה קלאסטר הוא אקטיב?
13. למה הטרינו לא מחליף רגל אוטומאטית?
14. מה שני סוגי הFTE ומה היתרונות וחסרונות שלהם? יש שני סוגי retry, אחת לשאילה שמריצים אותה במקרה שהייתה תקלה על worker node, מומלץ כשהשאילתות קטנות יחסית היתרון של זה זה הרצה מהירה יחסית לשאילתות קטנות אבל אם הן גדולות מדיי זה latency ובכללי לחזור על תהליך יחסית ארוך, ויש task retry שמריץ רק משימה ספציפית אחת שנכשלה, מומלץ כשיש שאילתות גדולות או עיבוד מסגנון batch היתרון הוא שהretry יהיה מהיר יותר ולא דורש את כל התהליך עם המשאבים והתעבורה מחדש, החיסרון הוא שאם השאילתות קטנות ועושים הרבה retry task זה יכול לגרום לhigh latency שיקח יותר זמן מהרצת כל השאילתה.
## Wrapping Up :trophy:
Go over your answers with your mentor and clarify any uncertainties. Relate Trino concepts back to the broader data platform and how distributed query engines interact with storage systems and processing frameworks.

---

## Action Items
- Identify Trino topics you want to explore further.
- Search examples of industray usage of Trino.
- **Bonus** - what is the rabbit's name?
- Prepare questions for the next mentor Q&A session.

---

## Recommended Resources
- [Official Trino Documentation](https://trino.io/docs/current/) – the primary reference guide.
- [Trino: The Definitive Guide (O'Reilly)](https://dokumen.pub/trino-the-definitive-guide-sql-at-any-scale-on-any-storage-in-any-environment-2nbsped-109813723x-9781098137236.html)
- [Official Trino Gateway Documentation](https://trinodb.github.io/trino-gateway/)
