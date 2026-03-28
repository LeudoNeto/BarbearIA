"""
Configuração de Preview de Corte - Centraliza parâmetros de geração e publicação.
"""
import os


class PreviewConfig:
    """Classe para gerenciar a configuração de previews de corte."""

    def __init__(self):
        self.backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.preview_base_url = os.getenv("PREVIEW_BASE_URL", "http://localhost:8081").rstrip("/")
        self.preview_static_dir = os.path.join(self.backend_root, "static", "previews")
        self.preview_default_filename = "preview_corte_default.png"
        self.preview_default_path = os.path.join(self.preview_static_dir, self.preview_default_filename)
        self.preview_default_legacy_path = os.path.join(self.backend_root, self.preview_default_filename)
        self.openai_api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAPI_API_KEY")


# Instância singleton
preview_config = PreviewConfig()
