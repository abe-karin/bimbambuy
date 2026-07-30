import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("GOOGLE_API_KEY", "test")

import app


class TestIngestao(unittest.TestCase):
    def test_carregar_documentos_txt_e_csv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            txt_path = Path(tmpdir) / "politica.txt"
            csv_path = Path(tmpdir) / "custos.csv"

            txt_path.write_text("Política de reembolso para clientes.", encoding="utf-8")
            csv_path.write_text("produto;valor\ncamisa;50\n", encoding="utf-8")

            documentos = app.carregar_documentos([txt_path, csv_path])

            textos = [doc.page_content for doc in documentos]
            self.assertTrue(any("reembolso" in texto.lower() for texto in textos))
            self.assertTrue(any("camisa" in texto.lower() for texto in textos))


if __name__ == "__main__":
    unittest.main()
