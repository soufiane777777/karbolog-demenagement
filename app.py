import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Karbo Déménagement", layout="wide")

# Sélecteur de langue
langue = st.selectbox("Choisissez la langue / Choose language / اختر اللغة", ["Français", "English", "العربية"])

# Dictionnaire des textes
texts = {
    "Français": {
        "title": "🚛 Karbo Déménagement",
        "subtitle": "Recevez un devis gratuit en quelques clics !",
        "separator": "---",
        "header1": "1️⃣ Vos coordonnées",
        "label_nom": "Nom complet",
        "label_telephone": "Téléphone",
        "label_email": "Adresse email",
        "header2": "2️⃣ Adresse de départ et d’arrivée",
        "label_adresse_depart": "Adresse de départ",
        "label_etage_depart": "Étage de départ",
        "label_ascenseur_depart": "Ascenseur ?",
        "label_adresse_arrivee": "Adresse d’arrivée",
        "label_etage_arrivee": "Étage d’arrivée",
        "label_ascenseur_arrivee": "Ascenseur ?",
        "header3": "3️⃣ Liste des meubles à déménager",
        "liste_meubles": ["Lit", "Canapé", "Table", "Chaise", "Armoire", "Réfrigérateur", "Lave-linge", "Télévision", "Bureau", "Cartons"],
        "volume_total": "📦 Volume total estimé : **{:.1f} m³**",
        "camion_recommande": "🚚 {}",
        "header4": "4️⃣ Date souhaitée pour le déménagement",
        "header5": "5️⃣ Commentaires ou besoins spécifiques",
        "label_commentaires": "Ajoutez vos remarques ici",
        "btn_send": "📨 Envoyer la demande",
        "success_msg": "Votre demande a été envoyée avec succès ! ✅",
        "etages": ["RDC", "1er", "2e", "3e", "4e ou plus"],
        "ascenseur_options": ["Oui", "Non"],
    },
    "English": {
        "title": "🚛 Karbo Moving",
        "subtitle": "Get a free quote in a few clicks!",
        "separator": "---",
        "header1": "1️⃣ Your contact details",
        "label_nom": "Full name",
        "label_telephone": "Phone",
        "label_email": "Email address",
        "header2": "2️⃣ Departure and arrival address",
        "label_adresse_depart": "Departure address",
        "label_etage_depart": "Departure floor",
        "label_ascenseur_depart": "Elevator?",
        "label_adresse_arrivee": "Arrival address",
        "label_etage_arrivee": "Arrival floor",
        "label_ascenseur_arrivee": "Elevator?",
        "header3": "3️⃣ List of furniture to move",
        "liste_meubles": ["Bed", "Sofa", "Table", "Chair", "Wardrobe", "Fridge", "Washing machine", "TV", "Desk", "Boxes"],
        "volume_total": "📦 Estimated total volume: **{:.1f} m³**",
        "camion_recommande": "🚚 {}",
        "header4": "4️⃣ Desired moving date",
        "header5": "5️⃣ Comments or specific needs",
        "label_commentaires": "Add your remarks here",
        "btn_send": "📨 Send request",
        "success_msg": "Your request has been sent successfully! ✅",
        "etages": ["Ground floor", "1st", "2nd", "3rd", "4th or higher"],
        "ascenseur_options": ["Yes", "No"],
    },
    "العربية": {
        "title": "🚛 كاربو للنقل",
        "subtitle": "احصل على عرض مجاني خلال نقرات قليلة!",
        "separator": "---",
        "header1": "1️⃣ بيانات الاتصال الخاصة بك",
        "label_nom": "الاسم الكامل",
        "label_telephone": "الهاتف",
        "label_email": "البريد الإلكتروني",
        "header2": "2️⃣ عنوان الانطلاق والوصول",
        "label_adresse_depart": "عنوان الانطلاق",
        "label_etage_depart": "طابق الانطلاق",
        "label_ascenseur_depart": "مصعد؟",
        "label_adresse_arrivee": "عنوان الوصول",
        "label_etage_arrivee": "طابق الوصول",
        "label_ascenseur_arrivee": "مصعد؟",
        "header3": "3️⃣ قائمة الأثاث للنقل",
        "liste_meubles": ["سرير", "أريكة", "طاولة", "كرسي", "خزانة", "ثلاجة", "غسالة", "تلفاز", "مكتب", "صناديق"],
        "volume_total": "📦 الحجم الإجمالي المقدر: **{:.1f} م³**",
        "camion_recommande": "🚚 {}",
        "header4": "4️⃣ التاريخ المطلوب للنقل",
        "header5": "5️⃣ التعليقات أو الاحتياجات الخاصة",
        "label_commentaires": "أضف ملاحظاتك هنا",
        "btn_send": "📨 إرسال الطلب",
        "success_msg": "تم إرسال طلبك بنجاح! ✅",
        "etages": ["الدور الأرضي", "الأول", "الثاني", "الثالث", "الرابع أو أعلى"],
        "ascenseur_options": ["نعم", "لا"],
    }
}

