# Hadoop Distributed File System (HDFS) :elephant:

## Overview
This session focuses on the core concepts of HDFS, the distributed storage layer of the Hadoop ecosystem. Understanding its architecture will help you appreciate how big data clusters store and manage massive datasets across many machines.

**Study the key components, design decisions, and how they work together to provide fault-tolerant, scalable storage.**

## Goals
- Learn the architecture and roles of HDFS components (NameNode, DataNode, etc.).
- Understand how HDFS handles storage, replication, and availability.
- Practice planning a self-study day and managing your time.

:warning: **Note:**
- This is a self-study day; independence and time management matter.
- Focus on grasping the full picture of each concept; if you can’t explain it, you haven’t learned it.
- When in doubt, consult your mentor about what to study.

## Core Concepts

Consider the following five questions to cover the major HDFS topics:

1. **Architecture & Roles:**  Describe HDFS’s overall architecture, including NameNode(s), DataNodes, blocks, and how the namespace and metadata are managed. Don’t forget the role of ZooKeeper in coordinating HA and keeping track of leases.

הHDFS שומר נתונים על שרתים שונים (בדרך כלל 128MB לכל בלוק) ומשכפל את אותם בלוקים כדי לשמור עותקים שלהם למקרה של קריסה.
מי שמחבר את כל השרתים האלו הוא הNameNode ששומר בתוכו את כל הmetadata של המערכת, הוא שומר את השרתים המעורבים ואת מיקום הבלוקים בהם הFS שמורה 
בדרך כלל יש שני nameNodes, אחד פעיל ואחד בסטנד ביי והם אחראים על התקשורת מול הלקוח
והשיכפולים שלהם. הnameNode נשמר על מה שנקרא הnamespace server והוא מנהל שינויים במידע בתוך מה שנקרא edit logs שם נשמר metadata כמו מיקומי בלוקים או מצב הnode. את הedit logs הוא משתף עם הnameNode שבסטנד ביי כדי שלא יהיה פער בין מה שהם יודעים. 
הnamespace אחראי גם על הfsimage שזה מה שמחזיק בפועל את כל המיפוי של הבלוקים וקבצים.
הDataNode הוא שרת עליו שמורים מספר בלוקים ששומרים בפועל את המידע.
היחסים בין nameNode לdataNodes הם יחסי master-slave, הnameNode אחראי שהdataNodes יבצעו פעולות כתיבה - יוסיפו\יעדכנו קובץ בהתאם להוראות שהוא מוריד להן בעוד הdataNodes מטפלים בבקשות קריאהה ומבצעים את הוראות הnameNode.
כשאנחנו רוצים להוסיף dataNode אנחנו בעצם טוענים את הedit log לfsimage ויוצרים בלוקים חדשים לנתונים שהתווספו.
הzookeepr אחראי על שמירה על הnameNode תקין, הZKFC neck הודעות ping כבדיקה שהוא תקין, אם הnameNode קרס או קפא ולא מחזיר שולח הודעה אז הZKFC נכנס למצב של כשך ומפעיל את הnameNode הסטנדביי ומבצע בחירות לnameNode שני. ככה תמיד הnameNode נמצא בHA ובכך שהnameNode תמיד פועל, יש רק קודקוד אחד שאחראי על פעולות כתיבה. 

2. **Storage & Fault Tolerance:**  Explain how HDFS divides files into blocks, uses replication (default factor three), and how it detects and recovers from node failures.

הHDFS מחלק קבצים לבלוקים של 128MB, כל בלוק בהגדרה הדיפולטיבית משוכפל 3 פעמים.
כל node אחראי לשלוח לnameNode הודעת heartbeat שמדגישה שהכל תקין, אם לא קיבלנו הודעה כזאת הnameNode ישים לב שיש תקלה, הוא יבדוק איזה בלוקים משוכפלים פחות מהמינימום בצריך ויעתיק אותם לnodes בריאים.
אם היינו באמצע כתיבה אז קודם נפתח כתיבה עם node בריא ואז נדאג להעתיק הכל לnode חדש.

3. **Topology Awareness & Performance:**  What is rack awareness and why does HDFS replicate across racks? Discuss how block placement, snapshots, and checksums contribute to performance and data integrity.

השיטה בה אנחנו מחלקים את העתקי הבלוקים היא נורא חשובה, ההמלצה על כל בלוק היא:
לשים בלוק אחד בnode של הלקוח
לשים בלוק שני בnode שנמצא בrack אחר
לשים בלוק שלישי בnode שנמצא באותו rack (לא אותו node).
הrack זה בעצם cluster של כמה nodes שתלויים באותו סוויץ'.
כל node ממופה לrack והמיפוי נשמר בnameNode, הניהול הזה גורם לכל שאם סוויץ' כשל לא מאבדים את כל העותקים, וגם יש גישה מהירה לנתונים ששמורים בrack של הלקוח.
לזה קוראים rack awarness, לפי המיפוי השרת מחליט איפה לצרף nameNodes כדי להתחשב בגישה מהירה אבל גם לא להעמיס על rack ולהפחית תעבורה.
הfsimage שומר snapshots של הFS ובכך בודק שהנתונים שלמים ואין חוסר התאמה בין נתונים כשמעבירים nameNode.
דבר נוסף ששומר על אמינות נתונים הוא הchecksum, שהוא מספר שמסמל את כמות הספרות הנכונות בבלוק, זה מועבר כל פעם והdataNode מאמת שהוא זהה לבלוק שניתן לו, וגם הלקוח מאמת שהמידע שהועבר לו תואם לchecksum ששמור.


