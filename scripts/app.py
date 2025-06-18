#!/usr/bin/env python3
"""
Telegram Media Downloader - Ponto de Entrada Central

Este é o script central que executa o Telegram Media Downloader.
"""

import sys
import os

# Adicionar o diretório do projeto ao path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def main():
    """Função principal que executa o app interativo"""
    try:
        # Importar e executar o script interativo
        from scripts.telegram_interactive import main_interactive
        main_interactive()
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("💡 Certifique-se de que todas as dependências estão instaladas:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Programa finalizado pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 