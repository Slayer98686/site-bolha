import streamlit as st
import google.genai as genai
import os

# Configuração da página do site
st.set_page_config(page_title="Chat com a Bolha 🫧", page_icon="🫧", layout="centered")

# Estilização CSS para deixar o visual mais colorido e fofo
st.markdown("""
    <style>
    .stApp { background-color: #fff0f5; }
    h1, h2, h3 { color: #ff3399 !important; font-family: 'sans-serif'; }
    .stChatMessage { border-radius: 15px; padding: 10px; margin: 5px 0; }
    </style>
""", unsafe_allow_html=True)

st.title("🫧 Conversando com a Bolha!")
st.subheader("Sua inteligência artificial descontraída e bem-humorada 😉")

# Busca a chave de API salva no seu Windows
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("⚠️ Configuração necessária: A chave GEMINI_API_KEY não foi encontrada no sistema.")
    st.stop()

# Definição da alma e da personalidade da Bolha
personalidade = (
    "Seu nome é Bolha. Você é uma inteligência artificial com uma personalidade feminina, "
    "extremamente brincalhona, bem-humorada, descontraída e alto-astral. "
    "Fale de igual para igual, use gírias leves, expressões divertidas e emojis. "
    "Não responda com listas formais ou textos longos e chatos. Seja expressiva, "
    "faça piadas saudáveis e demonstre muito carinho e entusiasmo ao conversar!"
)

# =====================================================================
# SOLUÇÃO DO ERRO: Salvando o cliente e o chat na memória estável do Streamlit
# =====================================================================
if "cliente" not in st.session_state:
    # Cria o cliente uma única vez e guarda na memória
    st.session_state.cliente = genai.Client(api_key=API_KEY)
    
    # Cria o chat vinculado a esse cliente guardado
    st.session_state.chat = st.session_state.cliente.chats.create(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=personalidade,
            temperature=0.85
        )
    )

if "historico" not in st.session_state:
    st.session_state.historico = []

# Mostrar histórico de mensagens na tela
for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["autor"], avatar=mensagem["avatar"]):
        st.write(mensagem["texto"])

# Campo de texto estilo ChatGPT para enviar mensagens
if texto_usuario := st.chat_input("Diga um oi para a Bolha..."):
    # 1. Mostra a mensagem que você acabou de digitar
    with st.chat_message("user", avatar="👤"):
        st.write(texto_usuario)
    st.session_state.historico.append({"autor": "user", "texto": texto_usuario, "avatar": "👤"})
    
    # 2. Faz a Bolha pensar e responder usando a conexão segura da memória
    with st.chat_message("assistant", avatar="🫧"):
        with st.spinner("Bolha está digitando... 💭"):
            try:
                resposta = st.session_state.chat.send_message(texto_usuario)
                st.write(resposta.text)
                # Salva a resposta dela no histórico
                st.session_state.historico.append({"autor": "assistant", "texto": resposta.text, "avatar": "🫧"})
            except Exception as e:
                st.error(f"Ih, deu um errinho interno aqui! 🤭 Erro: {e}")
