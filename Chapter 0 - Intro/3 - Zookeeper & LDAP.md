# Zookeeper, Kerberos & LDAP :lock:

## Overview
This session focuses on the components that provide coordination and authentication in distributed systems.  Zookeeper acts as the lightweight coordination service, while Kerberos and LDAP handle secure identities and directory information.  These technologies are commonly paired in Hadoop and other big‑data ecosystems.

**Study the key components, design decisions, and how they work together to enable secure, reliable clusters.**

## Goals
- Learn Zookeeper’s architecture and core features.
- Understand the Kerberos authentication flow and the purpose of LDAP directories.
- See how these systems integrate with each other and with Hadoop.
- Practice organizing a self‑study day and managing your time.
- Prepare to discuss your findings with your mentor.

:warning: **Note:**
- This is a self‑study session; independence and time management are critical.
- Focus on grasping the full picture of each concept – if you can’t explain it, you haven’t learned it.
- When in doubt, ask your mentor which topics deserve deeper attention.

## Core Concepts

### Zookeeper – five guiding questions
1. **Architecture & Data Model:**  Describe a Zookeeper ensemble, the role of the leader and followers, the znode hierarchy, and how znodes store data and metadata.

במערכת נורמטיבית, העבודה והנתונים מתחלקים לכמה שרתים במקומות שונים (DFS), הzookeeper הוא כלי שפועל על המערכת שמוודא שכל השרתים (NODES) בה מודעים אחד לשני ומסונכרנים אחד עם השני. הוא עושה את זה בעזרת עץ היררכיה בה לכל קבוצת נתונים קוראים Znode.
בעץ יש את הקודקוד הראשי שהוא הroot Znode, מכל קודקוד יש קודקודים המסתעפים ממנו שהם הfollowers שלו והוא הleader שלהם.
מהcluster של השרתים נבחר שרת שיהיה leader וכל השאר הם הfollowers שלו.
בכל פעם שהleader מקבל בקשה לכתיבה הוא עושה את השינויים ושולח את העדכונים לכל העוקבים שלו בעזרת הatomic broadcast והfollowers אחראים לכתיבה.
במקרה ששרת שהוא לא הleader קיבל בקשה לכתיבה הוא יעביר אותה לleader שיכתוב ויעביר את העדכון לכולם.
כמובן שלכל השרתים יש עותק של הZtree.
לכל Znode יש בעצם דאטה בייס שבו הוא מעדכן (וגם בFS לגיבוי במקרה של תקלות) והוא יכול להכיל עד 1MB של מידע, הZnode מכיל גם את הPATH מהroot node עד לנוכחי, מי מורשה גישה לZnode הזה ועוד מטה דאטה כמו זמן מספר גירסה וכו..
בשביל ensemble צריך לפחות 3 שרתים (מומלץ 5 לפחות), שרתי הensemble שמספקים שירות ללקוחות דואגים גם לשכפול המידע ביניהם כדי להימנע מאיבוד מידע.
סוגי Znodes :
- הPersistence - נשארים עד שמוחקים אותם.
- הEphemeral - נשארים עד שהחיבור לקוח מת, נגיד כשנעשה ping scan אז כל הוסט ישלח לנו את הIP שלו וברגע שחיבור עם הוסט מסויים יתנתק הZnode שלו ימות כי אין בו צורך יותר.
- הsequential - יכולים לשמש כגם וגם, יש להם מספר סידורי של 10 ספרות, כשצריך לבחור znode שיהיה leader נבחור את זה עם המספר הסידורי הקטן ביותר.
בעזרת הzookeeper לכל השרתים יש אמת אחת שהם יכולים לסמוך עלייה, וזה גם מספר גיבוי טוב במקרה שאחד מהם נופל, כי כולם מודעים למצב של הכל.
- 

2. **Consistency & Watches:**  How does Zookeeper guarantee sequential consistency?  Explain watches, one‑time triggers, and how clients use them for cache invalidation.

