# ==========================================
# مشروع سكن الغرباء الجامعي الخيري
# الملف: config.py
# الوصف: إعدادات المشروع الأساسية، تحميل المتغيرات السرية، وضبط مسار Firebase.
# إعداد: وكالة مسارك كود
# ==========================================

import os
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env (يجب إنشاؤه في نفس المجلد)
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def find_firebase_credentials():
    """إرجاع مسار ملف اعتماد Firebase القياسي أو أول ملف مطابق."""
    default_path = os.path.join(basedir, 'serviceAccountKey.json')
    if os.path.isfile(default_path):
        return default_path

    matching_files = []
    for filename in os.listdir(basedir):
        if not filename.startswith('serviceAccountKey'):
            continue
        if not filename.endswith(('.json', '.json.json')):
            continue

        candidate_path = os.path.join(basedir, filename)
        if os.path.isfile(candidate_path):
            matching_files.append(candidate_path)

    if matching_files:
        return sorted(matching_files)[0]

    return None


class Config:
    """إعدادات التطبيق الأساسية."""
    
    # مفتاح التشفير للجلسات (يُستخدم لحماية النماذج والجلسات)
    # في حال لم يوجد في .env، نضع قيمة افتراضية للتطوير فقط
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'masar-code-super-secret-key-2026'
    FIREBASE_SERVICE_ACCOUNT_KEY = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY')
    
    # مسار ملف حساب خدمة Firebase، مع دعم الاسم القياسي والأسماء البديلة.
    FIREBASE_CREDENTIALS = find_firebase_credentials()
    
    # إعدادات إضافية
    JSON_AS_ASCII = False  # لدعم اللغة العربية في استجابات JSON
    TEMPLATES_AUTO_RELOAD = True  # لتحديث القوالب تلقائياً أثناء التطوير