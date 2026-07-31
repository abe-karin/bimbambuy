# BimBam Buy

BimBam Buy é um assistente inteligente em Flask para responder perguntas com base em documentos da loja, usando uma abordagem RAG (Retrieval-Augmented Generation). A aplicação lê arquivos da pasta documentos, extrai texto e tenta responder com contexto relevante, seja usando modelos externos como Gemini ou OpenAI, ou com um fallback local quando as chaves não estão disponíveis.

## O que a aplicação faz

- Lê arquivos de texto e documentos em diferentes formatos:
  - PDF
  - TXT
  - CSV
  - DOCX / DOC
- Carrega esses arquivos na base de conhecimento do projeto.
- Recupera trechos relevantes para a pergunta do usuário.
- Gera respostas com base no contexto recuperado.
- Expõe uma interface web simples para interação.

## Estrutura do projeto

```text
bimbambuy/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── documentos/
├── tests/
├── README.md
└── .env
```

## Requisitos

- Python 3.10 ou superior
- Ambiente virtual recomendado
- Uma chave de API do Google Gemini ou OpenAI, opcionalmente

## Configuração do ambiente

### 1. Criar e ativar o ambiente virtual

No Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependências

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se o comando de instalação falhar por problema com o launcher do pip no Windows, use:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Crie um arquivo chamado .env na raiz do projeto com uma das opções abaixo:

```env
GOOGLE_API_KEY=sua_chave_aqui
```

ou

```env
OPENAI_API_KEY=sua_chave_aqui
```

## Colocar documentos na base de conhecimento

Adicione os arquivos que devem servir como fonte de resposta na pasta documentos/.

Exemplos aceitos:
- arquivos .txt
- arquivos .csv
- arquivos .pdf
- arquivos .docx / .doc

## Executar a aplicação

```bash
python app.py
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000/
```

## Testes

Os testes automatizados podem ser executados com:

```bash
python -m unittest discover -s tests -v
```

## Observações importantes

- Se não houver documentos na pasta documentos/, a aplicação não conseguirá montar a base de conhecimento.
- Se nenhuma chave de API estiver configurada, o projeto usa um modo local de fallback para responder com base no contexto disponível.
- As interações do chat são registradas em um arquivo chamado historico_chat.log.

## Próximos passos possíveis

- Melhorar a recuperação semântica com reranking.
- Adicionar filtros por metadados e data.
- Implementar autenticação e painel admin.
- Preparar a aplicação para deploy em ambiente de produção.
