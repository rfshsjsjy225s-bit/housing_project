# ==========================================
# مشروع سكن الغرباء الجامعي الخيري
# الملف: app/routes.py
# الوصف: المسارات الرئيسية، جلب البيانات من Firebase،
#        وتمرير الروابط الرسمية للقوالب.
# إعداد: وكالة مسارك كود
# ==========================================

from flask import Blueprint, render_template, current_app, jsonify
from app import get_db
from firebase_admin import firestore
from datetime import datetime


# إنشاء Blueprint للمسارات الرئيسية
bp = Blueprint('main', __name__)


# ==========================================
# 1. الثوابت والروابط الرسمية
# ==========================================
# نضع كل الروابط في مكان واحد لسهولة التعديل مستقبلاً
# ==========================================

SITE_INFO = {
    'name': 'سكن الغرباء الجامعي الخيري',
    'tagline': 'بيئة سكنية آمنة ومهيأة للطلاب، تجمع بين الاستقرار والاهتمام بالتعليم والقيم.',
    'location': 'المكلا - فوه - المساكن - بجانب مسجد البركة',
    'google_maps_url': 'https://maps.app.goo.gl/cmNYs5kSzcgs9tBq8',
}

# معلومات وكالة مسارك كود (المطوّر)
MASAR_CODE = {
    'name': 'وكالة مسارك كود',
    'name_en': 'Masar Code',
    'url': 'https://masar-code-new.vercel.app/?hl=ar-EG#contact',
    'whatsapp': 'https://wa.link/8n06p2',
}

# قائمة المشرفين مع روابط واتساب (منقولة من المعلومات التي أرسلتها)
SUPERVISORS = [
    {
        'id': 1,
        'name': 'المشرف الأول',
        'title': 'مشرف عام السكن',
        'phone_display': '+967 773 614 101',
        'phone_raw': '967773614101',
        'whatsapp': 'https://wa.me/967773614101?text=%D8%A7%D9%84%D8%B3%D9%84%D8%A7%D9%85%20%D8%B9%D9%84%D9%8A%D9%83%D9%85%0A%D8%A3%D8%B1%D8%BA%D8%A8%20%D8%A8%D8%A7%D9%84%D8%AA%D8%B3%D8%AC%D9%8A%D9%84%20%D9%81%D9%8A%20%D8%B3%D9%83%D9%86%20%D8%A7%D9%84%D8%BA%D8%B1%D8%A8%D8%A7%D8%A1%20%D9%88%D9%85%D8%B9%D8%B1%D9%81%D8%A9%20%D8%A7%D9%84%D8%AA%D9%81%D8%A7%D8%B5%D9%8A%D9%84',
    },
    {
        'id': 2,
        'name': 'المشرف الثاني',
        'title': 'مشرف السكن',
        'phone_display': '+967 779 560 300',
        'phone_raw': '967779560300',
        'whatsapp': 'https://wa.me/967779560300?text=%D8%A7%D9%84%D8%B3%D9%84%D8%A7%D9%85%20%D8%B9%D9%84%D9%8A%D9%83%D9%85%20%D8%A3%D8%B1%D8%BA%D8%A8%20%D8%A8%D8%A7%D9%84%D8%AA%D8%B3%D8%AC%D9%8A%D9%84%20%D9%81%D9%8A%20%D8%B3%D9%83%D9%86%20%D8%A7%D9%84%D8%BA%D8%B1%D8%A8%D8%A7%D8%A1%20%D9%88%D9%85%D8%B9%D8%B1%D9%81%D8%A9%20%D8%A7%D9%84%D8%AA%D9%81%D8%A7%D8%B5%D9%8A%D9%84',
    },
]


# ==========================================
# 2. البيانات الاحتياطية (Fallback Data)
# ==========================================
# في حال فشل الاتصال بـ Firebase، نعرض بيانات افتراضية
# حتى لا يظهر الموقع فارغاً أو معطلاً.
# ==========================================

FALLBACK_NOTIFICATIONS = [
    {
        'title': 'بدء التسجيل للفصل الدراسي الجديد',
        'content': 'نعلن عن فتح باب التسجيل للفصل القادم، يرجى تجهيز المستندات المطلوبة والتواصل مع مشرفي السكن.',
        'date': '2026-01-15',
    },
    {
        'title': 'حفل ختامي للأنشطة الطلابية',
        'content': 'يقيم السكن حفلاً ختامياً للأنشطة الطلابية نهاية الشهر الجاري، بحضور المشرفين والطلاب.',
        'date': '2026-01-20',
    },
]

