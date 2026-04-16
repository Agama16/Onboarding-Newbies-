# Docker Foundations

Docker is a platform for running applications in isolated environments called containers.

It introduces a standardized way to package and execute software across different environments, without depending on the underlying system configuration.

Instead of installing dependencies directly on a machine, applications are bundled into portable units that can run consistently wherever Docker is available.

---

### ⏳ Timeline
Estimated Duration: 1 Day

Day 1 – Docker Core Concepts  
- Containers vs Virtual Machines  
- Images, Containers, Dockerfile  
- Networking & Storage  
- Security & Isolation  
- Build strategies (Docker, Kaniko, DinD)

---

### 📚 Resources
- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kaniko Documentation](https://github.com/GoogleContainerTools/kaniko)
- [OCI Specification](https://opencontainers.org/)

---

# Docker Core Concepts

### ❓ Guide Questions

1. **What is Docker and what problems does it solve?**  
   Explain what a container is, how it differs from a virtual machine, and why containers are useful in modern systems (portability, consistency, isolation).

דוקר הוא הכלי המאפשר הרצה של יישומים על הקונטיינרים, הם מספקים סביבה מותאמת לכל קונטיינר וכולם מופרדים כך שהם לא מפריעים אחד לשני.
הקונטיינר סוג של עוטף את האפליקציה ביחד עם הספריות וחבילות שבהן היא תלויה ומספק לו סביבת עבודה נפרדת.
דוקר יכול לרוץ על לינקוס, ווינדוס או מאק, ועל ענן או על מחשב מקומי, לכן כל קוד שנכתב יכול לרוץ עם כל סביבת עבודה אפשרית.
בניגוד לVM לדוגמה, ההגדרה והעלאה של דוקר הוא קל ופשוט, ובדרך כלל גם מהיר מאוד.
מלבד העובדה שדוקס מספקת סביבה מופרדת לקונטיינר ומאפשרת להריץ אותו על כל סביבת עבודה, הוא אוכף את הסביבת עבודה למשתמשים שעובדים על אותו קונטיינר (גם אם הם עןובדים בסביבות שונות), הדוקר מוודא שיש התאמה בסביבת עבודה, בין אם זה גרסה של מסד נתונים או שירות רשת 
הדוקר שונה לגמרי מהמכונת הוירטואלית, הVM רץ על הייפרויזור שמאפשר להריץ אותו על מערכת הפעלה שונה לגמרי. הדוקר לעומת זאת מריץ קונטיינרים על אותו קרנל של מערכת ההפעלה ומשתמש פשוט בcgroups, namespaces כדי ליצור הפרדה בין הפרוססים.
ההבדל בהתנהלות עושה את הדוקר מהיר יותר, אבל יותר מסוכן מבחינת אבטחה.
העובדה שהקונטיינרים מאפשרים לארוז ישום עם כל התלויות שלו, בעצם מפרידה את היישום מהאינפרה מתחתיו, כלומר אני יכולה להזיז קונטיינרים בין סביבות עבודה.
הקונטיינר מיוצג ע"י image שאותו מריצים כדי להעלות את היישום.
בהפשטה - קונטיינר הוא היישום והתלות שלו, האימג' הוא ייצוג שלו והדוקר מאפשר ליצור ולהריץ את הקונטיינר.


2. **What are the core Docker components and how do they interact?**  
רכיבי הדוקר הם:
- תוכנה: תהליך daemon בשם dockerd רץ ומאזין לבקשות שנשלחות דרך הAPI של דוקר, ויש גם CLI בשם דוקר המאפשר לתקשר עם התהליך.
- אובייקטים:  האובייקטים של דוקר הם מה שבונים ביחד את האפליקציה, ה3 העיקריים הם הדוקר קונטיינר, שזה הסביבה להרצת האפליקציה, האימג' שזה סוג של טמפלט שבונה את הקונטיינר, והservice שמאפשר להריץ קונטיינר על כמה daemons שונים (ידוע גם כswarm).
כל הdaemons בswarm מתקשרים עם הדוקר API.
- רגיסטרים: ריפוסיטורי של דוקר לאימג'ים, משם הלקוחות יכולים להוריד את האימג'ים או להעלות כאלה שהם יצרו
הרגיסטרי העיקרי והדיפולטיבי זה docker hub.
- הdockerfile: זה קובץ טקסט שמכיל נתונים חשובים על הסביבת עבודה של הקונטיינר כמו פקודה להרצה בהעלאה.
- הdocker compose: הוא מה שמאפשר להריץ יישום על כמה קונטיינרים במקביל באמצעות קבצי YAML, ועדיין אפשר להעלות אותם ולשלוט עליהם בעזרת פקודה אחת.
הקובץ של docker-compose.yml מאפשר לקנפג את היישום על גבי הקונטיינרים, הוא מכיל הגדרות של build לדוגמה שמקנפג דברים כמו הpath של הdockerfile וכו...
אפשר ליצור יותר מcompose אחד ולאחד ביניהם, האיחוד יהיה לפי סדר שמגדירים וחלק מהערכים ידרסו אחרים.
גם פה אפשר לגשת לאפליקצמיות דרך הCLI עם פקודת הdocker compose.


3. **How do networking and storage work in Docker?**  
   Explain:
   - Container networking (bridge, host, ports)  
   - Communication between containers  
   - Volumes vs bind mounts  
   - When to use persistent storage

נתחיל מאחסון:
 יש שני סוגים של אחסון שאפשר לדבר עליהם, container data persistence או daemon storage backend.
כשאנחנו מדברים על אחסון של הקונטיינר מדברים על אחסון של אפליקציה בעצם אבל שנשמר מחוץ לקונטיינר בעזרת volumes / bind mounts.
כל הקבצים שנוצרים בתוך הקונטיינר נשמרים בשכבה של הקונטיינר מעל הimage. השכבה הזאת של הcontainer layer היא.
כדי לשמור את הנתונים מחוץ לקונטיינר יש כמה אופציות:
volume mounts שומרים את הנתונים על המערכת קבצים של ההוסט גם אחריי שהסרנו את הקונטיינר. כדי לגשת לvolume data צריך לעשות mount לקונטיינר.
הגישה היא מהירה בדיוק כמו גישה למערכת קבצים ישירות.
bind mounts:  יוצרים לינק ישיר בין הקונטיינר והPATH של מערכת ההפעלה של ההוסט.
נותנים גישה לקבצים ותיקיות בכל מקום בהוסט, אבלבגלל שהם לא מבודדים ע"י דוקר, גם תהליכים שהם לא קונטיינרים יכולים לשנות את המידע באותו הזמן.
נשתמש בזה לנתונים שצריך לגשת אליהם גם מהקונטיינר וגם מההוסט.
tmpfs files: מאחסן נתונים ממש בזיכרון של ההוסט, לא בדיסק. המידע נמחק כשמסירים או מרסטים את הקונטיינר.
ישומר למידע רגיש, או למידע ביניים שצריך caching וכו..
בכללי נשתמש בpersistent stirage כשנרצה שהמידע ישמר גם בריסוטים, לדוגמה אם יש לנו DB על קונטיינר, לא נרצה שבכל ריסוט הוא ימחק ויתחיל מ0.


הסוג השני של אחסון הוא איך הdaemon מאחסן image layers וcontainer layers על הדיסק.
משתמשים בcontainered image stores ששם מאחסנים את הimage layers ע"י snapshotters. הimage layers נשמרים שם גם בפורמט compressed וגם uncompressed.

נעבור לnetworking:
קונטיינרים יכולים לתקשר ביניהם, אבל הם לא יודעים באיזה סוג תקשורת ואם הקונטיינרים האחרים הם גם קונטיינרים של דוקר.
כשהמנוע דוקר מתחיל, נוצר לו network built in בשם default bridge.
קונטיינרים שמחוברים לו יכולים לגשת לרשתות מחוץ לdocker host, לכן אם יש לו אינטרנט לא צריך עוד קונפיגורציות לגישה לאינטרנט.
ככה הקונטיינרים מתקשרים בינם עם הIP שלהם.
אפשר לעשות גם custom network שבה מגדירים קבוצת קונטיינרים שמחוברת אליה.
הbridge הוא סוג של דרייבר , יש עוד כמו ipvlan שמחבר אותו לvlans חיצוניים .
אפשר לחבר קונטיינור ליותר מרשת אחת, נגיד ipvlan לגישה לאינטרנט וbridge לגישה לרשת 
המקומית
עוד סוגי דרייברים: host מסיר את הisolation בין הקונטיינר להוסט, none עושה  isolation לקונטיינר מההוסט ומקונטיינרים אחרים.



4. **What are the security and isolation risks in Docker?**  
   Discuss:
   - Namespaces and cgroups (high-level)  
   - Running containers as root vs non-root  
   - Image vulnerabilities and best practices

דוקר משתמש בnamespaces של הקרנל כדי ליצור isolation, הnamespace יכול להיות מכמה סוגים, כמו processID, mount ועוד.
cgroups מגבילים משאבים ומדווחים על היכולות בקונטיינר, הם מקצים CPU, זיכרון, דיסק ועוד
בהרצה של קונטיינרים כרוט, יש לנו שליטה מלאה על הקונטיינר, ליוזר שהוא לא רוט אין את זה,אין להם בהכרח גישה לכל הFS של הקונטיינר.
צריך להתמיד בגישת least privilage כדי למנוע privilage escalations ולכן לתת הרשאות רק למה שצריך.
האימג'ים מהווים מקור פגיעה, הגרסאות עלולות להיות ישנות ותגיות כמו latest גם מסוכנים לשימוש, בגלל זה צריך לעשות סריקה על האימג'ים לפני שמעלים אותם.


5. **How are Docker images built in different environments?**  
   Compare:
   - Standard Docker build  
   - Docker-in-Docker (DinD)  
   - Kaniko  
   Explain when each approach is used (e.g., CI/CD pipelines, Kubernetes).

-docker in docker זאת שיטה להריץ קונטיינר בתוך קונטיינר, נשתמש בעיקר לCI ליישומים בטסטים וכדומה.
-kaniko הוא כלי שמעלה קונטיינרים ללא הdaemon מהדוקר פייל, והוא עושה את זה בכך שמשתמש בexecutor שמריץ פקודה פקודה על הnamespace. נשתמש בקוברנטיס

********************שאלות סקילה *************************
1.איך עושים בDIND שהdaemon יעלה? עם run docker:dind? אני לא סגורה על זה, בכל מקרה יש systemctl start docker אף פעם לא התאכזבתי.
2. עוד צורה שהדוקרים מתקשרים? DNS ואמרתי גם אבל בסדר...
3.חסרונות בהוסט: ההוסט והקונטיינר חולקים namespace וip ולכן אין port mapping והם מזוהים באמת כמו "מכונה אחת" כמו שהם בתכלס.
4. האם לדוקר יש DNS אחד? יש שרת שממפה DNSים אני אמרתי מה אני חושבת ולא ארחיב מעבר.
5.איזה אלטרנטיבה יש לkaniko? יש buildkit שהוא מנוע build של דוקר שתומך בcaching מתקדם, בילד מקבילי, ועושה אותנטיקציה יותר טובה מקניקו (בכללי קניקו עושה בעיות בכל אלה).
6.למה בכלל להשתמש בקניקו? כי לפעמים אין הרשאות root אבל רוצים שליטה, קניקו לא קשור לדיימון ולכן אין צורך להיות רוט.
7.הבדל בין CMD לentrypoint: entrypoint מביא את הפקודה שצריך להריץ וCMD את הארגומנטים הדיפולטיבים שצריך להריץ.
8.איך ממפים volumes? בעזרת volume-subpath שזה ממפה לsubdirectory שנמצא בvolume עצמו.
9.מה זה docker layer? שינוי בimage
10.למה להשתמש בmulti-stage build? כי אפשר להשתמש בimage buildהקודם ו"לעבוד" עליו במקום ידנית להתחיל מ0 כל פעם.
הבסיס עובר לשלב הבא (מבלי הקבצים המיותרים).
---

### 🔄 Alternatives
Assignment: Compare two virtualization approaches:

- Virtual Machines (VMs) vs Containers

Deliverable:
- 1–2 sentences comparison  
- Include a real-world use case for each

Goal:
Understand the trade-offs between full virtualization and container-based isolation.

---

### 🎯 User Story & Scenario

Assignment: Describe a real-world usage of Docker.

Deliverable (2 paragraphs):

- Describe a service (e.g., API) that is packaged using Docker  
- Explain how it is built (Dockerfile), stored (registry), and deployed  
- Describe briefly how containers help ensure consistency across environments
