import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("GOOGLE_API_KEY", "test")

import app


class TestIngestao(unittest.TestCase):
    def test_carregar_documentos_txt_e_csv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            txt_path = Path(tmpdir) / "politica.txt"
            csv_path = Path(tmpdir) / "custos.csv"

            txt_path.write_text("Política de reembolso para clientes.", encoding="utf-8")
            csv_path.write_text("produto,valor\ncamisa,50\n", encoding="utf-8")

            documentos = app.carregar_documentos([txt_path, csv_path])

            textos = [doc.page_content for doc in documentos]
            self.assertTrue(any("reembolso" in texto.lower() for texto in textos))
            self.assertTrue(any("camisa" in texto.lower() for texto in textos))

    def test_resposta_local_encontra_formas_de_pagamento(self):
        documento = app.Document(
            page_content="Métodos Aceitos: cartões de crédito e débito, transferência bancária (PIX), boletos e carteiras digitais.",
            metadata={"source": "politicas.txt", "file_type": "txt"},
        )
        recuperador = app.RecuperadorLocal([documento])
        agente = app.configurar_agente(recuperador)

        resposta = agente.invoke({"input": "quais são as formas de pagamento aceitas?"})

        texto_resposta = resposta["answer"].lower()
        self.assertTrue("cartões" in texto_resposta or "pix" in texto_resposta)

    def test_configurar_agente_usa_openai_quando_chave_for_fornecida(self):
        class FakeChatOpenAI:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

            def invoke(self, messages):
                return type("Response", (), {"content": "resposta openai"})()

        fake_module = types.SimpleNamespace(ChatOpenAI=FakeChatOpenAI)

        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "fake-key"}, clear=False):
            with mock.patch.dict(sys.modules, {"langchain_openai": fake_module}):
                agente = app.configurar_agente(app.RecuperadorLocal([app.Document(page_content="contexto", metadata={})]))
                resposta = agente.invoke({"input": "pergunta"})

        self.assertEqual(resposta["answer"], "resposta openai")


if __name__ == "__main__":
    unittest.main()
