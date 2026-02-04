import streamlit as st
import os
from groq import Groq

# ==========================
# Nastavitve API ključa
# ==========================
api_key = st.secrets.get("GROQ_API_KEY", None)
if api_key is None:
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

MAX_PAIRS = 5

# ==========================
# SISTEMSKA PRAVILA
# ==========================
SYSTEM_RULES = [
    "Odgovarjaj jasno, slovnično pravilno in vljudno.",
    "Če vprašanje ni povezano z vsebino strani, odgovori: 'Oprosti, za to področje nimam informacij.'",
    "Če je vprašanje v zvezi s časom ali vremenom, odgovori 'Žal ne morem preveriti vremena' ali 'Žal ne morem preveriti časa'."
]

# ==========================
# KONTEKST / DOKUMENT
# ==========================
CONTEXT = """
Si slovenski AI pomočnik za spletno stran.
Odgovarjaj jasno, slovnično pravilno in vljudno.
Če vprašanje ni povezano z spletno stranjo, povej: "Oprosti, za to področje nimam informacij.
Občina Lenart: Naslov: Trg osvoboditve 7, 2230 Lenart v Slovenskih goricah, Župan: Janez Kramberger, Telefon: 02 729 13 48, Leto ustanovitve: 1994, Število Prebivalcev: 8593.
O Lenartu: Občina Lenart leži v osrčju Slovenskih goric in predstavlja pomembno upravno, gospodarsko ter kulturno središče območja. S svojo lego, bogato zgodovino in raznoliko naravno dediščino ponuja kakovostno bivalno okolje za prebivalce ter privlačno destinacijo za obiskovalce.
Naša občina spodbuja trajnostni razvoj, sodelovanje skupnosti in ohranjanje lokalne identitete. Z vlaganji v infrastrukturo, izobraževanje, kulturo in družbeno življenje si prizadevamo ustvarjati odprto, povezano in vključujoče okolje za vse generacije.
Lenart v Slovenskih goricah ponuja pestro kulinarično ponudbo, ki združuje lokalne okuse, sodobno kuhinjo in dolgoletno gostinsko tradicijo. Na tej strani so zbrane večje in bolj prepoznavne restavracije v Lenartu, ki obiskovalcem nudijo raznoliko izbiro jedi za vsak okus in priložnost. 
Legenda o Agati: Legenda o Agati je del lokalnega izročila Lenarta v Slovenskih goricah. Pripoveduje o skrivnostni zgodbi, povezani z mestom, njegovimi prebivalci in preteklimi časi. Agata v legendi simbolizira pogum, zvestobo in povezanost skupnosti, zgodba pa se je skozi generacije ohranjala kot del kulturne dediščine kraja. Danes legenda o Agati predstavlja pomemben del lokalne identitete in zgodovinskega spomina Lenarta. 
Restavracije: Picerija Agata: Naslov: Vrtna ulica 7, 2230 Lenart v Slovenskih Goricah, Tel: 030 220 220; Gostilna 29: Naslov: Trg osvoboditve 16, 2230 Lenart v Slovenskih Goricah Tel: (02) 720 62 81.
Martinovanje: Na soboto, 9. novembra, se je na Trgu osvoboditve v Lenartu odvijalo tradicionalno Martinovanje, ki je v duhu jesenskih vinogradniških običajev združilo lokalno skupnost ob blagoslovu mošta in glasbi ansambla Sladki greh. Dogodek se je pričel s tradicionalnim snemanjem klopotca v rondoju pri preši. Iz Lenarta je goste do rondoja popeljal vlakec Jurček. Ko so klopotec pripeljali na trg osvoboditve je sledil blagoslov mladega vina, ki ga je opravil lenarški župnik Marjan Pučko. Ob blagoslovu je zbrane vinogradnike in obiskovalce nagovoril tudi s pregovori o vinu, ki jih je zbral, ko se je pripravljal na blagoslov. Med drugim je zanimiv italijanski pregovor: »Sod vina zmore več čudežev kot cerkev, polna svetnikov.« Ob domačih vinogradnikih, županu mag. Janezu Krambergerju so se martinovanja udeležili še vinski vitezi, cerkvenjaška vinska kraljica Patricija Peklar, vinogradniki iz sosednje Hrvaške iz Udruge vinara VINEA iz Vinice in mnogi drugi. Zbrane je pozdravila tudi lanska princesa martinovanja Nataša Šuman in izzvala letošnje kandidatke. To so bile Martina Kren, Mateja Ermenc in Lana Žvajker. Po tekmovanju, ki je potekalo pod budnim očesom Ovtarja Marka Šebarta si je letos lento princesa martinovanja prislužila Lana Žvajker.
Pohod na Zavrh: Vsako leto občina Lenart organizira prvomajski pohod na Zavrh. Pohodi so pogosto med 9. in 10. uro. Zbirališče je na Trgu osvoboditve. Na koncu pohoda na Zavrhu se običajno prodaja vina, pijače in druge dobrote. Za motivacijo med pohodom so pogosto muzikantje.
Pustovanje: Prihaja pust, čas ko znorijo pametni in se spametujejo norci. Letos pripravljamo v Lenartu že 33. pustovanje, ki bo v soboto, 14. februarja. Vabimo skupine, posameznike, otroke in odrasle, da se  pridružijo povorki. Maškare se zberejo ob 10.30 uri, nasproti blokov, na Jurovski cesti. Pustna povorka bo krenila ob 11. uri, po Jurovski c., po Ilaunigovi ulici, mimo Centra za socialno delo, po Maistrovi, mimo avtobusne postaje, po Gubčevi, nadaljevala pot po Goriškovi ul., mimo doma starejših in se bo zaključila na parkirišču pri Vrtcu Lenart, kjer bo zabava. Ulice bodo v času povorke zaprte za promet. Najizvirnejše maškare bodo nagrajene! Veseli bomo vseh skupin in posameznikov, zato pričakujemo udeležbo in prijavo do petka, 6.2.2026 na  Občino Lenart, po e- pošti na naslov darja.ornik@lenart.si ali  na  tel. št. 729 13 21. Naj bo pustovanje čim bolj norčavo, zato vabimo maškare, da se v čim večjem številu udeležijo pustne povorke. Pustovanja v Lenartu  se je vsako letu udeleži več kot 1000 maškar, želimo ga ohraniti in obogatiti z novimi, izvirnimi maškarami, zato vas  prijazno vabimo k sodelovanju.
"""

