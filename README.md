# BimBam Buy - Assistente RAG com Base de Conhecimento

Este projeto implementa um assistente inteligente baseado em Recuperação-Augmentada de Geração (RAG), com interface web em Flask e processamento de documentos em PDF para responder perguntas com base em contexto.

## 1. Preparação e configuração
Estrutura do repositório com pastas e arquivos para facilitar o desenvolvimento, manutenção e implantação:

```text
bimbam-buy/
├── app.py
├── requirements.txt
├── .env
├── documentos/
│   └── *.pdf
├── templates/
│   └── index.html
└── README.md
```

### Requisitos
- Python 3.10+
- Ambiente virtual configurado
- Chave de API do Google Gemini configurada em `.env`

### Instalação
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Variáveis de ambiente
Crie um arquivo `.env` com:

```env
GOOGLE_API_KEY=sua_chave_aqui
```

---

## 2. Coleta e curadoria
Com base nos documentos disponíveis na base de conhecimento:

- Atendimento e suporte: FAQ, reembolsos e devoluções
- Pós-venda e garantia: políticas de garantia, prazos e custos
- Parcerias e relacionamento: programa de afiliados

### Boas práticas
- Documentos centralizados na pasta `documentos/`
- Valida formato, autoria e relevância de cada material
- Curadoria periódica para remover versões antigas ou duplicadas

---

## 3. Processamento e extração
O fluxo de ingestão processa arquivos de diferentes formatos antes de incorporar os dados ao pipeline RAG:

- PDF
- Word (.docx/.doc)
- CSV
- TXT

### Fluxo 
- Extração de texto dos documentos
- Limpeza de caracteres especiais e ruídos
- Padronização de estrutura e linguagem
- Conversão para um formato homogêneo para processamento posterior

---

## 4. Indexação vetorial
Este projeto utiliza uma pipeline de indexação baseada em embeddings para a base de conhecimento carregada a partir de PDFs.

---

## 5. Recuperação e RAG
A recuperação é feita por meio de um fluxo RAG com os seguintes passos implementados no código:

- Buscar os trechos semanticamente mais semelhantes para a pergunta do usuário
- Recuperar um conjunto limitado de chunks para compor o contexto do modelo
- Enviar esses trechos ao prompt do LLM para gerar a resposta

### Limitações atuais
O projeto ainda não implementa, no estado atual, as etapas abaixo:
- reranking explícito dos resultados (não implementado)
- filtragem por metadados como `departamento` ou `data` (não implementado)

### Estratégia prevista para evolução
1. Recuperar os trechos mais relevantes para a pergunta do usuário
2. Aplicar reranking para priorizar os fragmentos com maior valor semântico
3. Filtrar por metadados, quando os documentos passarem a incluir estrutura informacional
4. Combinar os trechos selecionados no prompt do modelo
5. Gerar respostas com base apenas no contexto recuperado

---

## 6. Geração, validação e interface
O LLM responde somente com base no contexto recuperado.

### Diretrizes de resposta
- Responder apenas com informações presentes no contexto
- Evitar alucinações ou inferências não suportadas
- Ser claro, objetivo e educado
- Se a resposta não existir, indicar que não foi encontrado o conteúdo nas fontes disponíveis

### Interface
A aplicação possui uma interface web simples em Flask, acessível via navegador, permitindo:
- envio de perguntas pelo usuário
- processamento pelo agente RAG
- retorno da resposta em tempo real

---

## 7. Deploy na OCI (não implementado)
Para implantação na Oracle Cloud Infrastructure (OCI), recomenda-se:

- Containerizar a aplicação com Docker
- Publicar a imagem em um registro de container da OCI
- Subir o serviço em uma infraestrutura compatível com aplicações web
- Configurar variáveis de ambiente seguras e persistentes

### Exemplo de containerização
```bash
docker build -t bimbam-buy .
docker run -p 5000:5000 --env-file .env bimbam-buy
```

---

## 8. Manutenção e monitoramento (não implementado)

Registre queries, contexto e respostas para auditoria e melhoria contínua.

### Recomendações
- Armazenar logs de perguntas e respostas
- Registrar métricas de recuperação e qualidade das respostas
- Monitorar falhas, latência e erros de execução
- Integrar logs com serviços de observabilidade da OCI, como Logging

---

## Como executar

```bash
python app.py
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000/
```

---

## Resumo do projeto

Este repositório apresenta uma solução inicial de assistente RAG para organização e consulta de conhecimento, com foco em:
- ingestão de documentos em diferentes formatos
- extração e normalização de conteúdo
- indexação vetorial com embeddings
- recuperação semântica de trechos relevantes
- geração de respostas com base no contexto recuperado
- interface web simples para interação com o usuário
