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
        "🎙️ 30 soniya davomida o'zingizni prezident deb tasavvur qiling va guruhga mamlakatni rivojlantirish bo'yicha jiddiy nutq so'zlang!",

    "⚖️ G'olibni sudya deb tan oling va 3 ta sabab bilan nega mag'lub bo'lganingizni sud majlisida himoya qilayotgandek tushuntiring!",

    "📺 Guruhga xuddi televizordagi yangiliklar boshlovchisidek jiddiy ohangda o'z mag'lubiyatingiz haqida maxsus reportaj yozing!",

    "🧑‍💼 2 daqiqa davomida guruhdagi oddiy savollarga ham xuddi katta kompaniya direktori kabi rasmiy va jiddiy javob bering!",

    "🎤 20 soniyalik audio yuboring: o'zingizni dunyodagi eng buyuk motivator deb hisoblab, guruhni hayotda muvaffaqiyatga erishishga undang!",

    "🕵️ 3 ta kulgili yolg'on detektori savolini o'ylab toping va g'olibdan jiddiy tergovchi kabi so'rang!",

    "🏆 G'olib uchun tantanali mukofot topshirish marosimi tashkil qiling: kamida 4 qatorlik dabdabali tabrik nutqi yozing!",

    "📜 O'z mag'lubiyatingiz haqida rasmiy farmon yozing. Unda kamida 3 ta modda bo'lsin va oxirida o'zingiz imzo qo'ying!",

    "🧑‍🏫 30 soniyalik audio yuboring: 'Nega men yutqazdim?' mavzusida xuddi universitet professori kabi ilmiy ma'ruza qiling!",

    "🚨 Guruhga favqulodda vaziyatlar xizmati xodimi kabi jiddiy ogohlantirish yozing: 'Diqqat! Guruhda juda kuchli chempion aniqlandi. Barcha mag'lublar ehtiyot choralarini ko'rsin!'"
    "📸Hoziroq o'zingizni suratga oling va guruhga yuboring!"
]

def get_random_penalty() -> str:
    """Tasodifiy jazo/shartni qaytaradi"""
    return random.choice(PENALTIES)
