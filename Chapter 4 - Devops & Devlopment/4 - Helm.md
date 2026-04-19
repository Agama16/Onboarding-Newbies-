# Container Orchestration Foundations: Kubernetes & Helm

Before deploying production-grade services, it is important to understand how container orchestration works.

This module introduces Kubernetes and Helm as the standard tools for managing containerized applications at scale.

The goal is to understand *how systems are deployed, configured, and managed*, and to gain hands-on experience using real-world labs.

---

### ⏳ Timeline  
Estimated Duration: 2 Days  

**Day 1 – Theory & Concepts**  
- Kubernetes core architecture  
- Workloads and networking  
- Helm fundamentals and packaging  

**Day 2 – Hands-On Labs**  
- Kubernetes practical labs  
- Helm chart deployment  
- Debugging and inspection  

---

### 📚 Resources  
Use the resources below as your primary reference:

- [Kubernetes Documentation](https://kubernetes.io/docs/)  
- [Helm Documentation](https://helm.sh/docs/)  
- [OpenShift Documentation](https://docs.openshift.com/)  

---

# Day 1 – Kubernetes & Helm Concepts

### ❓ Guide Questions

1. What is Kubernetes, and what problems does it solve compared to running containers manually on vm?  

קוברנטיס זה מנוע תזמון קונטיינרים שמנהל יישומים בקונטיינרים, עושה להם deployment וscaling בצורה אוטומאטית, והוא מאפשר לעשות את כל זה בצורה מהירה, ללא downtime מכביד.
קוברנטיס מאפשר לעשות mount לאחסון, לנהל את כמות הקונטיינרים, לנטר את הרונטיינרים ו"להחלים" אותם, ולהוסיף פיצ'רים נוספים. את כל זה הוא מנהל בהתאם לכמה CPU/RAM שאנחנו רוצים והוא דואג לנצל אותם בצורה הטובה ביותר.
הניגוד לVM לדוגמה, הוא לא עושה הפרדה ממש במערכת הפעלה אלא יוצר בידוד של המשאבים לקונטיינרים, הדבר הזה פותר את הoverhead הגבוה שיש בVM.
קוברנטיס גם מאפשר להרית הרבה יותר קונטיינרים מאשר הקמה שלהם ידנית על VM אחד.
ההתנהלות עם הקונטיינרים בקוברנטיס הרבה יותר קלה ונוחה, אין צורך לכתוב כל דרישה, קוברנטיס יכול לנהל בעצמו בהתאם למה צריך, לנהל את כמות המשאבים כדי למנוע עומס, לנהל תקשורת בין קונטיינרים בעזרת IP\DNS בניגוד לניהול בVM שהכל ידנית ושם צריך לקנפג ולהגדיר מחדש כל פעם שיש צורך בשינוי, ההתעסקות בVM היא כמעט תמידה בעוד שבקוברנטיס אנחנו יכולים להיות הרבה פחות אקטיבים.
בנוסף, לפעמים VMים יכולים להשתמש ביותר משאבים ממה שהם באמת צריכים.

2. Describe the main Kubernetes components and architecture.  
   Include: cluster, nodes, control plane, kubelet, API server, etcd.

מרכיבי קוברנטיס:
- הAPI מאפשר תשאול של קונטיינרים בעזרת HTTP, מאפשר ליוזרים ולחלקים שונים בקלאסטר לתקשר אחד עם השני. הבקשות API מגיעות לAPI server שעושה להן ולידציה.
- הetcd זה אחסון של כל הנתונים של הקלאסטר כkey-value בשביל סוג של בק-אפ.
- הscheduler מחכה לpods חגשים שלא נמצאים על node מסויים, ומוצא להם node, הוא מתחשב במשאבים, deadline, data locality ועוד.
- הkube controller manager מריץ את תהליכי הcontrollers וביניהם: node controller שמנהל nodes שנפלו, jon controller שיוצר פודים לטאסקים, ועוד.
- הcloud controller manager הוא מרכיב שעושה לינק בין הקלאסטר לAPI של הענן (אם יש).
חמשת המרכיבים האלה הם הcontrol plane.
- הקלאסטר זה השרתים שאנחנו מספקים לקוברנטיס בשביל להקים עליהם פודים (קבוצה של nodes).
- הnodes הם הרכיב שמרכיב את הקלאסטר, שרת.
- הkubelet הוא סוג של סוכן שיש על כל node שמוודא שהקונטיינרים רצים עליו בפוד ושהם "בריאים".
- הפודים זה קבוצה של קונטיינרים שחולקים אחסון ומשאבי רשת.
- הקונטיינר הוא קבוצת משאבים עליו רץ ישום מסויים.
- הcontainer runtime מנהל את כל הlifecycle של הקונטיינר.
-  

3. What are the core Kubernetes resources?  
   Explain Pods, Stateful sets, daemon sets , limit ranges, pv and PVC, namespaces, cronjobs, jobs, roles, rolebindings  Deployments, Services, ConfigMaps, and Secrets, and how they interact.

הpodים הם יחידות של כמה containers עם אחסון משותף ומשאבי רשת משותפים והגדרות ספציפיות על איך להריץ את הקונטיינרים.
התוכן ששל קונטיינרים בפוד משותף תמיד ישבו באותו מיקום ויהיו מתוזמנים ביחד, הם חולקים namespaces, cgroups ולקונטיינרים בפוד יהיו דברים שיבודדו אותם עצמם.
שמים קונטיינרים באותו הפוד רק אם הם תלויים אחד בשני.
אפשר גם ליצור פודים סטטים שיוצרים בקובץ בdirectory כלשהו ונותים לkubelet לנטר, אבל אי אפשר עדיין אי אפשר לנהל אותם עם kubectl או API. 
פודים יכולים לרוץ בסטים שנקראים stateful sets, זה אומר שהם persistent וגם האחסון שלהם צריך להיות. לכל אחד יש מזהה מיוחד (sticky identity).
תחלופה לstateful sets זה daemon sets, זה סט של פודים שמספקים שירותים לוקליים כלשהם, כל node שנמצא בdaemon set יש לו העתק של הפודים, אם אין מקום על הnode לפוד חדש נצטרך לעשות evict לפודים קיימים.
אפשר גם להריץ תהליכי daemon בכך שנתחיל אותם ישירות על node מסויים, אבל daemon sets מאפשרים לנטר לוגים כמו בישומים, מאפשרים לנהל אותם עם kubectl וטמפלטים.
הlimit ranges הם מה שמגדירים את ערכי הדיפולט של המשאבים (CPU/RAM) בהם הnamespace משתמש, בתוך הnamespace הם יכולים להשתמש עד הresourceQuota.
אפשר להגביל משאבי חישוב פר פוד או קונטיינר, אחסון פר volumeClaim, וערכי דיפולט.
הpersistent volume הם volumes שהם פשוט לא תלויים בחיי הפוד, מי שמכיל אותם זה הpvc, שהם בקשה של פודים לאחסון, והם צורכים את הPV בבהתאם לצורך ולמה שאפשר.
הPV יכול להיות סטטי, או דינאמי ואז אם הם לא מתאימים לPVC ניצור volume חדש, בתנאי שהוגדר storage class מתאים.
המשאבים שמורים על namespaces שיוצרים הפרדה לוגית ביניהם.
את הפודים אפשר לתזמן בעזרת cronjobs, אם זה משהו שקורה באופן רגיל, בעיקרון אובייקט cronjob הוא כמו שורת cronjob בקובץ לינוקס. אם פיספסנו תזמון מסיבה מסויימתף אפשר להגדיל דדליין למתי אפשר לתזמן בכל זאת.
אם יש כמה משימות מתוזמנות לאותו זמן, אפשר להגדיר שלא ניתן לעשות זאת, שנדלג על המשימה החדשה, או שנחליף את הישנה.
דרך אחרת היא jobs רגילים, שמריצים task אחד ובו הם יוצרים פודים ומריצים אותם עד שהם מצליחים (עושים נסיון חוזר שוב ושוב).
קוברנטיס מתנהל עם RBAC שבו מגדירים role שזה סט הרשאות בתוך namespace מסויים, או clusterRoles שבהם מגדירים הרשאות למשאבים שיכולים לתת גישה מעבר לnamespace.
בעזרת rolebinding, clusterbinding משבצים role ליוזר מסויים.
הdeployment הוא בעצם מה שמריץ את הפודים עליו ומהווה יישום כלשהו.
על הdeployment אנחנו יכולים ליצור replicasets שזה כמות העותקים של פודים, ואת כל ההגדרות ריצה של הפודים שלנו.
את הdeployment אנחנו בעצם חושפים בעזרת הservices שמוצאים את הIP של הפודים ומאפשרים לתקשראיתם ברשת. זה בעצם אבסטרקציה שחושפת קבוצת פודים בכך שהיא מגדירה סט של endpoints, ככה נגיד פרונט של אפליקציה לא צריך לדעת את הIP של הפודים של הבאק בעצמו.
יש כמה סוגים:
הclusterIP , אפשר לגשת לסרוויס רק מתוך הקלאסטר והוא חושף IP פנימי, אפשר לחשוף לציבורי בעזרת מingress / gateway, זה הדיפולט.
הNodePort חושף את הסרוויס בIP של כל node על פורט סטטי.
הloadBalancer, חושף את הסרוויס חיצונית בעזרת load balancer.
הexternakName ממפה את הסרוויס לexternal name.
הconfigMaps שומרים לנו נתונים בערכי key-value, זה יכול להיות health checks, פקודות, משתנים גלובלים ועוד. זה עושה decoupling מהimage.
בכללי זה אובייקט API שמורכב מdata ומbinaryDat.
הconfigMaps לנתונים "סודיים" נקראים secrets, שם שמים מידע מוצפן, נגיד כשנצטרך מפתח מוצפן שחשוף רק לקונטיינר אחד.


4. How does networking work in Kubernetes?  
   Explain Service types (ClusterIP, NodePort,Ingress,Internal or external network) and basic communication between pods.

.
יש כמה סוגים:
הclusterIP , אפשר לגשת לסרוויס רק מתוך הקלאסטר והוא חושף IP פנימי, אפשר לחשוף לציבורי בעזרת מingress / gateway, זה הדיפולט.
הNodePort חושף את הסרוויס בIP של כל node על פורט סטטי.
הloadBalancer, חושף את הסרוויס חיצונית בעזרת load balancer.
הexternakName ממפה את הסרוויס לexternal name..
תקשורת בין פודים:
לכל פוד יש כתובת IP פנימית בקלאסטר, כלומר כל הפודים בקלאסטר יכולים לתקשר בלי NAT, סט של פודים מיוצג על ידי service מסויים שמנטב לפודים בעזרת לייבלים בבקשות.


5. What is Helm, and why is it used?  
   Explain charts, values.yaml, templating, and how Helm simplifies deployments.

הhelm הוא כלי שעושה distribution לאפליקציה אוטומאטית בעזרת helm charts, הוא מוודא שיש הגדרות ברורות לאפליקציה ושיש עקביות בין הקונטיינרים.
בעיקרון מה שזה מאפשר זה לעדכן קונפיגורציה על כל הקונטיינרים בעזרת variable override.
הלם משתמש בcharts שזה בעיקרון הגדרת כל האפליקציה והעדכונים ובכך מעביר משאבים לקלאסטר קוברנטיס בעזרת הAPI של קוברנטיס.
הchart זה בעיקרון אוסף קבצים לpackage אחד המורכב מ3 דברים עיקריים:
הchart.yaml מגדיר מטא-דאטה של האפליקציה כמו שם, תלויות וכו..
הvalues.yaml מגדיר איך נעשה משתנים חדשים שיחליפו את הישנים בcharts.yaml, מאפשר לעשות לו reuse.
תיקיית /tempelate מאחסן את הטמפלט ומשלב אותו עם הvalues.yaml.
ה/charts מגדיר את כל התלויות של הצ'ארטים .
כל פעם שמורידים chart יוצרים אינסטנס שלו בשם release

---

********************** שאלות סקילה ********************************
1. למה משאבים יותר נוחים לניהול בקוברנטיס מאשר vm? קוסרנטיס יודע לנהל משאבים בצורה יעילה שממצה את מה שצריך ולא יותר, בvm בגלל שזה ממש מערכת הפעלה נפרדת לפעמים יכולים להשתמש או להעלות יותר משאבים ממה שבפועל צריך ולבזבז אותם כשיכלו ללכת למטרה אחרת.
2. איך מקטלגים פוד לקבוצה מסויימת של volume? בעזרת storage classes ממפים אותם סוג של לסוג מסויים של אחסון.
3. באיזה יחידות מידה הCPU? בmillie cores / cores
4. מה זה הlimit range? מגדיר דיפולט למשאבים כמו CPU וRAM, הסברתי בשאלה 3.
5. איך מגבילים networking? בעזרת network policies כמו ingress/egress אפשר להגדיר למי יש יכולת לשלוח בקשות לפוד ואיזה בקשות, יש גם ipBlock שחוסם בקשות מIP מסויים.
6. איך מאפשרים תקשורת בטוחה בקוברנטיס? התקשורת מוצפנת עם TLS, ויש RBAC בו יש roles שלפיהם יש הרשאות להכל, אפשר לעשות אינטגרציה עם LDAP בשביל אותוריזציה.
7. האם route עובד על DNS? כן
8. האם ingress חייב להיות על nginx? לא, למרות שרוב השימושים שלהם ביחד, הוא יכול להיות משולב עם עוד כלים כמו aws load balancer.
9. מה זה הnode port? סוג service שפותח פורט סטטי על כל node ובכך פותח גישה לתעבורה חיצונית. יוצר clusterIP פנימי ומנטר תעבורה מבחוץ ללא load balancer.
10. איך קובעים על איזה node הפוד שלנו יהיה? או בעזרת הוספת תווית של nodeSelector לspec של הפוד ושם להוסיף שם של Node או בעזרת affinity שקובע על איזה nodes הפוד יכול לרוץ, זה יותר גמיש, אפשר או לקבוע שאם לא נמצאה התאמה לא נריץ את הפוד או שאם לא נמצאה התאמה נשבץ אותו על node אחר.
11. מה עושים כשמעבירים את הצ'ארט enviroment מאחת לאחרת? בצ'ארט עצמו כלום, בvalues את האימג' שטוענים וכל הגדרות הסביבה השנייה, ואז לטעון את הvalues לצ'ארט.
12. מה זה אומר לעשות build לצ'ארט? ממש להפוך אותו מקובץ לישום ויזואלי.
13. 

# Day 2 – Hands-On Labs (Kubernetes & Helm)

### ⚠️ Important

There are **two versions of this exercise**:

- Internal lab (provided by the team)  
- External lab (public platforms)  

👉 **You must ask your mentor which version you are required to complete before starting.**

---

## 🧪 Lab Tasks (External Option)

### Kubernetes Core Practice

👉 Start here:  
- [KillerCoda Kubernetes Labs](https://killercoda.com/kubernetes)

**You must complete the following scenarios:**

- Kubernetes Basics  
- Kubernetes Pods  
- Kubernetes Deployments  

---

### 🎯 Required Skills (Must Demonstrate)

During the labs, you must perform:

- Deploy an application (nginx or similar)  
- Expose it using a Service  
- **Scale the deployment (replicas up/down)**  
- **Perform a Rolling Update (change image/version)**  
- Inspect logs and running pods  

---

### Helm Hands-On Lab

👉 Helm practice:  
- [KillerCoda Helm Labs](https://killercoda.com/helm)

Tasks:

- Install a Helm chart  
- Modify values.yaml  
- Perform upgrade  
- Uninstall release  

---

## 🔄 Alternatives

Assignment: Compare two Kubernetes deployment approaches:

- Helm Charts vs Raw Kubernetes YAML manifests

Deliverable:
- 1–2 sentences comparison  
- Include a real-world use case for each  

Goal:
Understand the trade-offs between templated/package-based deployments and manual resource definitions.

---

## 🎯 User Story & Scenario

Assignment: Describe a real-world Kubernetes deployment using Helm.

Deliverable (2 paragraphs):

- Describe a service (e.g., API) deployed to Kubernetes  
- Explain how deployment is managed using Helm (chart, values.yaml, releases)  
- Describe how Helm helps manage environments (dev/staging/prod) and simplifies updates (e.g., rolling upgrades)  

---

## 🎯 Deliverable

By the end of this module, you should have:

- Completed the assigned labs (internal or external, per mentor decision)  
- Successfully deployed and exposed an application in Kubernetes  
- Demonstrated scaling and rolling updates  
- Used Helm to install and manage an application  
- Demonstrated ability to inspect and debug workloads 
