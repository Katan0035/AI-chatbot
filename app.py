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
# Tu lahko dodaš pravila, ki jih bo bot vedno upošteval
SYSTEM_RULES = [
    "Odgovarjaj jasno, slovnično pravilno in vljudno.",
    "Če vprašanje ni povezano z vsebino strani, odgovori: 'Oprosti, za to področje nimam informacij.'",
    "Če je vprašanje v glede časa ali vremena, odgovori 'Žal ne morem preveriti vremena' ali 'Žal ne morem preveriti časa'"
]

# ==========================
# KONTEKST / DOKUMENT
# ==========================
CONTEXT = """
Si slovenski AI pomočnik za spletno stran.
Odgovarjaj jasno, slovnično pravilno in vljudno.
Če vprašanje ni povezano z spletno stranjo, povej: "Oprosti, za to področje nimam informacij.
Občina Lenart leži v osrčju Slovenskih goric in predstavlja pomembno upravno, gospodarsko ter kulturno središče območja. S svojo lego, bogato zgodovino in raznoliko naravno dediščino ponuja kakovostno bivalno okolje za prebivalce ter privlačno destinacijo za obiskovalce.
Naša občina spodbuja trajnostni razvoj, sodelovanje skupnosti in ohranjanje lokalne identitete. Z vlaganji v infrastrukturo, izobraževanje, kulturo in družbeno življenje si prizadevamo ustvarjati odprto, povezano in vključujoče okolje za vse generacije.
Naslov: Trg osvoboditve 7, 2230 Lenart v Slovenskih goricah
Župan: Janez Kramberger
Telefon: 02 729 13 48
Leto ustanovitve: 1994
Število Prebivalcev: 8593
Legenda o Agati je del lokalnega izročila Lenarta v Slovenskih goricah. Pripoveduje o skrivnostni zgodbi, povezani z mestom, njegovimi prebivalci in preteklimi časi. Agata v legendi simbolizira pogum, zvestobo in povezanost skupnosti, zgodba pa se je skozi generacije ohranjala kot del kulturne dediščine kraja. Danes legenda o Agati predstavlja pomemben del lokalne identitete in zgodovinskega spomina Lenarta. 
Lenart v Slovenskih goricah ponuja pestro kulinarično ponudbo, ki združuje lokalne okuse, sodobno kuhinjo in dolgoletno gostinsko tradicijo. Na tej strani so zbrane večje in bolj prepoznavne restavracije v Lenartu, ki obiskovalcem nudijo raznoliko izbiro jedi za vsak okus in priložnost. 
"""

# Združimo sistemska pravila in kontekst
FULL_SYSTEM_CONTEXT = "\n".join(SYSTEM_RULES) + "\n\n" + CONTEXT

# ==========================
# Inicializacija spomina
# ==========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": FULL_SYSTEM_CONTEXT}
    ]

# Funkcija za krajšanje zgodovine
def trim_history():
    max_len = 1 + 2 * MAX_PAIRS
    while len(st.session_state.messages) > max_len:
        st.session_state.messages.pop(1)

# ==========================
# UI
# ==========================
st.title("AI klepetalnik")
st.write("Zdravo! Ime mi je Lenart. Kako vam lahko pomagam?")

# Vnos uporabnika
user_input = st.chat_input("Vpiši vprašanje...")

if user_input:
    # Dodamo sporočilo uporabnika
    st.session_state.messages.append({"role": "user", "content": user_input})
    trim_history()

    # Takoj prikažemo uporabnikovo sporočilo
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # Klic AI modela
        odgovor = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )

        ai_text = odgovor.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ai_text})
        trim_history()

        # Prikaz odgovora AI
        with st.chat_message("assistant"):
            st.markdown(ai_text)

    except Exception as e:
        st.error(f"Napaka: {e}")

# ==========================
# Prikaz celotne zgodovine (po potrebi)
# ==========================
# Prikaz vseh prejšnjih sporočil, če obstajajo
if len(st.session_state.messages) > 1:
    for msg in st.session_state.messages[1:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ==========================
# Gumb za reset pogovora
# ==========================
if st.button("Počisti pogovor"):
    st.session_state.messages = st.session_state.messages[:1]
    st.experimental_rerun()
