# BimBam Buy

O BimBam Buy é um assistente virtual em Flask para responder perguntas com base em documentos da loja. O projeto lê arquivos da pasta documentos, extrai texto e tenta responder com contexto relevante. Quando as variáveis de ambiente com chaves da OpenAI ou Gemini estão configuradas, a aplicação pode usar esses modelos; caso contrário, utiliza um fallback local simples.

## O que o projeto faz

- Expõe uma interface web simples para conversação.
- Recebe perguntas via endpoint HTTP e retorna respostas em JSON.
- Lê documentos em diferentes formatos:
  - TXT
  - CSV
  - PDF
  - DOCX
- Monta uma base de conhecimento a partir dos arquivos presentes na pasta documentos/.
- Registra as interações em um arquivo chamado historico_chat.log.
- Pode ser executado localmente, com Docker ou em uma instância OCI.

## Estrutura do projeto

```text
bimbambuy/
├── app.py
├── Dockerfile
├── requirements.txt
├── templates/
│   └── index.html
├── documentos/
├── prints/
├── tests/
├── README.md
└── .env (opcional)
```

## Requisitos

- Python 3.9 ou superior
- Ambiente virtual recomendado
- Docker (opcional, para execução em container)
- Chaves de API da OpenAI ou Google Gemini (opcional)

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

Se o comando falhar por problema com o launcher do pip no Windows, use:

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

Se nenhuma chave for configurada, a aplicação continua funcionando com o modo local de fallback.

## Adicionar documentos à base de conhecimento

Coloque os arquivos que devem servir como fonte de resposta na pasta documentos/.

Formatos aceitos:
- TXT
- CSV
- PDF
- DOCX

> Se a pasta documentos/ estiver vazia ou não houver arquivos suportados, a aplicação não conseguirá montar a base de conhecimento corretamente.

## Executar localmente

```bash
python app.py
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000/
```

A interface web está na rota principal e o chat é processado pela rota /chat.

## Executar com Docker

Construa a imagem:

```bash
docker build -t bimbambuy .
```

Execute o container:

```bash
docker run -p 5000:5000 --env-file .env bimbambuy
```

## Executando no OCI

O projeto também funciona no Oracle Cloud Infrastructure (OCI). Ele pode ser implantado em uma instância Linux com Docker, exposto na porta 5000 e acessado via navegador.

Fluxo de execução no OCI:

- Criar ou selecionar uma instância Compute no OCI.
- Instalar Docker na máquina.
- Fazer o build da imagem do projeto.
- Publicar o container na porta 5000.
- Acessar a interface pelo endereço público da instância.

Exemplos visuais da interface e do ambiente de execução:

![Tela da aplicação](prints/app.png)

![Tela da aplicação](prints/app2.png)

![Tela da aplicação](prints/app3.png)
(Se a pergunta não estiver de acordo com a documentação fornecida, o bot não responderá.)
![Ambiente OCI](prints/OCI.png)

## Testes

Os testes automatizados podem ser executados com:

```bash
python -m unittest discover -s tests -v
```

## Observações importantes

- O projeto utiliza Flask e o arquivo principal de execução é app.py.
- As respostas podem variar conforme os documentos presentes na pasta documentos/ e conforme o modo de resposta configurado.
- O arquivo historico_chat.log é gerado automaticamente durante o uso da aplicação.
