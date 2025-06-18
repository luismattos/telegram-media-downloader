# Telegram Media Downloader

Um downloader de mídia e mensagens para Telegram com suporte a downloads incrementais, organização por data e histórico detalhado.

## 🚀 Roadmap do Projeto

Este projeto está em constante evolução! Consulte o **[ROADMAP.md](ROADMAP.md)** para ver o plano completo de desenvolvimento, incluindo:

- **Fase 1**: ✅ Refatoração e estrutura profissional (CONCLUÍDA)
- **Fase 2**: Funcionalidades avançadas (filtros, download em lote)
- **Fase 3**: Interface web e melhorias de UX
- **Fase 4**: Infraestrutura e deploy
- **Fase 5**: Funcionalidades enterprise
- **Fase 6**: Comunidade e distribuição

**Status atual**: ✅ **Fase 1 Concluída** - Projeto refatorado com estrutura modular profissional.

## 🏗️ Nova Estrutura do Projeto

O projeto foi refatorado com uma estrutura modular profissional:

```
telegram-media-downloader/
├── telegram_media_downloader/          # Pacote principal
│   ├── __init__.py                     # Configuração do pacote
│   ├── core/                           # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── downloader.py               # Downloader principal
│   │   ├── chat_lister.py              # Listador de chats
│   │   └── interactive.py              # Modo interativo
│   ├── models/                         # Modelos de dados
│   │   ├── __init__.py
│   │   ├── chat.py                     # Modelo de chat
│   │   └── message.py                  # Modelo de mensagem
│   └── utils/                          # Utilitários
│       ├── __init__.py
│       ├── config.py                   # Sistema de configuração
│       ├── logging.py                  # Sistema de logging
│       └── validators.py               # Sistema de validações
├── scripts/                            # Scripts de entrada
│   ├── telegram_media_downloader.py    # Entrypoint do downloader
│   ├── list_chats.py                   # Entrypoint do listador
│   └── telegram_interactive.py         # Entrypoint interativo
├── tests/                              # Testes automatizados
│   ├── test_structure.py               # Testes da estrutura
│   └── test_core_modules.py            # Testes dos módulos core
├── docs/                               # Documentação
├── logs/                               # Logs do sistema
├── downloads/                          # Arquivos baixados
├── setup.py                            # Configuração do pacote
├── requirements.txt                    # Dependências
└── README.md                           # Este arquivo
```

## Características

- **Estrutura Modular**: Código organizado em módulos reutilizáveis
- **Sistema de Logging Unificado**: Logs centralizados com diferentes níveis
- **Configuração Centralizada**: Sistema de configuração via variáveis de ambiente
- **Modelos de Dados**: Classes estruturadas para chats e mensagens
- **Validações Robustas**: Sistema de validação de entradas
- Download de diferentes tipos de mídia:
  - Fotos
  - Vídeos
  - Documentos
  - Páginas web com mídia
- Download de mensagens de texto
- Organização dos arquivos por data
- Histórico de downloads para evitar duplicatas
- **Interface interativa** para configuração e uso
- Interface simples via linha de comando
- Suporte a downloads incrementais (apenas novos arquivos)
- **Sistema de logs robusto** com arquivos de log detalhados
- Logs em tempo real no console e salvos em arquivos
- **Listagem de chats salva em arquivo JSON** para referência
- **Diretório de download configurável** via variáveis de ambiente

## Requisitos

- Python 3.8 ou superior
- Conta no Telegram
- Credenciais da API do Telegram (api_id e api_hash)

## Configuração da API do Telegram

1. Acesse https://my.telegram.org/auth
2. Faça login com seu número de telefone do Telegram
3. Clique em "API development tools"
4. Preencha o formulário:
   - App title: Nome do seu aplicativo (ex: "Meu Downloader")
   - Short name: Nome curto (ex: "downloader")
   - Platform: Desktop
   - Description: Descrição do app (ex: "Downloader de mídia e mensagens")
5. Clique em "Create application"
6. Anote o `api_id` (número) e `api_hash` (string)
7. Configure as variáveis de ambiente:

### Método Automático (Recomendado)
O script `setup.sh` criará automaticamente o arquivo `.env` com template.

### Método Manual
Copie o arquivo de exemplo e configure suas credenciais:

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas credenciais reais
# Para Fish shell:
set -x TELEGRAM_API_ID seu_api_id
set -x TELEGRAM_API_HASH seu_api_hash