הzookeeper שומר על תיאום בין כל השרתים, אם znode עשה עדכון, בכל השרתים האחרים זה גם יעודכן.
אחד מהדברים שעוזרים לעקביות בzookeeper זה הwatch, בעזרתו הלקוח יכול לעקוב אחריי Znodes אחרים ולקבל עדכון כשהם השתנו ובכך למנוע עיקובים ולהתעדכן במהירות.
כשאנחנו מגדירים watch, הוא מוגדר לפעם אחת, כלומר רק לעדכון אחד אנחנו נקבל התראה ואז נצטרך להגדיר את הwatch שוב אם נרצה, זה נקרא one time trigger זאת על מנת שנימנע מעומס התראות, אחריי שקיבלנו התראה אחת על שינוי ועד שנעשה שינוי לznode (ההתראה לא כוללת מה העדכון, עדיין צריך לעשות שאילתה כדי לקבל את המידע) המידע יכול להשתנות עוד הרבה פעמים ואנחנו לא רוצים לקבל התראות על כל הפעמים האלה.
ככה אנחנו תמיד שומרים על המידע בcache מעודכן ושהעץ לא יהיה "מאחור".



3. **Sessions & Failure Handling:**  What is a Zookeeper session, how are heartbeats maintained, and what happens when the session expires?  Discuss how ephemeral and sequential nodes relate to this.

הsession הוא בעצם חיבור של הלקוח לensemble, הוא מתחיל כשהלקוח מתחבר לzookeeper ונגמר כשהוא מתנתק או כשיש session timeout.
לכל session יש session id (מזהה של 64 ביטים), בו הם משתמשים בזמן התקשורת ביניהם.
הלקוח הוא זה שקובע את הtimeout, וברגע שאין שום תקשורת מהלקוח לשרת (heartbeat) אז השרת הוא זה שחותך את הקשר ומסיים את הסשן, השרת מצפה לאיזשהו heartbeat במהלך הסשן כדי לדעת שהלקוח עדיין מעוניין בתקשורת איתו.
בשלב זה ephemeral nodes ימותו וימחקו לגמרי, הsequential nodes אם הם מסוג ephemeral sequential ימותו גם אבל אם הם מסוג persistent אז ישארו בחיים.

4. **Common Patterns:**  Explain how leader election, distributed locks, and configuration storage are implemented on top of Zookeeper primitives.

בzookeeper בחירת מנהיג תלויה בהסכמה של הרוב 
לכל znode שהוא מסוג ephemeral sequential יש מספר סידורי, כשznode שהוא הleader נמחק, נוצר znode בשם election שמתחתיו שמתחתיו יש קודקודים של כל המשימות שצריכות leader ש"מציעות" את עצמן להיבחר ולכולן יש מספר סידורי. הznode עם המספר הסידורי הקטן ביותר יבחר להיות הleader.
איך שומרים שלא 2 שרתים עובדים על אותו משאב ביחד? בעזרת distributed locks.
באופן דומה לבחירת הleader, יש לנו קודקוד בשם lock, וגם לו כל לקוח יצור ephemeral sequential node עם מספר סידורי שעולה. הקודקוד עם המספר הסידורי הקטן ביותר יש לו גישה למשאב וכשהקודקוד הזה ימות הקודקוד עם המספר הכי קטן הבא יקבל גישה (מין FIFO כזה).
בzookeeper הכל מסודר לפי בnodes כמו תיקיות ממש כמו FS, גם ההגדרות configurations שמורות בקובץ zoo.cfg שם יש את המספר מזהה של השרת , snapshots (העץ) ועוד הגדרות. 

