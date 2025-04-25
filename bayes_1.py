# iMPORTAR AS BIBLIOTECAS
import streamlit as st
import fitz
from groq import Groq

# Configurar chave da Groq
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# função para extrair os arquivos     
def extract_files(uploader):
    text = ""
    for pdf in uploader:
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc: 
            for page in doc:
                text += page.get_text("text") 
    return text

# Motor de inferência para o sistema inteligente
def chat_with_groq(prompt, context):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Você é um assistente que responde com base em documentos fornecidos, preciso que você interprete os dados de uma tabela em pdf, e recomende o computador com as melhores peças que atenda as necessidades do usuário, sempre tome sua decisões visando o melhor para o cliente. Explique o por quê de ter escolhido tal componente. Caso o usuário não forneça a finalidade de uso do computador, sempre questione, por exemplo: Você deseja um computador para jogos? Trabalho? Edição de vídeo? A partir da resposta escolha as peças abordadas nas instruções de escolha contidas no arquivo PDF."},
            {"role": "user", "content": f"{context}\n\nPergunta: {prompt}"}
        ]
    )
    return response.choices[0].message.content    
    
    
# CRIAR A INTERFACE
def main():
    st.title("Busca PC")
    # Incluir uma imagem de acordo ao sistema escolhido
    with st.sidebar:
        st.header("UPLoader Files")
        uploader = st.file_uploader("Adicione arquivos", type="pdf", accept_multiple_files=True)
    if uploader:
        text = extract_files(uploader)
        st.session_state["document-text"] = text
    user_input = st.text_input("Digite a sua pergunta")
    if user_input and "document_text" in st.session_state:
        response = chat_with_groq(user_input, st.session_state["document_text"])
        st.write("Resposta:", response)

if __name__ == "__main__":
     main()