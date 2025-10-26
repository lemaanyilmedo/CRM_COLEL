# 🚀 מדריך מהיר - העלאה לגיטהאב ופריסה

## ⚡ העלאה מהירה לגיטהאב

### אופציה 1: באמצעות הסקריפט (Windows)
```cmd
# הרץ את הקובץ:
setup_git.bat
```

### אופציה 2: ידנית
```bash
# 1. אתחול Git
git init

# 2. הוספת קבצים
git add .

# 3. יצירת commit
git commit -m "Initial commit: מערכת CRM כוללים"

# 4. הגדרת branch
git branch -M main

# 5. חיבור לגיטהאב (החלף YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/CRM_KOLEL.git

# 6. העלאה
git push -u origin main
```

## ☁️ פריסה מהירה בRender

1. **היכנס ל-[Render.com](https://render.com)**
2. **New Web Service**
3. **בחר את הריפו CRM_KOLEL**
4. **הגדרות:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run.py`
5. **Deploy!**

## 🔧 עדכונים עתידיים

```bash
# לאחר שינויים:
git add .
git commit -m "תיאור השינוי"
git push origin main

# Render יעדכן אוטומטי!
```

## 📱 פרטי התחברות
- **משתמש:** admin  
- **סיסמה:** admin123

## 🎯 קישורים חשובים
- [GitHub Repository](https://github.com/YOUR_USERNAME/CRM_KOLEL)
- [Live Demo](https://kolel-crm.onrender.com)
- [מדריך מפורט](./GITHUB_DEPLOY_GUIDE.md)

---
*בהצלחה! 🙏*