5. **Operational Concerns:**  Outline how to deploy an ensemble, handle scaling, manage snapshots and transaction logs, and troubleshoot typical issues (e.g., split‑brain, latency).

   בשביל לבנות ensemble, נבחר במספר אי-זוגי של שרתים (מומלץ אי זוגי בשביל הקונצנזוס).
   ההגדרות הן בzoo.cfg ושם נגדיר גם מי השרת מאסטר וניתן שמות לשאר (נגדיר IP ועוד פרטים).
   צריך לתת לכל שרת מספר מזהה מיוחד ואז לאתחל את העצים של כל אחד.
   ניהול מהסוג הזה של השרתים מונע את בעיית הsplit brain, בעיה בה השרתים ברשת מתפצלים ל2 קבוצות שאינן מתקשרות ואז לא מעדכנים אחד את השני בעדכונים. בzookeeper יש querom, כלל של רוב שחייב להיות התלוי בגודל השרתים הכולל, Q=N/2 +1 אז אם נגיד יש 5 שרתים והם התפצלו לקבוצה של 3 ו2, הזוג שרתים לא יוכלו לתפקד כי הם לא עומדים בדרישה הזאת, ורק ה3 יבצעו פעולות כתיבה. 
   אפשר להוסיף עוד שרתים שאינם מאסטר, זה נקרא scaling, אנחנו יכולים להוסיף שרתי followers שיעזרו בקריאת בקשות ושמירת נתונים , או observers שגם עוזרים בקריאת בקשות אבל אינם "חלק" כלומר הם לא בוחרים מאסטר חדש בבחירות ולא יכולים להיבחר, וגם אין להם שום חלק בכתיבה.
   על כל כתיבה שנעשתה בעץ, השרת פותח transaction log, תיעוד של השינוי שנעשה. אחריי כמות מוגדרת מראש של transaction logs אנחנו יוצרים snapshot , השרת מתעד את כל העץ כמו שהוא ושומר אותו לוקלית כדי להימנע מאיבוד מידע במקרה של קריסה.
   בגלל שרק שרת אחד אחראי על פעולת כתיבה וצריך לחכות לאישור של כל השרתים האחרים, יכול להיות latency גבוה מאוד, בגלל זה צריך למצוא איזון בין מספר השרתים followers לבין כמות הבקשות והמידע, כדי שיהיה יעיל אבל לא יכביד מדיי עד כדי שהפעולות לוקחות מלא זמן.
    
   
   

### Kerberos – five guiding questions
1. **Protocol Flow:**  Walk through the Kerberos authentication flow from initial login (kinit) to obtaining service tickets.  Include AS, TGS, and ticket caches.

הkerberos הוא כלי לאותנטיקציה ברשת שאינה בהכרח בטוחה.
איך האותנטיקציה נראית?
יוזר מסויים שולח בקשה מוצפנת בעזרת הkinit (פקודה בקומנד ליין) להשתמש באיזה service מסויים, שבה יש את השם משתמש שלו, המזהה של הservice בו הוא רוצה להשתמש ואת הIP שלו וכמה זמן הם רוצים לTGT בשביל אותנטיקציה.
עם kerberos הבקשה מגיעה לKDC של הrealm שבו היוזר נמצא, בKDC השרת אותנטיקציה (AS - authentication server) בודק שהיוזר באמת מוכר לו ושולח לו TGT שזה כרטיס לבקש כרטיס מהשרת כרטיסים ביחד עם הזמן סשן של הTGT (לא חייב להיות מה שהלקוח ביקש).
הAS שולח בסהכ 2 הודעות, בשתיהן המזהה של הTGS, הזמן של הסשן של הTGT ועוד פרטים, ובהודעה השנייה גם הIP ושם משתמש של הלקוח, ההודעה הראשונה מוצפנת עם המפתח של הלקוח והשנייה עם הTGS session key.
בשלב הזה היוזר מכניס סיסמה שממנה נוצר המפתח הסודי שלו, זה שלה האימות סימה בעצם. (היוזר עדיין לא יכול לפענח את ההודעה השנייה)
היוזר שולח את הTGT לשרת של חלוקת הכטיסים (TGS - ticket granting server) שמאמת את הכרטיס ואת ההודעה ושולח ליוזר חזרה ST (server ticket) .
היוזר יוצר הודעת אותנטיקציה ושולח אותה ביחד עם הST לשרת שמאמת אותה ויוצר הודעת אותנטיקציה משלו ליוזר (כדי שיאמתו אחד את השני).
דבר נוסף שהKDC עושה הוא לבדוק שהיוזר לא כבר עשה אותנטיקציה בזמן האחרון, הוא עושה זאת בכך שהוא שומר ticket cache שם יש רשימות של כל היוזרים שעשו אותנטיקציה והסשן של הTGT עדיין חל, ביחד עם הsession key.



