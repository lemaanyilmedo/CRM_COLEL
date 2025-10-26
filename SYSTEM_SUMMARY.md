# 🕍 סיכום מערכת CRM Kolel

## 📌 מה זו המערכת?
מערכת ניהול מקיפה לכוללים - מעקב אחר אברכים, נוכחות, תשלומים ודיווח.

---

## 🏗️ ארכיטקטורה טכנית

### Backend:
- **Framework:** Flask (Python 3.13)
- **ORM:** SQLAlchemy
- **Authentication:** Flask-Login
- **Database:** SQLite (ניתן לשדרג ל-PostgreSQL)
- **Server:** Gunicorn (ייצור)

### Frontend:
- **UI Framework:** Bootstrap 5
- **Icons:** Font Awesome
- **JavaScript:** Vanilla JS (ללא frameworks)
- **Templating:** Jinja2

### מבנה Blueprint:
```
app/
├── admin/          # ניהול מערכת (משתמשים, סניפים, הגדרות)
├── attendance/     # ניהול נוכחות (יומי, היסטוריה)
├── auth/           # אימות והרשאות (login/logout)
├── avrech/         # ניהול אברכים (CRUD)
├── calendar/       # לוח שנה עברי
├── main/           # דף ראשי ודשבורד
├── payment_profiles/  # פרופילי תשלום
└── reports/        # דוחות (חודשי, שנתי, נוכחות)
```

---

## 🗄️ מודלים במסד נתונים

### 1. **User** - משתמשי מערכת
- username, email, password_hash
- role: 'admin' / 'employee'
- is_active

### 2. **Branch** - סניפי כולל
- name, address, phone
- is_active
- Relationship: → Avrech (one-to-many)

### 3. **PaymentProfile** - פרופילי תשלום
- name, default_entry_time, default_exit_time
- payment_method: 'daily_fixed' / 'monthly_target'
- daily_amount, monthly_target
- enable_late_penalty, late_penalty_method, late_penalty_amount
- enable_absence_penalty
- Relationship: → Avrech (one-to-many)
- Relationship: → BonusRule (one-to-many)

### 4. **BonusRule** - חוקי בונוסים
- name, bonus_type, amount, description
- Belongs to: PaymentProfile

### 5. **Avrech** - אברך
- first_name, last_name, id_number, phone, email
- branch_id, payment_profile_id
- is_active, enrollment_date
- Methods: get_monthly_attendance_summary()
- Relationship: → AttendanceLog (one-to-many)

### 6. **AttendanceLog** - רישום נוכחות
- avrech_id, date, entry_time, exit_time
- status: 'present' / 'absent' / 'sick' / 'vacation'
- late_minutes, early_exit_minutes
- taanit_dibur_bonus (boolean)
- daily_base_amount, penalties_amount, bonuses_amount, net_daily_amount
- Methods: calculate_amounts()

### 7. **SystemCalendar** - לוח שנה מערכתי
- date, event_type, is_working_day
- hebrew_date, description
- Static method: is_working_day(date)

---

## 🔐 מערכת הרשאות

### Admin:
- גישה לכל הפונקציות
- ניהול משתמשים, סניפים, הגדרות
- צפייה וניהול של כל האברכים

### Employee:
- צפייה ברשימות אברכים
- רישום נוכחות
- צפייה בדוחות

---

## 🎯 תכונות מרכזיות

### ✅ מוכן ופעיל:
1. **אימות והרשאות** - login/logout מלא
2. **ניהול אברכים** - הוספה, עריכה, צפייה, מחיקה
3. **ניהול סניפים** - הוספה ועריכה
4. **רישום נוכחות יומי** - עם חישוב איחורים
5. **היסטוריית נוכחות** - מעקב לפי אברך/תאריך
6. **פרופילי תשלום** - הגדרת מדיניות תשלום
7. **דוחות חודשיים** - עם סיכומים וסטטיסטיקות
8. **דוחות שנתיים** - מעקב שנתי
9. **סיכום נוכחות** - אחוזים וגרפים
10. **ניהול משתמשים** - הוספה ועריכה

