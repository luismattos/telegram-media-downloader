# Scripts do Telegram Media Downloader

Este diretório contém os scripts principais para usar o Telegram Media Downloader.

## Scripts Disponíveis

### `app.py` ⭐ **SCRIPT CENTRAL**
Script central que é o ponto de entrada real do aplicativo.
- Contém toda a lógica de inicialização
- Tratamento de erros centralizado
- Configuração de paths
- Importado pelos scripts `run.py` e `main.py` da raiz

**Uso:**
```bash
python3 scripts/app.py
```

### `telegram_interactive.py`
Script interativo principal para baixar mídia de grupos e canais do Telegram.
- Interface amigável com menu de opções
- Sistema de loop para baixar múltiplos grupos
- Configuração de opções de download
- Organização por subdiretórios

**Uso:**
```bash
python3 scripts/telegram_interactive.py
```

### `list_chats.py`
Lista todos os chats disponíveis (grupos, canais e usuários) separados por categorias.
- Mostra grupos normais e supergrupos
- Mostra canais de transmissão
- Mostra usuários/contatos
- Salva lista em JSON

**Uso:**
```bash
python3 scripts/list_chats.py
```

### `telegram_media_downloader.py`
Script de linha de comando para download direto.
- Uso via argumentos de linha de comando
- Menos interativo que o telegram_interactive.py

**Uso:**
```bash
python3 scripts/telegram_media_downloader.py "Nome do Grupo"
```

### `debug_chats.py`
Script de debug para análise detalhada de todos os chats.
- Mostra informações técnicas de cada chat
- Útil para desenvolvimento e troubleshooting
- Salva debug em JSON

**Uso:**
```bash
python3 scripts/debug_chats.py
```

## Como Usar

### **Recomendado - Scripts da Raiz:**
```bash
# Da raiz do projeto
python3 run.py
python3 main.py
```

### **Scripts Específicos:**
```bash
# Script central
python3 scripts/app.py

# Scripts específicos
python3 scripts/telegram_interactive.py
python3 scripts/list_chats.py
```

1. Certifique-se de que as credenciais da API estão configuradas no arquivo `.env`
2. Execute o script desejado
3. Siga as instruções na tela

## Estrutura de Downloads

Os downloads são organizados da seguinte forma:
```
downloads/
├── Nome do Grupo/
│   ├── download_history.json
│   ├── 20250618/
│   │   ├── arquivos_baixados.jpg
│   │   └── mensagens.txt
│   └── 20250619/
│       └── ...
└── Outro Grupo/
    └── ...
``` 