2. **Key Concepts:**  Define principals, realms, KDC components, tickets (TGT vs service ticket), and how encryption keys are derived and used.

הrealm הוא בעצם איזהשהו תחום מוגדר ברשת שיש מספר שרתים ולקוחות שכולם "שייכים לו" ותחת שליטתו של הKCD העומד במרכזו.
הprincipal הוא יישות, יכול להיות לקוח או שרת שצריך לעשות לו אותנטיקציה והוא שייך לתחום מסויים.
האותנטיקציה הזאת נעשית באמצעות הkdc (key disterbution center) שמחלק כרטיסים שהם בעצם סשן זמני שיש למשתמש בו הוא עושה אותנטיקציה לשירות מסויים.
הKDC מורכב משני שרתים, אחד של אותנטיקציה שמוודא שמי שמבקש לעשות את האותנטיקציה זה יוזר מוכר ומבקש לחלק לו כרטיס והשרת השני של חלוקת כרטיסים מוודא שהיוזר עשה בקשת אותנטיקציה לשרת מוכר ונותן כרטיס.
הKDC שומר גם על כל המפתחות הצפנה שצריך.
השני מרכיבים העיקריים של הKDC (הAS והTGS) מכילים את כל המידע הנדרש, בAS יש רשימה של כל היוזרים בrealm והמפתחות הסודיים שלהם ובTGS יש רשימה של השרתים בrealm והמפתחות הסודיים שלהם.



3. **Security Properties:**  Why is Kerberos considered secure?  Discuss mutual authentication, replay protection, time sensitivity, and the role of the ticket lifetime.

למה kerberos נחשב בטוח? נסתכל על כמה היבטים:
- אותנטיקציה הדדית, הkerberos עומד בין היוזר לשירות בו היוזר רוצה להשתמש ודואג שתהיה אותנטיקציה הדדית של שניהם, כלומר לא רק האתר מוודא שהיוזר בטוח או להפך, הkerberos כצד שלישי מוודא שגם האתר מוכר ותקין וגם היוזר, מה שיוצר בטיחות והגנה מפני MITM.
- הreplay protection של kerberos הוא מתודה להגנה מפני האזנה בו בזכות הticket cache שבו שומרים איזה יוזרים כבר התחברו, גם אם תוקף הצליח להאזין לתעבורה ולגלות פרטי התחברות של יוזר מסויים שהתחבר, הוא לא יוכל להתחבר שוב כי היוזר נמצא בticket cache כמחובר. כלומר תוקף לא יכול לנסות לשכפל הודעות אותנטיקציה של יוזר שהתחבר כי הוא ידחה.
- מדיניות time sensitivity דואגת שהשעונים של כל השרתים המעורבים יהיו מסונכרנים, גם של השרתים בKDC וגם של הלקוח ששלח בקשה, אחרת תוקף היה יכול לחכות ולשלוח בקשה ישנה עם פער בזמנים ואם לא היה ניטור על זה השרת היה רואה אותה כלגיטימית. כשהשעות חייבות להיו תמסונכרנות וגם בתחום סשן של הטיקט תוקף לא יכול לשכפל בקשה ישנה ולנסות להציג אותה כעדכנית.
- הticket lifetime הוא מגבלת זמן שיש לTGT וגם לST שהשרתים נותנים ליוזר, בתחום הזמן הזה הלקוח נחשב כעבר אותנטיקציה , לעומת זאת אם לא היה את זה תוקף שהצליח להיכנס היה יכול להישאר באותו יוזר (כי אין תוקף לכרטיס). זה גם דואג לניהול הרשאות אצל היוזרים עצמם, נגיד שיש יוזרים של מנהלים ויוזרים רגילים ולקוח הפך ממנהל ליוזר רגיל, אם אין לכרטיס שלו תוקף סיום הוא ישאר עם הרשאות של אדמין לנצח.
כל הדברים האלה דואגים שkerberos תנהל ממש מדיניות צד שלישי של cookies בין לקוח לשרת. 

