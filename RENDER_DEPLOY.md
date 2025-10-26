# 🚀 מדריך פריסה ל-Render

## שלב 1: הכנת החשבון ב-Render

1. **גש ל-Render:** https://render.com
2. **הירשם/התחבר** עם חשבון GitHub שלך
3. **אשר את החיבור** לחשבון GitHub

---

## שלב 2: יצירת Web Service חדש

1. **לחץ על** "New +" בפינה הימנית העליונה
2. **בחר** "Web Service"
3. **חבר את הריפו:**
   - אם זה הפעם הראשונה: לחץ על "Connect account" → אשר גישה ל-GitHub
   - חפש את הריפו: `CRM_COLEL`
   - לחץ על "Connect"

---

## שלב 3: הגדרת השירות

### הגדרות בסיסיות:
- **Name:** `kolel-crm` (או כל שם שתבחר)
- **Region:** `Frankfurt (EU Central)` (או Oregon אם אתה באמריקה)
- **Branch:** `main`
- **Root Directory:** השאר ריק
- **Environment:** `Python 3`
- **Build Command:** 
  ```
  pip install -r requirements.txt && python init_db.py
  ```
- **Start Command:**
  ```
  gunicorn run:app
  ```

### תוכנית:
- **בחר:** `Free` (חינם!)

---

## שלב 4: הגדרת משתני סביבה (Environment Variables)

לחץ על "Advanced" ואז הוסף את המשתנים הבאים:

### משתנה 1:
- **Key:** `SECRET_KEY`
- **Value:** לחץ על "Generate" או הזן: `your-secret-key-here-change-in-production-12345`

### משתנה 2:
- **Key:** `FLASK_ENV`
- **Value:** `production`

### משתנה 3 (אופציונלי):
- **Key:** `DATABASE_URL`
- **Value:** `sqlite:///kolel_crm.db`

---

## שלב 5: פריסה!

1. **לחץ על** "Create Web Service"
2. **המתן** - Render יתחיל לבנות את האפליקציה (זה לוקח כ-2-3 דקות)
3. **עקוב אחרי הלוגים** בעמוד הראשי

---

## 🎉 זהו! האתר שלך עולה!

אתה תקבל כתובת כמו:
```
https://kolel-crm.onrender.com
```

---

## 🔐 התחברות ראשונה:

```
שם משתמש: admin
סיסמה: admin123
```

**⚠️ חשוב:** שנה את הסיסמה מיד אחרי הכניסה הראשונה!

---

## ⚙️ הגדרות נוספות (אופציונלי)

### 1. Custom Domain (דומיין מותאם אישית)
- Settings → Custom Domain → הוסף את הדומיין שלך

### 2. Persistent Disk (אחסון קבוע למסד נתונים)
⚠️ **חשוב:** ב-Free tier, מסד הנתונים נמחק כל פעם שהשירות נכבה!

לפתרון זה:
- Settings → Disks → Add Disk
- **Name:** `data`
- **Mount Path:** `/data`
- **Size:** 1 GB (חינם)

ואז תצטרך לשנות את `DATABASE_URL` ל:
```
sqlite:////data/kolel_crm.db
```

### 3. Auto-Deploy (פריסה אוטומטית)
- Settings → Auto-Deploy → הפעל
- כל push ל-main יעלה אוטומטית!

---

## 🐛 פתרון בעיות

### האתר לא עולה?
1. בדוק את הלוגים ב-Render Dashboard
2. וודא ש-`requirements.txt` מכיל את כל התלויות
3. וודא ש-`Procfile` קיים ותקין

### שגיאת Database?
1. וודא שהפקודה `python init_db.py` רצה בהצלחה
2. שקול להשתמש ב-Persistent Disk

### האתר איטי?
- זה נורמלי ב-Free tier - השירות "נרדם" אחרי 15 דקות של חוסר שימוש
- הכניסה הראשונה יכולה לקחת 30-60 שניות

---

## 📊 מעקב ומוניטורינג

- **Logs:** Dashboard → Logs
- **Metrics:** Dashboard → Metrics
- **Health Checks:** אוטומטי כל כמה דקות

---

## 🔄 עדכונים עתידיים

כשתרצה לעדכן את האפליקציה:

```bash
# עשה שינויים בקוד
git add .
git commit -m "תיאור השינוי"
git push origin main
```

Render יזהה את השינוי ויפרוס אוטומטית! 🎉

---

## 💡 טיפים

1. **גיבוי:** ייצא את מסד הנתונים מדי פעם
2. **ביצועים:** שקול לשדרג ל-Starter ($7/חודש) לביצועים טובים יותר
3. **אבטחה:** שנה את SECRET_KEY לפני הפריסה
4. **סביבת פיתוח:** השאר את הפיתוח המקומי והשתמש ב-Render רק לייצור

---

**בהצלחה! 🚀**