# Para Bash/Zsh:
TELEGRAM_API_ID=seu_api_id
TELEGRAM_API_HASH=seu_api_hash
```

### Configuração do Diretório de Download

Você pode configurar onde os arquivos serão salvos usando a variável `TELEGRAM_DOWNLOAD_PATH`:

```bash
# Para Fish shell:
set -x TELEGRAM_DOWNLOAD_PATH ~/Downloads/telegram

# Para Bash/Zsh:
TELEGRAM_DOWNLOAD_PATH=~/Downloads/telegram
```

#### Exemplos de Diretórios:
- `~/Downloads/telegram` - Pasta Downloads do usuário
- `~/Documents/telegram_downloads` - Pasta Documents
- `/Users/username/telegram_media` - Caminho absoluto
- Deixe vazio para usar o diretório padrão (`./downloads`)

#### Comportamento:
- Se a variável não estiver definida: usa `./downloads` (dentro do projeto)
- Se definida: usa o diretório especificado
- O diretório será criado automaticamente se não existir
- Suporta expansão de `~` para o diretório home

## Configuração do Ambiente Virtual

### Método Automático (Recomendado)

O projeto inclui um script de configuração universal que funciona em qualquer shell:

```bash
# Funciona em Fish shell, Bash e Zsh
source setup.sh
```

O script detecta automaticamente qual shell você está usando e:
- Cria um ambiente virtual Python (`.venv`)
- Ativa o ambiente virtual
- Instala as dependências automaticamente
- Cria o arquivo `.env` com template apropriado para seu shell

### Método Manual

Se preferir configurar manualmente:

```bash
# 1. Criar ambiente virtual
python3 -m venv .venv

# 2. Ativar o ambiente virtual
# Para Fish shell:
source .venv/bin/activate.fish

# Para Bash/Zsh:
source .venv/bin/activate

# 3. Atualizar pip
python3 -m pip install --upgrade pip

# 4. Instalar dependências
pip install -r requirements.txt
```

## Instalação das Dependências

As principais dependências são:

- **Telethon**: Biblioteca Python para a API do Telegram
- **python-dotenv**: Para carregar variáveis de ambiente do arquivo `.env`

### Instalação Manual do Telethon

Se precisar instalar apenas o Telethon:

```bash
# Com o ambiente virtual ativado
pip install telethon>=1.28.5
pip install python-dotenv>=1.0.0
```

### Verificação da Instalação

Para verificar se tudo foi instalado corretamente:

```bash
# Verificar se o Telethon está instalado
python3 -c "import telethon; print('✅ Telethon instalado:', telethon.__version__)"

# Verificar se o python-dotenv está instalado
python3 -c "import dotenv; print('✅ python-dotenv instalado')"
```

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd [NOME_DO_DIRETÓRIO]
```

2. Configure o ambiente virtual:
```bash
# Script universal que funciona em qualquer shell
source setup.sh
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

### 🚀 Método Interativo (Recomendado)

O script interativo guia você através de todo o processo de configuração e download:

```bash
# Ative o ambiente virtual
source .venv/bin/activate.fish  # Fish shell
# ou
source .venv/bin/activate       # Bash/Zsh

# Execute o modo interativo
python telegram_interactive.py
```

O modo interativo irá:
1. ✅ Verificar/criar credenciais da API
2. ✅ Configurar diretório de download
3. ✅ Listar grupos e canais disponíveis
4. ✅ Permitir seleção do grupo/canal
5. ✅ Configurar opções de download
6. ✅ Iniciar o download automaticamente

### 📋 Listar Chats Disponíveis

Para ver todos os grupos e canais disponíveis:

```bash
# Ative o ambiente virtual
source .venv/bin/activate.fish  # Fish shell
# ou
source .venv/bin/activate       # Bash/Zsh

# Liste os chats
python list_chats.py
```

### 📥 Download Direto

Para download direto via linha de comando:

```bash
# Ative o ambiente virtual
source .venv/bin/activate.fish  # Fish shell
# ou
source .venv/bin/activate       # Bash/Zsh

# Download com nome do chat como argumento
python telegram_media_downloader.py "Nome do Grupo/Canal"

# Ou sem argumento (será solicitado interativamente)
python telegram_media_downloader.py
```

### 🔧 Uso Programático

Com a nova estrutura modular, você pode usar o downloader programaticamente:

```python
import asyncio
from telegram_media_downloader.core.downloader import TelegramMediaDownloader