4. **Administration & Tools:**  What are common Kerberos administration tasks?  Describe commands like `kadmin`, `kinit`, `klist`, `kdestroy`, and how to add principals or change passwords.

בצד הפרקטי, מה המשימות המנהלתיות בkerberos?
הkadmin הוא אחת הפקודות המרכזיות, איתו יוצרים principals משנים סיסמאות ועוד הרבה פעולות אחרות. הkadmin הוא בעצם מה שמנהל את המערכת, מתקשר עם הדאטה בייס ומבצע פעולות עליו.
כמובן שצריך לעבור אותנטיקציה כדי להתחבר אליו דרך הkadmin/admin או kadmin/host, ואפשר גם להתחבר לוקלית לkadmin.local שפועל דרך הKDC.
בתור אדמין אנחנו יכולים ליצור principals עם הפקודה addprinc x (הx זה השם של הprincipal שנרצה), למחיקה נכתוב delprinc x, לשינוי סיסמה נשתמש בcpw x.
פקודה מרכזית נוספת היא kinit שהיא סוג של הכלי של היוזר שמנסה לעשות אותנטיקציה, היא אחראית לתפעל את קבלת הTGT.
בצד היוזר כל מה שצריך לעשות זה להקדליד kinit x (שם היוזר) ואז להכניס סיסמה והkinit הוא זה שעושה לנו את הלוגין בכך שיוצרת או מחדשת כרטיס.
הפקודה klist מראה לנו מה יש בticket cache, כלומר איזה כרטיסים יש עם סשנים שעדיין לא פג תוקף (רק של אותו יוזר כמובן) ככה אפשר לבדוק אם לוגין לא עבד או משהו קרה.
הפקודה kdestroy היא פקודה שמוחקת את האותנטיקציה של משתמש, היא מנקה את הticket cache שלו , גם את הTGT וגם את הST הנוכחיים.


5. **Integration & Troubleshooting:**  How do services (Hadoop, HTTP, SSH) integrate with Kerberos?  What are typical issues (clock skew, wrong realm, keytab problems) and how do you diagnose them?

 משתמשים בkerberos ביחד עם hadoop בגלל שלhadoop לכשעצמו אין מערכת אותנטיקציה חזקה.
 כל שירות בקלאסטר של hadoop מהווה principal בkerberos וכשלקוח רוצה להתחבר אליהם הוא עושה זאת עם אותנטיקציה רגילה דרך kerberos, ככה הוא עושה אותנטיקציה לכל המשתמשים.
 גם השירותים עצמם בתוך hadoop כשהם מתקשרים אחד עם השני הם בעצם עוברים אותנטיקציה דרך kerberos ומקבלים TGT וכו..
 שגיאה שיכולה להיות נפוצה מאוד בhadoop (וגם מחוץ לה) היא clock skew שקורית כשיש הפרש שעות גדול מדי בין השרתים של hadoop לkerberos נגיד, השרתים של kerberos יחשבו שמנסים לזייף אותנטיקציה ולכן ידחו את כל הנסיונות. דרך להתגבר על זה היא לסנכרן זמן עם NTP.
 כשמדברים על HTTP אנחנו מדברים על רשת לא בטוחה, kerbos מהווה שכבת הגנה כדי לתת אותנטיקציה שאין וזה נעשה בדרך כלל בעזרת SPENGO. השרת מבקש מהדפדפן את האותנטיקצית kerberos והוא שולח לשרת את הST שביקש מהKDC בתור הודעת HTTP, השרת מםענח ומאמת אותו וככה אין צורך בסיסמה.
 באינטגרציה עם SSH משתמשים בGSSAPI, המשתמש עושה KINIT ואז מבקש התחברות SSH לשרת, גם פה השרת יבקש ST ויאמת אותו בלי צורך בסיסמה או לוגין.