### ⚠️ חלקי - דורש השלמה:
1. **לוח שנה** - UI קיים, אבל אין אירועים דינמיים
2. **הגדרות מערכת** - עמוד קיים אך ריק
3. **עריכת אברך** - הטופס קיים אך הנתיב חסר
4. **מחיקת רשומות** - כפתורים קיימים אך פונקציונליות חסרה

---

## 📊 חישובי תשלומים

### לוגיקה:
1. **בסיס יומי:** daily_amount מ-PaymentProfile
2. **קיזוזים:**
   - איחור: לפי late_penalty_method (fixed/per_minute)
   - היעדרות: לפי absence_penalty_method (full_day/partial)
3. **בונוסים:**
   - תענית דיבור: +10 ₪ ליום (אופציונלי)
   - בונוסים נוספים מ-BonusRule
4. **נטו:** base_amount - penalties + bonuses

### נוסחה:
```python
net_daily_amount = daily_base_amount - penalties_amount + bonuses_amount
```

---

## 🚀 פריסה

### Development:
```bash
python init_db.py
python run.py
# http://127.0.0.1:5000
```

### Production (Render):
- Build: `pip install -r requirements.txt && python init_db.py`
- Start: `gunicorn run:app`
- Environment: SECRET_KEY, FLASK_ENV=production

---

## 🔧 קבצי תצורה

### requirements.txt
כל התלויות של Python

### Procfile
```
web: gunicorn run:app
```

### render.yaml
הגדרות Render אוטומטיות

### .gitignore
מונע העלאת __pycache__, instance/, .env

---

## 📱 כניסה ראשונה

```
URL: https://crm-colel.onrender.com
Username: admin
Password: admin123
```

**⚠️ חשוב:** שנה סיסמה מיד!

---

## 🎨 UI/UX

### עיצוב נוכחי:
- **Theme:** Bootstrap 5 default
- **Colors:** צבעוני (primary, success, danger, warning, info)
- **RTL:** מלא - תמיכה בעברית
- **Responsive:** מותאם למובייל

### נקודות לשיפור:
- [ ] עיצוב מינימליסטי יותר
- [ ] פלטת צבעים מקצועית (לבן/אפור/כחול כהה)
- [ ] אנימציות מתונות
- [ ] טיפוגרפיה עברית משודרגת

---

## 🔄 שיפורים עתידיים (TODO)

### פיצ'רים:
- [ ] ייצוא PDF
- [ ] שליחת SMS/Email
- [ ] תזכורות אוטומטיות
- [ ] גיבוי אוטומטי
- [ ] API REST
- [ ] אפליקציית מובייל

### טכני:
- [ ] מעבר ל-PostgreSQL
- [ ] Redis לקאשינג
- [ ] Celery למשימות רקע
- [ ] Docker containerization
- [ ] CI/CD pipeline

---

## 📞 תמיכה ופיתוח

**GitHub:** https://github.com/lemaanyilmedo/CRM_COLEL  
**Developer:** @lemaanyilmedo  
**Python:** 3.8+  
**License:** Private use

---

## 💡 טיפים ל-AI עוזר:

### כשמשנים קוד:
1. שמור על מבנה Blueprint
2. עדכן גם routes וגם templates
3. אל תשכח db.session.commit()
4. בדוק הרשאות (@login_required)

### כשמוסיפים פיצ'ר:
1. הוסף נתיב ב-routes.py
2. צור/עדכן template בתיקיה המתאימה
3. עדכן navigation ב-base.html
4. בדוק שהכל עובד לפני push

### כשמתקנים באגים:
1. בדוק logs ב-terminal/render
2. בדוק שהמודלים מסונכרנים
3. אתחל DB אם צריך (python init_db.py)
4. נקה cache בדפדפן

---

**המערכת מוכנה לשימוש ייצורי! 🎊**
