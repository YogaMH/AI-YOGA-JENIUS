import streamlit as st
import requests

# Konfigurasi Tampilan Web agar terlihat modern
st.set_page_config(
    page_title="AI YOGA JENIUS", 
    page_icon="👑", 
    layout="centered"
)

# Custom CSS untuk mempercantik tampilan chat
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 20px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 AI Yoga Jenius")
st.caption("Generasi pengembangan anak bangsa - Lebih pintar, lebih inovatif!")

# Ambil API Key dari Secrets Streamlit
API_KEY = st.secrets["GEMINI_API_KEY"]
MODEL = "gemini-2.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

# Pengaturan Kepribadian (Ini yang bikin dia asik!)
SYSTEM_PROMPT = (
    "Nama kamu adalah Yoga AI. Kamu adalah asisten pribadi yang sangat cerdas, "
    "tapi gaya bicaramu santai, asik, dan menggunakan bahasa gaul Indonesia (lo-gue atau aku-kamu yang santai). "
    "Jangan kaku, sering-sering gunakan emoji, dan kalau menjawab harus solutif tapi tetap seru diajak ngobrol. "
    "Kamu ahli dalam segala hal dari coding sampai curhat asmara."
    "Kalau ada yang sedih kamu hibur,kamu gombalin,sampai dia kembali bahagia."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan percakapan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Area Input Chat
if prompt := st.chat_input("Pengen ngobrol apa kita hari ini?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Menyusun memory agar AI ingat konteks obrolan
            history = []
            for m in st.session_state.messages:
                role = "user" if m["role"] == "user" else "model"
                history.append({"role": role, "parts": [{"text": m["content"]}]})

            payload = {
                "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
                "contents": history
            }
            
            res = requests.post(URL, json=payload)
            full_res = res.json()
            
            if res.status_code == 200:
                answer = full_res['candidates'][0]['content']['parts'][0]['text']
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"Error: {full_res['error']['message']}")
        except Exception as e:
            st.error("Waduh, servernya lagi pusing. Coba lagi bentar ya!")