שתי תקלות נפוצות היכולות לקרות:
בעיות עם הkeytab, לדוגמה יכול להיות שהמפתח שאנחנו מנסים להשתמש בו להצפנה לא תואם את המפתח השמור בKDC , שהייתה תקלה בשמירה ושהוא עודכן מאז ועכשיו האותנטיקציה לא עובדת, לפעמים נצטרך ליצור מחדש realm וkeytab כדי לפתור את זה.
בעיות wrong realm, כשאנחנו מנסים לעשות אותנטיקציה לשרת שנמצא בrealm מסויים אבל אנחנו בKDC שנמצא בrealm אחר, זה יכול להיגרם בגלל שאילתת DNS לא נכונה לדוגמה. במקרה זה צריך לבדוק את השאילתת DNS, לרשום KINIT מחדש עם realm ספציפיץ

### LDAP – five guiding questions
1. **Directory Structure:**  Explain how LDAP organizes information in a hierarchical tree (DN, RDN), common object classes, and attributes for users and services.

כשרוצים לגשת לdirectory מסויים אבל לא יודעים מה לחפש, פונים לLDAP (lighweight directory access protocol).
הLDAP שומר את כל המידע בעץ היררכיה מסודר בראשו עומד הroot directory. ממנו מסתעפים למדינות, משם לארגונים, משם ליחידות ארגוניות ומשם לאינדיבדואלים.
לכל רשומה בתוך הdirectory יש סט תכונות, ולכל תכונה יש שם וערכים מוגדרים מראש, לדוגמה : שם התכונה : אימייל , ערך : x@gmail.com.
לכל רשומה כזאת יש DN, שזה הPATH המלא לרשומה, וRDN שזה השם של הרשומה בתוך הdirectory.
לכל רשומה יש object class שמייצגת איזה סוג רשומה זאת וגם לobject class יש שם מזהה וסט תכונות (שכל שאר הרשומות מאותו סוג צריכות שיהיה להן).
סוגי הobject class הנפוצים:
אדם, יחידה ארגונית, קבוצה
ויש עוד הרבה כאלו.
התכונות שיכולות להיות נדרשות לכל רשומה זה שם\רשימת DN, שם ארגון ועוד...
הLDAP גם מאפשר לשלוט בלמי יש הרשאות במערכות מסויימות וגם לחפש מידע לפי תכונות או שמות, לדוגמה לפי הכנסה של שם פרטי או של חברה לחפש אימייל.


2. **Protocols & Operations:**  Describe basic LDAP operations – bind, search, modify, add, delete – and the difference between simple and SASL binds.

פעולות בLDAP:
- הbind זאת פעולה שנוצרת אחריי שנוצר סשן של LADP ולקוח יצר חיבור לשרת אבל עדיין לא עשה אותנטיקציה, הbind יוצר אותנטיקציה לסשן. הbind שולח את הDN של היוזר והסיסמה שלו לשרת שמאמת אותו מול התכונה של הסיסמה ברשומת היוזר. בbind פשוט השם משתמש והסיסמה נשלחים בplaintext ובSASL זה מוצפן בTLS ומספק גם אותנטיקציה עם kerbekos 
- הsearch היא הפעולה לחיפוש רשומות,שם אפשר להכניס פילטרים למה לחפש והאם לחפש רק את הרשומה או את כל העץ מתחתיה.
- הmodify מבקשת מהשרת LDAP לשנות רשומה קיימת,הDN של הרשומה חייב להיות כלול והשינוי צריך להיות ADD/DELETE/REPLACE.
- הadd מכניסה רשומה חדשה לדאטה בייס של LADP בתנאי שאין כבר שם DN כזה.
- הdelete מוחקת רשומה בהינתן הDN שלה ובתנאי שאין רשומות בת. 

