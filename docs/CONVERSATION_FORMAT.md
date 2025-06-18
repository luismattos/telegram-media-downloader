# Formato de Conversa - Telegram Media Downloader

## Nova Organização de Mensagens

O sistema agora organiza as mensagens de texto em um único arquivo de conversa por grupo, similar ao fluxo do Telegram, em vez de arquivos separados para cada mensagem.

## Estrutura de Arquivos

### Antes (Formato Antigo)
```
downloads/
└── Lucky/
    ├── 20250618/
    │   ├── 20250617_233830_message_44.txt
    │   ├── 20250617_233831_message_45.txt
    │   ├── 20250617_233832_message_46.txt
    │   └── 20250617_233830_.jpg
    └── 20250619/
        ├── 20250618_100000_message_47.txt
        └── 20250618_100001_message_48.txt
```

### Agora (Novo Formato)
```
downloads/
└── Lucky/
    ├── Lucky_conversation.txt              # Todas as mensagens do grupo
    └── media/                              # Pasta com mídia organizada por data
        ├── 20250618/
        │   ├── 20250617_233830_.jpg
        │   └── 20250617_233831_.mp4
        └── 20250619/
            └── 20250618_100000_.pdf
```

## Formato do Arquivo de Conversa

### Exemplo: `Lucky_conversation.txt`

```
================================================================================
CONVERSA: Lucky
================================================================================

[2025-06-18 10:30:15] @joao_silva (ID: 123456789):
Olá pessoal! Como estão?

--------------------------------------------------------------------------------

[2025-06-18 10:32:45] Maria Santos (ID: 987654321):
Oi! Tudo bem aqui! 😊

--------------------------------------------------------------------------------

[2025-06-18 10:35:12] @joao_silva (ID: 123456789):
Que bom! Alguém tem novidades sobre o projeto?

--------------------------------------------------------------------------------

[2025-06-18 11:15:30] User_555666777:
Sim! Acabei de finalizar a primeira versão do downloader.

--------------------------------------------------------------------------------

[2025-06-19 09:45:20] @joao_silva (ID: 123456789):
Perfeito! Vamos testar?

--------------------------------------------------------------------------------
```

## Vantagens do Novo Formato

### ✅ **Conversa Completa**
- Todas as mensagens em um único arquivo
- Fluxo cronológico completo
- Fácil de ler do início ao fim

### ✅ **Identificação Inteligente**
- **Username:** `@joao_silva (ID: 123456789)` - quando disponível
- **Nome Completo:** `Maria Santos (ID: 987654321)` - quando não tem username
- **ID Apenas:** `User_555666777` - quando não consegue obter mais informações
- **Fallback:** `Unknown` - em casos extremos

### ✅ **Organização Simples**
- Um arquivo de texto por grupo
- Mídia organizada em pasta separada
- Estrutura limpa e intuitiva

### ✅ **Contexto Preservado**
- Conversa completa preservada
- Timestamps precisos
- Identificação detalhada dos usuários

### ✅ **Compatibilidade**
- Mídia organizada por data para evitar conflitos
- Histórico de downloads mantido
- Funcionalidade de skip preservada

## Detalhes Técnicos

### Formatação das Mensagens
- **Timestamp:** `[YYYY-MM-DD HH:MM:SS]`
- **Usuário:** Prioridade: `@username` > `Nome Completo` > `User_ID` > `Unknown`
- **Separador:** Linha de 80 hífens
- **Encoding:** UTF-8

### Identificação de Usuários
O sistema tenta obter informações do usuário na seguinte ordem:
1. **Username:** `@joao_silva (ID: 123456789)`
2. **Nome Completo:** `João Silva (ID: 123456789)`
3. **ID Apenas:** `User_123456789`
4. **Fallback:** `Unknown`

### Organização de Arquivos
- **Conversa:** `{nome_grupo}_conversation.txt` (único arquivo)
- **Mídia:** `media/YYYYMMDD/` (organizada por data)
- **Histórico:** `download_history.json` (por grupo)

### Tratamento de Mídia
- Arquivos de mídia em pasta `media/` separada
- Organizados por data para evitar conflitos de nome
- Nomeados com timestamp para unicidade

## Exemplo de Uso

```bash
# Executar download
python3 run.py

# Resultado: arquivo de conversa único
cat downloads/Lucky/Lucky_conversation.txt

# Ver mídia organizada
ls downloads/Lucky/media/
```

## Migração

O sistema é compatível com downloads anteriores:
- Arquivos antigos permanecem inalterados
- Novos downloads usam o formato de conversa única
- Histórico de downloads preservado 