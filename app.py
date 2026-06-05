import streamlit as st
import google.genai as genai
import os
import json
from datetime import datetime

# ====================================
# CONFIGURAÇÃO DA PÁGINA
# ====================================

st.set_page_config(
    page_title="Chat com a Bolha 🫧",
    page_icon="🫧",
    layout="centered"
)

if st.session_state.get("tema", "Claro") == "Claro":
    fundo = "#fff0f5"
    texto = "#000000"
    titulo = "#ff3399"
else:
    fundo = "#121212"
    texto = "#ffffff"
    titulo = "#ff66cc"

st.markdown(f"""
<style>

.stApp {{
    background-color: {fundo};
    color: {texto};
}}

h1, h2, h3 {{
    color: {titulo} !important;
}}

.stChatMessage {{
    border-radius:15px;
    padding:10px;
    margin:5px 0;
}}

</style>
""", unsafe_allow_html=True)

h1, h2, h3 {
    color: #ff3399 !important;
}

.stChatMessage {
    border-radius: 15px;
    padding: 10px;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

st.title("🫧 Conversando com a Bolha!")
st.image(
    "https://cdn-icons-png.flaticon.com/512/4140/4140048.png",
    width=100
)

st.subheader("Sua inteligência artificial descontraída e bem-humorada 😉")

# ====================================
# PASTA DE CONVERSAS
# ====================================

PASTA_CONVERSAS = "conversas"

if not os.path.exists(PASTA_CONVERSAS):
    os.makedirs(PASTA_CONVERSAS)

# ====================================
# API KEY
# ====================================

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.error(
        "⚠️ A variável GEMINI_API_KEY não foi encontrada."
    )
    st.stop()

# ====================================
# PERSONALIDADE DA BOLHA
# ====================================

personalidade = """
Seu nome é Bolha.

Você é uma inteligência artificial feminina,
divertida, engraçada, simpática e muito amigável.

Use emojis naturalmente.
Fale de forma descontraída.
Evite respostas excessivamente formais.
"""

# ====================================
# INICIALIZAÇÃO
# ====================================

if "cliente" not in st.session_state:

    st.session_state.cliente = genai.Client(
        api_key=API_KEY
    )

    st.session_state.chat = (
        st.session_state.cliente.chats.create(
            model="gemini-2.5-flash",
            config=genai.types.GenerateContentConfig(
                system_instruction=personalidade,
                temperature=0.85
            )
        )
    )

if "historico" not in st.session_state:
    st.session_state.historico = []
    
    if "tema" not in st.session_state:
    st.session_state.tema = "Claro"

if "contador_mensagens" not in st.session_state:
    st.session_state.contador_mensagens = 0

# ====================================
# FUNÇÕES
# ====================================

def gerar_titulo():
    if len(st.session_state.historico) == 0:
        return "Conversa_Vazia"

    primeira = st.session_state.historico[0]["texto"]

    titulo = primeira[:30]
    titulo = titulo.replace("/", "-")
    titulo = titulo.replace("\\", "-")
    titulo = titulo.replace(":", "-")

    return titulo


def salvar_conversa():

    titulo = gerar_titulo()

    data = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    nome = f"{data}_{titulo}.json"

    caminho = os.path.join(
        PASTA_CONVERSAS,
        nome
    )

    with open(
        caminho,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            st.session_state.historico,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    return nome


def carregar_conversa(nome_arquivo):

    caminho = os.path.join(
        PASTA_CONVERSAS,
        nome_arquivo
    )

    with open(
        caminho,
        "r",
        encoding="utf-8"
    ) as arquivo:

        st.session_state.historico = json.load(
            arquivo
        )


def excluir_conversa(nome_arquivo):

    caminho = os.path.join(
        PASTA_CONVERSAS,
        nome_arquivo
    )

    if os.path.exists(caminho):
        os.remove(caminho)


# ====================================
# SIDEBAR
# ====================================

with st.sidebar:

    st.header("📁 Conversas")

    if st.button("💾 Salvar conversa"):

        nome = salvar_conversa()

        st.success(
            f"Conversa salva!\n{nome}"
        )

    arquivos = sorted(
        os.listdir(PASTA_CONVERSAS),
        reverse=True
    )

    arquivos_json = [
        a for a in arquivos
        if a.endswith(".json")
    ]

    if arquivos_json:

        conversa = st.selectbox(
            "📜 Conversas salvas",
            arquivos_json
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button("📂 Carregar"):

                carregar_conversa(conversa)

                st.success(
                    "Conversa carregada!"
                )

                st.rerun()

        with col2:

            if st.button("🗑️ Excluir"):

                excluir_conversa(conversa)

                st.success(
                    "Conversa excluída!"
                )

                st.rerun()

    st.divider()

    if st.button("✨ Nova conversa"):

        st.session_state.historico = []

        st.session_state.chat = (
            st.session_state.cliente.chats.create(
                model="gemini-2.5-flash",
                config=genai.types.GenerateContentConfig(
                    system_instruction=personalidade,
                    temperature=0.85
                )
            )
        )

        st.rerun()

# ====================================
# MOSTRAR HISTÓRICO
# ====================================

for mensagem in st.session_state.historico:

    with st.chat_message(
        mensagem["autor"],
        avatar=mensagem["avatar"]
    ):

        st.write(mensagem["texto"])

# ====================================
# CHAT
# ====================================

if texto_usuario := st.chat_input(
    "Diga um oi para a Bolha..."
):

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.write(texto_usuario)

    st.session_state.historico.append({
        "autor": "user",
        "texto": texto_usuario,
        "avatar": "👤"
    })

    with st.chat_message(
        "assistant",
        avatar="🫧"
    ):

    placeholder = st.empty()

placeholder.info(
    "🫧 Bolha está pensando em algo divertido..."
)
        ):

            try:

                resposta = (
                    st.session_state.chat
                    .send_message(texto_usuario)
                )

                st.write(resposta.text)
                
                placeholder = st.empty()

placeholder.info(
    "🫧 Bolha está pensando em algo divertido..."
)

                st.session_state.historico.append({
                    "autor": "assistant",
                    "texto": resposta.text,
                    "avatar": "🫧"
                })

            except Exception as e:

                st.error(
                    f"Erro: {e}"
                )