3. **Schema & Extensibility:**  What is an LDAP schema?  How do object classes, attribute types, and syntax rules define what data can be stored?  Mention extending schemas.

סכמת הLDAP בעצם מגדירה איך נראים הנתונים בLDAP, היא מכילה נתונים על הצורה של הנתונים ששמורים בספריות.
היא עושה זאת בעזרת כך שהיא שומרת פרטים על הסוגי תכונות- האם התכונה חובה, איזה תכוונות יש, חוקי סינטקס- איזה סוג של טקסט זה כל תכונה (INTEGER/STING) ועוד. בעזרתם היא מגדירה מה מותר לנתון להיות ומה אסור ואיך כל הנתונים חייבים להיראות.
אפשר גם להשתמש בערכים והגדרות נוספים לתכונות ואפילו הוספת תכונות ובכך להאריך את הסכמה (ניתן לעשות זאת בעזרת ldapmodify).



4. **Authentication & Authorization:**  How is LDAP used for authentication and authorization?  Cover binding with credentials, password policies, and group lookups.

אחד מהשימושים של LDAP הוא לאותנטיקציה, זאת בעזרת בקשת הbind שLDAP עושה עם חיבור הלקוח לשרת בה היא שולחת את הcredentials (שם משתמש וסיסמה), השרת של LDAP בודק שבאמת יש DN מתאים לשם משתמש הזה ומאמת את הסיסמה עם הנתונים בדאטה בייס שלו (הסיסמה שמורה כתכונה בערך של השם משתמש). את מדיניות הסיסמאות עצמה, LDAP מנהלת, יש מינימום על אורך הסיסמה, תוקף אחריו צריך לשנות סיסמה ומנגנון נעילת יוזר אם היו יותר מדיי נסיונות כושלים לעשות ממנו לוגין.
מנכנון נוסף של LDAP הוא שמירה על הרשאות, לכל משתמש יש גישה מסויימת לרשומות ולא לכולם יש הרשאה להכל.
אלה דואגים לשמור על אותנטיקציה של המשתמש ושמירה על ההרשאות של המשתמשים אחריי הגישה.

5. **Deployment & Security:**  Outline how to install/configure an LDAP server (e.g., OpenLDAP), secure it with TLS, replicate data, and troubleshoot common errors (referral loops, access controls).


הורדה וקונפיגורציה של LDAP:
תחילה צריך להוריד ETEL ולאחר מכן אפשר להוריד openLDAP. לאחר מכן יש להתחיל אותו עם systemctl start ואז לעשות לו enable.
לאחר מכן יש לאפשר חיבור חיצוני ובcentOS צריך לאשר חיבור לחומת אש.
לאחר מכן צריך לערוך את ההגדרות ברירות מחדל וליצור סיסמה לroot user וליצור קובץ rootpw.file.
את השרת צריך לקנפג עם תעודת CA, מפתח פרטי ותעודה חתומה של השרת, ובצד הלקוח יש להוסיף את התעודת CA של השרת לרשימת המסמכים שסומכים עליהם. 
ככה הלקוח יסמוך ויקבל את הCA של השרת ויוכלו להתחיל בתקשורת מוצפנת בTLS.
כשנרצה לשנות מידע, הלקוח (מוסמך בלבד) ישלח בקשה לשרת, והשרת ישלח את התשובה ללקוח וישכפל את השינויים לכל השרתים.
אם השרתים ביחסי master-slave אז שרת המאסטר יפיץ את העדכון, אם הם ביחסי master-master אז הם יכולים להתעדכן אחד מהשני על השינויים.
לפעמים נחפש מידע מהשרת הלא נכון, והוא יפנה אותנו לשרת אחר שבו המידע נמצא.
אם הDNS לא מוגדר טוב יכול להיווצר לופ מעגלי. כדי למנוע אותו, נגדיר מספר מקסימלי של הפניות שניתן לעשות ונבדוק מעגלים.


