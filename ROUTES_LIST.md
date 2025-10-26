# 🗺️ רשימת נתיבים מלאה - CRM Kolel

## 🔐 Auth - אימות

| נתיב | שיטה | תיאור | סטטוס |
|------|------|-------|-------|
| `/auth/login` | GET/POST | דף התחברות | ✅ עובד |
| `/auth/logout` | GET | יציאה מהמערכת | ✅ עובד |
| `/auth/profile` | GET | פרופיל משתמש | ⚠️ קיים אך ריק |

---

## 🏠 Main - עמוד ראשי

| נתיב | שיטה | תיאור | סטטוס |
|------|------|-------|-------|
| `/` | GET | דשבורד ראשי | ✅ עובד |
| `/index` | GET | דשבורד (אליאס) | ✅ עובד |

---

## 👥 Avrech - ניהול אברכים

| נתיב | שיטה | תיאור | סטטוס |
|------|------|-------|-------|
| `/avrech/` | GET | רשימת אברכים | ✅ עובד |
| `/avrech/add` | GET/POST | הוספת אברך | ✅ עובד |
| `/avrech/<int:id>` | GET | צפייה באברך | ✅ עובד |
| `/avrech/<int:id>/edit` | GET/POST | עריכת אברך | ❌ לא מוגדר |
| `/avrech/<int:id>/delete` | POST | מחיקת אברך | ❌ לא מוגדר |

---

## 📅 Attendance - נוכחות

| נתיב | שיטה | תיאור | סטטוס |
|------|------|-------|-------|
| `/attendance/` | GET | נוכחות יומית (אליאס) | ✅ עובד |
| `/attendance/daily` | GET | רישום נוכחות יומי | ✅ עובד |
| `/attendance/save_daily` | POST | שמירת נוכחות | ✅ עובד |
| `/attendance/history` | GET | היסטוריית נוכחות | ✅ עובד |

---

## 💰 Payment Profiles - פרופילי תשלום

| נתיב | שיטה | תיאור | סטטוס |
|------|------|-------|-------|
| `/payment-profiles/` | GET | רשימת פרופילים | ✅ עובד |
| `/payment-profiles/add` | GET/POST | הוספת פרופיל | ✅ עובד |
| `/payment-profiles/<int:id>` | GET | צפייה בפרופיל | ✅ עובד |
| `/payment-profiles/<int:id>/edit` | GET/POST | עריכת פרופיל | ❌ לא מוגדר |
| `/payment-profiles/<int:id>/delete` | POST | מחיקת פרופיל | ❌ לא מוגדר |

---

## 📊 Reports - דוחות

| נתיב | שיטה | תיאור | סטטוס |
|------|------|-------|-------|
| `/reports/` | GET | דוח חודשי (ברירת מחדל) | ✅ עובד |
| `/reports/monthly` | GET | דוח תשלומים חודשי | ✅ עובד |
| `/reports/annual` | GET | דוח שנתי | ✅ עובד |
| `/reports/attendance_summary` | GET | סיכום נוכחות | ✅ עובד |
| `/reports/export_csv` | GET | ייצוא לCSV | ✅ עובד |

---

## 🗓️ Calendar - לוח שנה

| נתיב | שיטה | תיאור | סטטוס |
|------|------|-------|-------|
| `/calendar/` | GET | לוח שנה ראשי | ⚠️ UI בלבד |
| `/calendar/manage` | GET | ניהול לוח שנה | ⚠️ דף ריק |
| `/calendar/add_event` | POST | הוספת אירוע | ⚠️ לא מחובר למודל |

---

## ⚙️ Admin - ניהול מערכת

| נתיב | שיטה | תיאור | סטטוס |
|------|------|-------|-------|
| `/admin/users` | GET | ניהול משתמשים | ✅ עובד |
| `/admin/users/add` | POST | הוספת משתמש | ❌ לא מוגדר |
| `/admin/users/<int:id>/edit` | GET/POST | עריכת משתמש | ❌ לא מוגדר |
| `/admin/users/<int:id>/delete` | POST | מחיקת משתמש | ❌ לא מוגדר |
| `/admin/branches` | GET/POST | ניהול סניפים | ✅ עובד |
| `/admin/branches/<int:id>/edit` | GET/POST | עריכת סניף | ❌ לא מוגדר |
| `/admin/branches/<int:id>/delete` | POST | מחיקת סניף | ❌ לא מוגדר |
| `/admin/system_settings` | GET | הגדרות מערכת | ⚠️ דף ריק |

---

## 📈 סיכום סטטוס

### ✅ פעיל ומלא (17):
- Login/Logout
- דשבורד
- רשימת אברכים + הוספה + צפייה
- נוכחות יומית + שמירה + היסטוריה
- פרופילי תשלום + הוספה + צפייה
- 3 דוחות מלאים + ייצוא CSV
- ניהול משתמשים (צפייה)
- ניהול סניפים + הוספה

### ⚠️ חלקי (4):
- פרופיל משתמש (עמוד קיים אך ריק)
- לוח שנה (UI מוכן, אין אירועים)
- ניהול לוח שנה (דף ריק)
- הגדרות מערכת (דף ריק)

### ❌ חסר (10):
- עריכת אברך
- מחיקת אברך
- עריכת פרופיל תשלום
- מחיקת פרופיל תשלום
- הוספת משתמש
- עריכת משתמש
- מחיקת משתמש
- עריכת סניף
- מחיקת סניף
- הוספת אירוע ללוח שנה (מחובר למודל)

---

## 🧪 בדיקת נתיבים - רשימה מהירה

### העתק ובדוק אחד אחד:

```
https://crm-colel.onrender.com/
https://crm-colel.onrender.com/auth/login
https://crm-colel.onrender.com/avrech/
https://crm-colel.onrender.com/avrech/add
https://crm-colel.onrender.com/attendance/daily
https://crm-colel.onrender.com/attendance/history
https://crm-colel.onrender.com/payment-profiles/
https://crm-colel.onrender.com/reports/monthly
https://crm-colel.onrender.com/reports/annual
https://crm-colel.onrender.com/reports/attendance_summary
https://crm-colel.onrender.com/calendar/
https://crm-colel.onrender.com/admin/users
https://crm-colel.onrender.com/admin/branches
https://crm-colel.onrender.com/admin/system_settings
```

---

## 🔧 תיקונים מומלצים

### עדיפות גבוהה:
1. הוסף עריכה ומחיקה לאברכים
2. הוסף עריכה ומחיקה לסניפים
3. השלם את עמוד הגדרות המערכת

### עדיפות בינונית:
4. חבר לוח שנה למודל SystemCalendar
5. הוסף CRUD מלא למשתמשים
6. הוסף פרופיל משתמש מלא

### עדיפות נמוכה:
7. הוסף עריכה למחיקה לפרופילי תשלום
8. הוסף ייצוא PDF
9. הוסף גרפים אינטראקטיביים

---

**סה"כ נתיבים: 31**  
**פעילים: 17 (55%)**  
**חלקיים: 4 (13%)**  
**חסרים: 10 (32%)**