# Injecter CSS RTL si arabe
if langue == "العربية":
    st.markdown(
        """
        <style>
        body, .css-18e3th9 {
            direction: rtl;
            text-align: right;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Connexion à la base SQLite (création si inexistante)
conn = sqlite3.connect("demenagement.db")
c = conn.cursor()

# Création de la table demandes si elle n'existe pas
c.execute("""
CREATE TABLE IF NOT EXISTS demandes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    telephone TEXT,
    email TEXT,
    adresse_depart TEXT,
    etage_depart TEXT,
    ascenseur_depart TEXT,
    adresse_arrivee TEXT,
    etage_arrivee TEXT,
    ascenseur_arrivee TEXT,
    meubles TEXT,
    volume_total REAL,
    camion_recommande TEXT,
    date_demenagement TEXT,
    commentaires TEXT,
    date_enregistrement TEXT
)
""")
conn.commit()

st.title(texts[langue]["title"])
st.subheader(texts[langue]["subtitle"])
st.markdown(texts[langue]["separator"])

# === Étape 1 : Coordonnées ===
st.header(texts[langue]["header1"])
nom = st.text_input(texts[langue]["label_nom"])
telephone = st.text_input(texts[langue]["label_telephone"])
email = st.text_input(texts[langue]["label_email"])

# === Étape 2 : Adresse de départ et d’arrivée ===
st.header(texts[langue]["header2"])
col1, col2 = st.columns(2)

with col1:
    adresse_depart = st.text_input(texts[langue]["label_adresse_depart"])
    etage_depart = st.selectbox(texts[langue]["label_etage_depart"], texts[langue]["etages"])
    ascenseur_depart = st.radio(texts[langue]["label_ascenseur_depart"], texts[langue]["ascenseur_options"], key="asc_dep")

with col2:
    adresse_arrivee = st.text_input(texts[langue]["label_adresse_arrivee"])
    etage_arrivee = st.selectbox(texts[langue]["label_etage_arrivee"], texts[langue]["etages"])
    ascenseur_arrivee = st.radio(texts[langue]["label_ascenseur_arrivee"], texts[langue]["ascenseur_options"], key="asc_arr")

# === Étape 3 : Liste des meubles ===
st.header(texts[langue]["header3"])

meubles = {}
liste_meubles = texts[langue]["liste_meubles"]

col1, col2 = st.columns(2)
for i, meuble in enumerate(liste_meubles):
    with (col1 if i % 2 == 0 else col2):
        meubles[meuble] = st.number_input(f"{meuble}", min_value=0, step=1, key=meuble)

# === Étape 4 : Calcul du volume total ===
# Volume par meuble (attention : les noms doivent correspondre à ceux en français pour la clé du dict)
# Pour l'anglais et arabe, on traduit le dict clef -> valeur en gardant les mêmes volumes

volumes_fr = {
    "Lit": 3,
    "Canapé": 1.5,
    "Table": 2,
    "Chaise": 0.5,
    "Armoire": 2.20,
    "Réfrigérateur": 1.5,
    "Lave-linge": 1.5,
    "Télévision": 0.3,
    "Bureau": 2,
    "Cartons": 0.1
}

volumes_en = {
    "Bed": 3,
    "Sofa": 1.5,
    "Table": 2,
    "Chair": 0.5,
    "Wardrobe": 2.20,
    "Fridge": 1.5,
    "Washing machine": 1.5,
    "TV": 0.3,
    "Desk": 2,
    "Boxes": 0.1
}

volumes_ar = {
    "سرير": 3,
    "أريكة": 1.5,
    "طاولة": 2,
    "كرسي": 0.5,
    "خزانة": 2.20,
    "ثلاجة": 1.5,
    "غسالة": 1.5,
    "تلفاز": 0.3,
    "مكتب": 2,
    "صناديق": 0.1
}

if langue == "Français":
    volume_par_meuble = volumes_fr
elif langue == "English":
    volume_par_meuble = volumes_en
else:
    volume_par_meuble = volumes_ar

volume_total = sum(volume_par_meuble.get(m, 0) * q for m, q in meubles.items())

# === Étape 5 : Recommandation de camion ===
if volume_total <= 20:
    camion = texts[langue]["camion_recommande"].format(
        "✅ Camion 7T recommandé (max 20 m³)" if langue == "Français" else
        "✅ 7T truck recommended (max 20 m³)" if langue == "English" else
        "✅ شاحنة 7 طن موصى بها (حد أقصى 20 م³)"
    )
elif volume_total <= 26:
    camion = texts[langue]["camion_recommande"].format(
        "✅ Camion 14T recommandé (max 26 m³)" if langue == "Français" else
        "✅ 14T truck recommended (max 26 m³)" if langue == "English" else
        "✅ شاحنة 14 طن موصى بها (حد أقصى 26 م³)"
    )
elif volume_total <= 35:
    camion = texts[langue]["camion_recommande"].format(
        "✅ 2 Camions 7T recommandé (max 26 m³)" if langue == "Français" else
        "✅ 2x 7T trucks recommended (max 26 m³)" if langue == "English" else
        "✅ شاحنتان 7 طن موصى بهما (حد أقصى 26 م³)"
    )
else:
    camion = texts[langue]["camion_recommande"].format(
        "🚫 Volume trop élevé, plusieurs camions nécessaires" if langue == "Français" else
        "🚫 Volume too high, multiple trucks needed" if langue == "English" else
        "🚫 الحجم كبير جدًا، يلزم عدة شاحنات"
    )

st.markdown(texts[langue]["volume_total"].format(volume_total))
st.markdown(camion)

# === Étape 6 : Date souhaitée ===
st.header(texts[langue]["header4"])
date_demenagement = st.date_input("")

# === Étape 7 : Commentaires ===
st.header(texts[langue]["header5"])
commentaires = st.text_area(texts[langue]["label_commentaires"])

# === Bouton de validation ===
if st.button(texts[langue]["btn_send"]):
    meubles_str = ", ".join(f"{m}: {q}" for m, q in meubles.items())
    date_enregistrement = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("""
        INSERT INTO demandes (
            nom, telephone, email,
            adresse_depart, etage_depart, ascenseur_depart,
            adresse_arrivee, etage_arrivee, ascenseur_arrivee,
            meubles, volume_total, camion_recommande,
            date_demenagement, commentaires, date_enregistrement
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        nom, telephone, email,
        adresse_depart, etage_depart, ascenseur_depart,
        adresse_arrivee, etage_arrivee, ascenseur_arrivee,
        meubles_str, volume_total, camion,
        date_demenagement.strftime("%Y-%m-%d"), commentaires, date_enregistrement
    ))
    conn.commit()

    st.success(texts[langue]["success_msg"])
    st.balloons()
