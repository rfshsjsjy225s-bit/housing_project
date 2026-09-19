# ==========================================
# مشروع سكن الغرباء الجامعي الخيري
# الملف: app/__init__.py
# الوصف: قلب التطبيق. تهيئة Flask، ربط Firebase، تسجيل المسارات،
#        معالجة الأخطاء، وإضافة رؤوس الأمان.
# إعداد: وكالة مسارك كود
# ==========================================

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, jsonify, request
from config import Config


# ==========================================
# 1. تهيئة قاعدة بيانات Firebase
# ==========================================
# نستخدم متغيراً عالمياً للتأكد من عدم تهيئة Firebase أكثر من مرة
# (لأن هذا يسبب خطأ في حال إعادة تشغيل السيرفر)
_db = None


def test_firebase_connection(db):
    """اختبار اتصال فعلي بـ Firestore وإظهار النتيجة للمطور."""
    try:
        db.collection('notifications').limit(1).get()
        print("✅ الاتصال ناجح")
        return True
    except Exception as error:
        print(f"❌ فشل اختبار الاتصال بـ Firebase: {error}")
        return False


def initialize_firebase(app):
    """تهيئة Firebase وربط التطبيق بقاعدة بيانات Firestore."""
    global _db
    
    if _db is not None:
        return _db
    
    # المحاولة الأولى: القراءة من متغير البيئة (لـ Vercel)
    service_account_json = app.config.get('FIREBASE_SERVICE_ACCOUNT_KEY')
    
    if service_account_json:
        try:
            service_account_info = json.loads(service_account_json)
            cred = credentials.Certificate(service_account_info)
            app.logger.info("✅ تم تحميل مفاتيح Firebase من متغير البيئة.")
        except Exception as e:
            app.logger.error(f"❌ فشل في قراءة متغير البيئة: {e}")
            raise
    else:
        # المحاولة الثانية: القراءة من الملف المحلي (للتطوير)
        cred_path = app.config.get('FIREBASE_CREDENTIALS')
        if not cred_path:
            raise FileNotFoundError(
                "❌ لم يتم العثور على ملف مفاتيح Firebase. "
                "تأكد من وضع ملف serviceAccountKey.json في المجلد الرئيسي."
            )
        cred = credentials.Certificate(cred_path)
        app.logger.info("✅ تم تحميل مفاتيح Firebase من الملف المحلي.")
    
    # تهيئة التطبيق
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
    _db = firestore.client()
    app.logger.info("✅ تم الاتصال بقاعدة بيانات Firebase بنجاح.")
    return _db


def get_db():
    """دالة مساعدة للوصول إلى قاعدة البيانات من أي مكان في التطبيق."""
    if _db is None:
        raise RuntimeError("❌ قاعدة البيانات لم تُهيأ بعد. تأكد من استدعاء create_app أولاً.")
    return _db


# ==========================================
# 2. دالة إنشاء التطبيق
# ==========================================
def create_app(config_class=Config):
    """إنشاء تطبيق Flask وتهيئته بكل الإعدادات والمسارات."""
    
    # --- إنشاء التطبيق ---
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    app.config.from_object(config_class)
    
    # --- تهيئة Firebase ---
    initialize_firebase(app)
    
    # --- تسجيل المسارات (Blueprints) ---
    # نستورد هنا لتجنب الاستيراد الدائري (Circular Import)
    from app import routes
    app.register_blueprint(routes.bp)
    
    # --- تسجيل معالج الأخطاء ---
    register_error_handlers(app)
    
    # --- إضافة رؤوس الأمان ---
    register_security_headers(app)
    
    app.logger.info("✅ تم إنشاء التطبيق بنجاح.")
    return app


# ==========================================
# 3. معالجة الأخطاء
# ==========================================
def register_error_handlers(app):
    """تسجيل صفحات الأخطاء المخصصة."""
    
    @app.errorhandler(404)
    def not_found_error(error):
        """صفحة غير موجودة."""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """خطأ داخلي في السيرفر."""
        app.logger.error(f"❌ خطأ داخلي: {str(error)}")
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """ممنوع الوصول."""
        return render_template('errors/403.html'), 403


# ==========================================
# 4. رؤوس الأمان (Security Headers)
# ==========================================
def register_security_headers(app):
    """إضافة رؤوس HTTP لحماية الموقع من الهجمات الشائعة."""
    
    @app.after_request
    def set_security_headers(response):
        # منع تضمين الموقع داخل iframe (حماية من Clickjacking)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        # منع المتصفح من تخمين نوع المحتوى (حماية من MIME Sniffing)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        # تفعيل حماية XSS في المتصفحات القديمة
        response.headers['X-XSS-Protection'] = '1; mode=block'
        # سياسة المرجع (Referrer Policy)
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        # سياسة أمان المحتوى (CSP) - تسمح بتحميل الخطوط والصور من مصادر موثوقة
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "img-src 'self' data: https:; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "script-src 'self' 'unsafe-inline'; "
            "connect-src 'self' https:;"
        )
        return response