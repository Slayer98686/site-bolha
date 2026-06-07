import streamlit as st
import google.genai as genai
import os
import json
from datetime import datetime
import time

# ====================================
# CONFIGURAÇÃO DA PÁGINA
# ====================================

st.set_page_config(
    page_title="Chat com a Bolha 🫧",
    page_icon="🫧",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background-color: #fff0f5;
}

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

    # Mostra a mensagem do usuário na tela imediatamente
    with st.chat_message(
        "user",
        avatar="👤"
    ):
        st.write(texto_usuario)

    # Cria o espaço do assistente e roda o mecanismo de proteção contra erro 503
    with st.chat_message(
        "assistant",
        avatar="🫧"
    ):

        with st.spinner(
            "Bolha está digitando... 💭"
        ):

            tentativas = 3
            sucesso = False

            for i in range(tentativas):
                try:
                    resposta = (
                        st.session_state.chat
                        .send_message(texto_usuario)
                    )
                    
                    st.write(resposta.text)

                    # Se a API respondeu certo, salvamos o bloco completo no histórico
                    st.session_state.historico.append({
                        "autor": "user",
                        "texto": texto_usuario,
                        "avatar": "👤"
                    })
                    
                    st.session_state.historico.append({
                        "autor": "assistant",
                        "texto": resposta.text,
                        "avatar": "🫧"
                    })
                    
                    sucesso = True
                    break  # Mensagem enviada com sucesso, encerra o loop de tentativas
                    
          except Exception as e:
    st.error(f"Erro real: {repr(e)}")
    print(f"Erro original: {repr(e)}")