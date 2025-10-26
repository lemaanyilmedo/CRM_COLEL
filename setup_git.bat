@echo off
echo ========================================
echo       העלאת הפרויקט לגיטהאב
echo ========================================
echo.

echo שלב 1: אתחול Git...
git init
if errorlevel 1 (
    echo שגיאה באתחול Git
    pause
    exit /b 1
)

echo.
echo שלב 2: הוספת כל הקבצים...
git add .
if errorlevel 1 (
    echo שגיאה בהוספת קבצים
    pause
    exit /b 1
)

echo.
echo שלב 3: יצירת commit ראשון...
git commit -m "Initial commit: מערכת CRM לניהול נוכחות כוללים"
if errorlevel 1 (
    echo שגיאה ביצירת commit
    pause
    exit /b 1
)

echo.
echo שלב 4: הגדרת branch ראשי...
git branch -M main
if errorlevel 1 (
    echo שגיאה בהגדרת branch
    pause
    exit /b 1
)

echo.
echo ========================================
echo     הכנה הושלמה בהצלחה!
echo ========================================
echo.
echo השלבים הבאים:
echo 1. צור repository חדש בגיטהאב בשם: CRM_KOLEL
echo 2. העתק את הכתובת (משהו כמו: https://github.com/USERNAME/CRM_KOLEL.git)
echo 3. הרץ: git remote add origin [כתובת הריפו]
echo 4. הרץ: git push -u origin main
echo.
echo לחץ כל מקש כדי לסגור...
pause