FALLBACK_ACTIVITIES = [
    {
        'title': 'دوري كرة القدم الشهري',
        'description': 'بطولة رياضية تنظم بين فرق السكن لإخراج جوائز رمزية، وتفريغ طاقات الشباب وتعزيز روح المنافسة الشريفة والأخوة.',
        'icon': '⚽',
    },
    {
        'title': 'السمرة المسائية الأسبوعية',
        'description': 'جلسة تجمع الساكنين كل خميس بعد أسبوع دراسي شاق، تتنوع فقراتها بين تلاوات عطرة، وخواطر تربوية، ومسابقات ثقافية مع شاي وقهوة.',
        'icon': '🌙',
    },
    {
        'title': 'الحلقات القرآنية اليومية',
        'description': 'مراجعة وحفظ أجزاء من القرآن الكريم جماعياً أو فردياً بإشراف ومتابعة.',
        'icon': '📖',
    },
    {
        'title': 'الدروس العلمية والتربوية',
        'description': 'دروس في الفقه والسيرة والأخلاق، ومنها درس "الروحة" المذكور في البرنامج اليومي.',
        'icon': '🕌',
    },
    {
        'title': 'الرحلات والأنشطة الترفيهية',
        'description': 'رحلة خلوية أو برية أو زيارة لمكان ترفيهي أو ثقافي مرة كل شهر لكسر روتين الدراسة.',
        'icon': '🏕️',
    },
    {
        'title': 'المسابقات الثقافية والعلمية',
        'description': 'مسابقات في حفظ المتون العلمية، ومسابقات منهجية بين غرف أو أقسام السكن.',
        'icon': '🏆',
    },
    {
        'title': 'أيام العمل التطوعي',
        'description': 'مشاركة الطلاب في أعمال خدمة المجتمع أو تنظيف المساجد والمرافق المحيطة بالسكن لغرس روح البذل والعطاء.',
        'icon': '🤝',
    },
]


# ==========================================
# 3. دوال مساعدة لجلب البيانات من Firebase
# ==========================================

def fetch_from_firebase(collection_name, fallback_data=None, limit=None):
    """
    دالة عامة لجلب البيانات من مجموعة (Collection) في Firebase.
    
    :param collection_name: اسم المجموعة في Firestore.
    :param fallback_data: بيانات بديلة في حال الفشل.
    :param limit: الحد الأقصى لعدد النتائج.
    :return: قائمة من القواميس (Dictionaries).
    """
    try:
        db = get_db()
        query = db.collection(collection_name)
        
        # ترتيب حسب التاريخ إن وُجد، وإلا حسب الترتيب الطبيعي
        try:
            query = query.order_by('date_posted', direction=firestore.Query.DESCENDING)
        except Exception:
            pass  # إذا لم يكن الحقل موجوداً، نتجاهل الترتيب
        
        if limit:
            query = query.limit(limit)
        
        docs = query.stream()
        results = []
        
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            # تنسيق التاريخ لعرضه
            if 'date_posted' in data and isinstance(data['date_posted'], datetime):
                data['date_display'] = data['date_posted'].strftime('%Y-%m-%d')
            results.append(data)
        
        return results if results else (fallback_data or [])
    
    except Exception as e:
        current_app.logger.warning(f"⚠️ تعذر جلب '{collection_name}' من Firebase: {e}")
        return fallback_data or []


# ==========================================
# 4. المسارات (Routes)
# ==========================================

@bp.route('/')
def index():
    """الصفحة الرئيسية للموقع."""
    
    # جلب الإشعارات (آخر اثنين)
    notifications = fetch_from_firebase(
        'notifications',
        fallback_data=FALLBACK_NOTIFICATIONS,
        limit=2
    )
    
    # جلب الأنشطة (آخر ستة)
    activities = fetch_from_firebase(
        'activities',
        fallback_data=FALLBACK_ACTIVITIES,
        limit=7
    )
    
    # تمرير كل البيانات للقالب
    return render_template(
        'index.html',
        site_info=SITE_INFO,
        masar_code=MASAR_CODE,
        supervisors=SUPERVISORS,
        notifications=notifications,
        activities=activities,
        current_year=datetime.now().year,
    )


@bp.route('/health')
def health_check():
    """مسار للتحقق من صحة الموقع واتصاله بـ Firebase (للنشر مستقبلاً)."""
    try:
        db = get_db()
        # محاولة قراءة بسيطة للتأكد من الاتصال
        db.collection('notifications').limit(1).get()
        return jsonify({
            'status': 'ok',
            'firebase': 'connected',
            'message': 'الموقع يعمل بشكل سليم ✅'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'firebase': 'disconnected',
            'message': f'فشل الاتصال بقاعدة البيانات: {str(e)}'
        }), 500