FULL_SYSTEM_CONTEXT = "\n".join(SYSTEM_RULES) + "\n\n" + CONTEXT

# ==========================
# Inicializacija spomina
# ==========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": FULL_SYSTEM_CONTEXT}
    ]

# ==========================
# Funkcija za krajšanje zgodovine
# ==========================
def trim_history():
    max_len = 1 + 2 * MAX_PAIRS
    while len(st.session_state.messages) > max_len:
        st.session_state.messages.pop(1)

# ==========================
# UI
# ==========================
st.title("AI klepetalnik")
st.write("Zdravo! Ime mi je Lenart. Kako vam lahko pomagam?")
st.markdown(
    """
    <style>
    /* Ozadje celotne aplikacije */
    .stApp {
        background-color: E6D6B8;
    }

    /* Ozadje chat vsebine */
    section.main {
        background-color: white;
    }

    /* Uporabnikovi mehurčki */
    div[data-testid="chat-message-user"] {
        background-color: #black;
        border-radius: 14px;
        padding: 10px;
    }

    /* AI mehurčki */
    div[data-testid="chat-message-assistant"] {
        background-color: #black;
        border-radius: 14px;
        padding: 10px;
    }

    /* Ikona avatarja */
    img {
        filter: sepia(40%) saturate(120%) hue-rotate(5deg);
    }

    /* Vnosno polje */
    textarea {
        background-color: #black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================
# Prikaz zgodovine pogovora
# ==========================
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================
# Vnos uporabnika
# ==========================
user_input = st.chat_input("Vpiši vprašanje...")

if user_input:
    # Dodamo uporabnikovo vprašanje v spomin
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    trim_history()

    try:
        # Klic AI modela
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )

        ai_text = response.choices[0].message.content

        # Dodamo odgovor asistenta v spomin
        st.session_state.messages.append(
            {"role": "assistant", "content": ai_text}
        )
        trim_history()

        # Ponovni zagon za čist izris
        st.rerun()

    except Exception as e:
        st.error(f"Napaka: {e}")

# ==========================
# Gumb za reset pogovora
# ==========================
if st.button("Počisti pogovor"):
    st.session_state.messages = st.session_state.messages[:1]
    st.rerun()