שאלות סקילה:

בzookeeper איך אני בודקת איזה שרת כתב מה לזיכרון?   השרת מאסטר הוא היחיד שמאשר פעולות כתיבה , יש לנו transaction log ששומר את כל התיעודים של הפעולות שנעשו וsnapshots שנלקחים כל כמה transaction logs שמתעדים איך זה נראה. אם שרת עדיין באמצע פעולת כתיבה, אנחנו נראה שהsnapshot שלו לא תואם את האחרים. אם כל הsnapshots של השרתים זהים כולם כתבו את כל המידע שצריך.
איך השרתים משתמשים בPexos במקרה שחלק התנתקו והם פחות מהquorum ? כשקורה split brain וחלק מהשרתים שהם פחות מהquorum התנתקו והם לא יכולים לעשות שום פעולה, הם ממתינים עד שיחזרו לרשת, ובזמן הזה קורה עקרון ZAB שהוא סוג של Paxos, בו בשרתים שנשארו ברשת הם בוחרים leader לפי מי הכי מעודכן כלומר יש לו את הzxid הכי קטן.
איך יודעים שהמספר של הsequential nodes עולה ב1 כל פעם ולא ביותר? הleader הוא זה שמנהל את היצירה של המספר הסידורי שלהם  ככה שאין התנגשויות כי הוא אחראי על כולם, המספר עולה אוטומטית ב1 מהפעם האחרונה (כל הקודקודים שמורים וניתן לראות את המספרים של כולם)
איך עובד התהליך של הורדת קונפיגורציה בzookeeper ? כשנרצה להוריד קונפיגורציה, השרת leader ישנה בקובץ /config/db את הקונפיגורציה שצריך (אחריי אישור של הרוב) ואז ישלח הודעה לכל הfollowers שישנו גם , ואז צריך: או לעשות ריסטרט , או שלכל הservices יהיה watch על הznode של הקונפיגורציה שהוא ידע לעדכן.
הגדרת ticktime והקשר של זה timeout     הticktime הוא כל כמה זמן מצפים לheartbeat, ואם עבר 2 ticktime ללא heartbeat זה נחשב timeout
Invalidate cache    כשאנחנו עושים watch זה חד פעמי כי בין כל watch שאנחנו עושים המידע יכול להתעדכן עוד הרבה מאוד פעמים ואנחנו לא רוצים לקבל התראה על כל פעם שזה קורה עוד לפני שעדכנו את המידע מההתחלה, לכן נעדכן ידנית watch כדי שנתעדכן אחריי שכבר עדכנו את המידע. נוסף על זה השרת יעדכן את הקובץ קונפיגורציה ואת הגרסה כל כמה זמן , ככה נבדוק שהcache שלנו תמיד מעודכן.
למה להשתמש בLDAP ולא SQL או דאטה בייס אחר?LDAP נותן לנו את האופציה של אינטגרציה עם שירותים אחרים כמו Kerberos, . בלי קשר לכך שהוא נוח לשימוש בצורה ההיררכית והאפשרויות חיפוש בו הוא גם מבצע אימות עם Kerberos ובדרך כלל בא בזוג איתו ב
 Directory.
## Wrapping Up :trophy:
Review your answers with your mentor and discuss any unclear points.  Relate each concept back to actual deployments you might encounter.

## Action Items
- Note topics you want to investigate further.
- Prepare questions for the mentor Q&A session.
- Document any commands or configuration steps you used during research.

## Recommended Resources
- [Apache Zookeeper Documentation](https://zookeeper.apache.org/)
- [Kerberos: The Network Authentication Protocol](https://web.mit.edu/kerberos/)
- [LDAP: RFC 4511 Overview](https://datatracker.ietf.org/doc/html/rfc4511)
- *Hadoop Security* chapter in any modern Hadoop book for integration examples.