4. **High Availability & Federation:**  Outline HDFS High Availability (Active/Standby NameNode, JournalNodes) and Federation (multiple namespaces). How do these features improve scalability and uptime?

כמו שהוסבר מקודם, הActive/standby nodes מאפשרים זמינות גם במקרה שהפעיל קרס משום שהקודקוד בסטנד ביי זמין לפעולה.
הjournal nodes הוא חבורת קודקודים שאחראים על ניהול הedit logs בnamespace, והם מאפשרים עדכון של הסטנד ביי. הnameNode חייב לכתוב לרוב הקודקודים.
הFederation הוא מצב בו יש כמה namespaces כדי להוריד עומס משרת אחד (scalability), כל הdatanodes מתקשרים עם כל הnamespaces ועונים להוראות של כולם.

5. **Protocol & Operations:**  Describe how clients read and write data to HDFS via RPC, how they locate NameNodes and DataNodes, how DataNodes send block reports, and why these mechanisms matter for everyday operations. Cover the runtime behaviour of leases and pipeline formation.

בקשות קריאה:
הלקוח מבקש לפתוח קובץ, הdataNode שמחזיק בקובץ
כדי לבצע קריאה לHDFS הלקוח צריך לפתוח חיבור עםהnameNode בTCP, ואז הוא יכול לתקשר עם הnameNode בעזרת הRPC.
פרוטוקול הRPC מאפשר את התקשורת בכך שהלקוח שולח בקשת RPC והnameNode מכניס אותם לתור.
כשהnameNode מגיע לבקשה הוא מוצא את האינדקסים של הdataNodes שמכילים את הבלוקים של הקובץ, והם מחזירים FSDataInputStream ללקוח (המשך של dataInputStream, מאפשר הרבה בקריאה).
הלקוח עושה read() כדי לקרוא את הקובץ, הdataNode הראשון יזרים לו את הקובץ ואז אוטומאטית יחפש את הdataNode הבא הכי קרוב להזרים לו ממנו את הבלוק הבא.

עבור כתיבה הלקוח עושה create() ושולח בקשת RPC לnameNode ששוב מכניס זאת לתור.
הnameNode בודק שללקוח יש הרשאות ושאין כבר קובץ כזה ושולח FSDataOutputStream ללקוח שיתחיל לכתוב.
הקובץ מתחלק לבלוקים שנכנסים לdataQueue בDdataStreamer שמעתיק אותם לdataNodes הראשון ומשם הראשון מעתיק לשני והלאה ואז חוזר אישור ACK אחורה' זה נקרא הpipeline formation.

אם רוצים לשנות קובץ - אי אפשר, אפשר לעשות append לסוף הקובץ.

גם הblock reports נשלחים עם RPC, ביחד עם רשימה של כל העתקי הבלוקים שיש בdataNode הזה כדי לשמור על שלמות הנתונים. שולחים את זה כשהקודקוד נוצר, כשהתווסף או נמחק ממנו קובץ, וכשצריך לשלוח heartbeat.

הlease מבטיח לנו שרק לקוח אחד יכול לפתוח קובץ כל פעם, בעצם כל פעם שהלקוח יוצר קובץ או עושה אפנד אנחנו "מסמנים" את הקובץ ושמים עליו lease ונבקש לחדש אותו כל פעם. כל עוד הקליינט כותב ימשיכו לחדש את הlease , אחרת אם הלקוח לא מגיב אחריי תקופת זמן מסויימת קצרה יחסית לקוח יכול לקחת גישה לקובץ ואם הוא לא מגיב אחריי משך זמן גדול יותר ולקוח אחר לא לקח את הקובץ אז המערכת תסגור אותו בכוח.


*********** הערה**************************
- הHDFS זה מערכת קבצים מבוזרת של hadoop שפרוסה על שרתים שונים באיזורים שונים ונועדה לאחסן קבצים גדולים מאוד.
  




## Wrapping Up :trophy:
Review your answers with your mentor and discuss any unclear points. Relate these concepts back to real-world usage scenarios you might encounter.

## Action Items
- Note topics you want to investigate further.
- Prepare questions for the mentor Q&A session.
- Continue the Day 01 challenge by linking these HDFS concepts to other chapters.

## Recommended Resources
- [Official HDFS User Guide](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html)
- *Hadoop: The Definitive Guide* (O'Reilly) – chapters covering HDFS architecture and administration.