async def download_chat():
    downloader = TelegramMediaDownloader(
        api_id="seu_api_id",
        api_hash="seu_api_hash", 
        download_path="/caminho/para/downloads"
    )
    
    # Encontrar chat por título
    chat = await downloader.find_chat_by_title("Nome do Chat")
    
    # Download de mídia
    await downloader.download_media_from_chat(chat, limit=100)

# Executar
asyncio.run(download_chat())
```

## Estrutura dos Arquivos Baixados

Os arquivos são organizados por data:

```
downloads/
├── 20241201/                    # Data: 01/12/2024
│   ├── 20241201_143022_photo.jpg
│   ├── 20241201_143025_video.mp4
│   ├── 20241201_143030_message_123.txt
│   └── ...
├── 20241202/                    # Data: 02/12/2024
│   ├── 20241202_091500_document.pdf
│   └── ...
└── download_history.json        # Histórico de downloads
```

## Logs

O sistema gera logs detalhados:

- **Console**: Logs em tempo real durante a execução
- **Arquivos**: Logs salvos em `logs/` com timestamp
- **Níveis**: INFO, DEBUG, WARNING, ERROR
- **Formato**: Timestamp, nível, módulo, mensagem

### Exemplo de Log:
```
2024-12-01 14:30:22,123 - INFO - telegram_media_downloader.core.downloader - Starting download from Meu Grupo
2024-12-01 14:30:22,456 - INFO - telegram_media_downloader.core.downloader - Found 150 messages to process
2024-12-01 14:30:25,789 - INFO - telegram_media_downloader.core.downloader - Downloaded media: /path/to/file.jpg
```

## Testes

O projeto inclui testes automatizados para validar a estrutura:

```bash
# Testar estrutura modular
python tests/test_structure.py

# Testar módulos core
python tests/test_core_modules.py
```

## Desenvolvimento

### Estrutura de Desenvolvimento

```bash
# Instalar dependências de desenvolvimento
pip install -e ".[dev]"

# Executar testes
python -m pytest tests/

# Formatar código
black telegram_media_downloader/

# Verificar tipos
mypy telegram_media_downloader/
```

### Adicionando Novos Módulos

1. **Utilitários**: Adicione em `telegram_media_downloader/utils/`
2. **Modelos**: Adicione em `telegram_media_downloader/models/`
3. **Lógica de negócio**: Adicione em `telegram_media_downloader/core/`
4. **Testes**: Adicione em `tests/`

## Troubleshooting

### Problemas Comuns

1. **Erro de credenciais da API**:
   - Verifique se `TELEGRAM_API_ID` e `TELEGRAM_API_HASH` estão configurados
   - Certifique-se de que as credenciais são válidas

2. **Erro de conexão**:
   - Verifique sua conexão com a internet
   - Certifique-se de que o Telegram não está bloqueado

3. **Erro de permissão**:
   - Verifique se você é membro do grupo/canal
   - Certifique-se de que tem permissão para acessar o conteúdo

4. **Erro de importação**:
   - Ative o ambiente virtual: `source .venv/bin/activate`
   - Instale as dependências: `pip install -r requirements.txt`

### Logs de Debug

Para logs mais detalhados, modifique o nível de logging em `telegram_media_downloader/utils/logging.py`:

```python
logger.setLevel(logging.DEBUG)  # Para logs mais detalhados
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Status do Projeto

- ✅ **Fase 1 Concluída**: Refatoração e estrutura profissional
- 🔄 **Fase 2**: Funcionalidades avançadas (em desenvolvimento)
- ⏳ **Fase 3**: Interface web e melhorias de UX
- ⏳ **Fase 4**: Infraestrutura e deploy
- ⏳ **Fase 5**: Funcionalidades enterprise
- ⏳ **Fase 6**: Comunidade e distribuição

Consulte o [PROJECT_STATUS.md](PROJECT_STATUS.md) para detalhes sobre o status atual do projeto.

## 🚀 Como Executar

### Método 1: Script Principal (Recomendado)

```bash
# Executar o app interativo
python3 run.py

# Ou usando o script main.py
python3 main.py

# Ou executar diretamente (se tiver permissões)
./run.py
./main.py
```

### Método 2: Scripts Específicos

```bash
# Script interativo principal
python3 scripts/telegram_interactive.py

# Listar chats disponíveis
python3 scripts/list_chats.py

# Download direto (menos interativo)
python3 scripts/telegram_media_downloader.py "Nome do Grupo"

# Debug de chats (para desenvolvimento)
python3 scripts/debug_chats.py
```

### Método 3: Módulo Python

```bash
# Executar como módulo Python
python3 -m telegram_media_downloader.core.interactive
```

## 📖 Como Usar 