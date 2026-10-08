import random

# Yutqazgan ishtirokchi uchun qiziqarli va kulgili shartlar / jazolar ro'yxati
PENALTIES = [
    "🎤 Guruhga 15 soniyalik audio yuboring: multfilm qahramoni yoki robot ovozida gapiring!",
    "✍️ G'olib ishtirokchi sharafiga 4 qatorli ekspromt she'r to'qib yozing!",
    "🌟 Guruhdagi tasodifiy bir ishtirokchiga chin dildan eng chiroyli maqtov/kompliment yozing!",
    "😂 O'zingiz bilgan eng kulgili latifani guruhga yozib bering!",
    "🎵 Sevimli qo'shig'ingizning naqoratini ovozli xabarda (audio) xonish qilib bering!",
    "🤐 Keyingi 10 daqiqa davomida guruhda faqat stiker va emojilar bilan yozishingiz mumkin (so'z ishlatish taqiqlanadi)!",
    "🗣️ 'Oq choynakka oq qopqoq, ko'k choynakka ko'k qopqoq' tez aytishini 3 marta tez va adashmasdan ovozli xabarda ayting!",
    "👑 Bugun kun oxirigacha g'olibga 'Hurmatli Chempion Janoblari' deb murojaat qiling!",
    "🤣 Telefoningizdagi eng kulgili stiker yoki memni guruhga tashlang!",
    "📢 Guruhga rasmiy xabar shaklida: 'Men tantanali ravishda mag'lubiyatimni tan olaman!' deb yozing!",
    "🧠 O'zingiz bilgan eng qiziqarli yoki g'alati faktni guruhga ulashing!",
    "🤖 5 daqiqa davomida o'zingizni sun'iy intellekt (bot) deb tuting va har bir savolga shunday javob bering!",
    "☕️ Ertaga g'olibga virtual (yoki real) qahva olib berishni va'da qiling!",
    "🎭 Guruhga harflar bilan emas, faqat imo-ishorali emojilar bilan jumboq yozing, boshqalar topsin!",
    "🧘‍♂️ 5 ta chuqur nafas oling va guruhga tinchlik tilab chiroyli tilak qoldiring!"
]

def get_random_penalty() -> str:
    """Tasodifiy jazo/shartni qaytaradi"""
    return random.choice(PENALTIES)
