import glob
import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_unstructured import UnstructuredLoader
import logging

# ==========================================
# 1. Configuração da API e Inicialização
# ==========================================
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".csv", ".docx", ".doc"}
recuperador_global = None
agente_global = None


def carregar_documentos(arquivos):
    documentos = []

    for arquivo in arquivos:
        caminho = Path(arquivo)
        if not caminho.exists() or not caminho.is_file():
            continue

        extensao = caminho.suffix.lower()
        print(f"   Lendo o arquivo: {caminho}")

        if extensao == ".pdf":
            carregador = UnstructuredLoader(str(caminho), languages=["pt"])
            documentos.extend(carregador.load())
        elif extensao == ".txt":
            texto = caminho.read_text(encoding="utf-8", errors="ignore")
            documentos.append(
                Document(page_content=texto, metadata={"source": str(caminho), "file_type": "txt"})
            )
        elif extensao == ".csv":
            texto = caminho.read_text(encoding="utf-8", errors="ignore")
            documentos.append(
                Document(page_content=texto, metadata={"source": str(caminho), "file_type": "csv"})
            )
        elif extensao in {".docx", ".doc"}:
            try:
                from docx import Document as DocxDocument
            except ImportError as exc:
                raise ImportError("Para ler arquivos Word, instale python-docx no ambiente.") from exc

            doc = DocxDocument(str(caminho))
            texto = "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip())
            documentos.append(
                Document(page_content=texto, metadata={"source": str(caminho), "file_type": "docx"})
            )

    return documentos


def listar_arquivos_documentos(pasta="documentos"):
    if not os.path.isdir(pasta):
        return []

    arquivos = []
    for item in glob.glob(os.path.join(pasta, "*")):
        caminho = Path(item)
        if caminho.is_file() and caminho.suffix.lower() in SUPPORTED_EXTENSIONS:
            arquivos.append(str(caminho))

    return sorted(arquivos)


def inicializar_base_conhecimento():
    print("1. Carregando os documentos da base de conhecimento...")

    arquivos = listar_arquivos_documentos()
    if not arquivos:
        raise ValueError("Nenhum documento suportado encontrado na pasta 'documentos'.")

    documentos = carregar_documentos(arquivos)
    if not documentos:
        raise ValueError("Não foi possível extrair texto dos documentos encontrados.")

    print("2. Fatiando o texto em pequenos pedaços (Chunks)...")
    divisor_texto = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    pedacos = divisor_texto.split_documents(documentos)
    pedacos = filter_complex_metadata(pedacos)

    print("3. Criando Embeddings e salvando no Banco de Dados Vetorial (Chroma)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    banco_vetorial = Chroma.from_documents(documents=pedacos, embedding=embeddings)

    recuperador = banco_vetorial.as_retriever(search_kwargs={"k": 3})
    return recuperador


def configurar_agente(recuperador):
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise RuntimeError("Defina GOOGLE_API_KEY no arquivo .env ou nas variáveis de ambiente do sistema.")

    os.environ["GOOGLE_API_KEY"] = google_api_key

    print("4. Configurando o cérebro do Agente (LLM + Prompt)...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

    prompt_sistema = (
        "Você é o assistente virtual de atendimento da loja online 'BimBam Buy'.\n"
        "Use APENAS os pedaços de contexto recuperados abaixo para responder à pergunta.\n"
        "Se a resposta não estiver no contexto, diga amigavelmente que não encontrou "
        "essa informação nas políticas da loja e oriente a contatar o suporte.\n"
        "Responda de forma clara, educada e direta.\n\n"
        "CONTEXTO RECUPERADO:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_sistema),
        ("human", "{input}"),
    ])

    class AgenteRAG:
        def __init__(self, recuperador, llm, prompt):
            self.recuperador = recuperador
            self.llm = llm
            self.prompt = prompt

        def invoke(self, payload):
            pergunta = payload["input"]
            documentos_recuperados = self.recuperador.invoke(pergunta)
            contexto = "\n\n".join(doc.page_content for doc in documentos_recuperados)

            mensagens = self.prompt.format_messages(input=pergunta, context=contexto)
            resposta = self.llm.invoke(mensagens)
            return {"answer": resposta.content}

    return AgenteRAG(recuperador, llm, prompt)


def get_agente():
    global recuperador_global, agente_global

    if agente_global is None:
        print("-" * 50)
        print("Iniciando o sistema RAG da BimBam Buy...")
        recuperador_global = inicializar_base_conhecimento()
        agente_global = configurar_agente(recuperador_global)
        print("Pronto! O Agente Inteligente está online.")
        print("-" * 50)

    return agente_global


# ==========================================
# 2. Configuração do Flask (Rotas Web)
# ==========================================
app = Flask(__name__)

# Configura o arquivo onde as mensagens serão salvas
logging.basicConfig(
    filename='historico_chat.log', # Nome do arquivo que será criado
    level=logging.INFO,
    format='%(asctime)s - %(message)s', # Formato: Data/Hora - Mensagem
    datefmt='%Y-%m-%d %H:%M:%S'
)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    dados = request.get_json()
    pergunta_usuario = dados.get('mensagem')

    if not pergunta_usuario:
        return jsonify({"erro": "Nenhuma mensagem fornecida"}), 400

    try:
        agente = get_agente()
        resposta_agente = agente.invoke({"input": pergunta_usuario})
        resposta_texto = resposta_agente["answer"]
        
        # SALVANDO NO ARQUIVO DE LOG AQUI:
        logging.info(f"PERGUNTA: {pergunta_usuario}")
        logging.info(f"RESPOSTA: {resposta_texto}\n{'-'*30}")
        
        return jsonify({"resposta": resposta_texto})
        
    except Exception as e:
        # É uma boa prática salvar os erros no log também
        logging.error(f"ERRO: {str(e)}")
        return jsonify({"erro": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)