# 📝 Formato do Arquivo de Conversa

## Visão Geral

O arquivo de conversa (`{chat_name}_conversation.txt`) contém todas as mensagens do grupo/canal em formato cronológico, incluindo texto, mídia e mensagens de serviço.

## Estrutura do Arquivo

### Cabeçalho
```
════════════════════════════════════════════════════════════════════════════════════════════════════
════════════════════════════════════════════════════════════════════════════════════════════════════
                    CONVERSA: Nome do Grupo/Canal
════════════════════════════════════════════════════════════════════════════════════════════════════
════════════════════════════════════════════════════════════════════════════════════════════════════

```

### Formato das Mensagens

#### Mensagens de Texto
```
[2025-01-18 14:30:22] @usuario123 (ID: 123456789):
Olá, pessoal! Como vocês estão?

────────────────────────────────────────────────────────────────────────────────────────────────────

```

#### Mensagens de Mídia
```
[2025-01-18 14:32:00] João Silva (ID: 987654321): [imagem enviada: 20250118_143200_photo.jpg]

────────────────────────────────────────────────────────────────────────────────────────────────────

```

#### Mensagens de Serviço
```
[2025-01-18 14:31:15] 👋 Alguém entrou no grupo via link de convite

────────────────────────────────────────────────────────────────────────────────────────────────────

[2025-01-18 14:35:20] 👋 João Silva foi adicionado ao grupo

────────────────────────────────────────────────────────────────────────────────────────────────────

[2025-01-18 15:10:30] 📝 Título do grupo alterado para: Grupo de Desenvolvimento v2

────────────────────────────────────────────────────────────────────────────────────────────────────

[2025-01-18 15:15:45] 📌 Uma mensagem foi fixada

────────────────────────────────────────────────────────────────────────────────────────────────────

[2025-01-18 16:20:00] 👋 Maria saiu do grupo

────────────────────────────────────────────────────────────────────────────────────────────────────

```

## Características

### ✅ **Formatação Melhorada**
- **Separadores visuais**: Linhas de separação mais largas (100 caracteres)
- **Espaçamento**: Linhas em branco entre mensagens
- **Cabeçalho destacado**: Bordas duplas para o título
- **Legibilidade**: Formato mais fácil de ler

### ✅ **Tipos de Mensagem Suportados**
1. **Texto**: Mensagens de texto com remetente e timestamp
2. **Mídia**: Referência ao arquivo baixado (imagem, vídeo, documento, etc.)
3. **Serviço**: Entradas, saídas, mudanças de grupo

### ✅ **Identificação de Usuários**
- **Username**: `@usuario123 (ID: 123456789)`
- **Nome completo**: `João Silva (ID: 987654321)`
- **Nome simples**: `Maria (ID: 555666777)`
- **Fallback**: `User_123456789`

### ✅ **Organização Cronológica**
- Todas as mensagens em ordem temporal
- Timestamp completo (data e hora)
- Fácil navegação e busca

## Exemplo Completo

```
════════════════════════════════════════════════════════════════════════════════════════════════════
════════════════════════════════════════════════════════════════════════════════════════════════════
                    CONVERSA: Grupo de Desenvolvimento
════════════════════════════════════════════════════════════════════════════════════════════════════
════════════════════════════════════════════════════════════════════════════════════════════════════

[2025-01-18 14:30:22] @dev_lead (ID: 123456789):
Bom dia, pessoal! Vamos começar a reunião de hoje?

────────────────────────────────────────────────────────────────────────────────────────────────────

[2025-01-18 14:31:15] 👋 Alguém entrou no grupo via link de convite

────────────────────────────────────────────────────────────────────────────────────────────────────

[2025-01-18 14:32:00] João Dev (ID: 987654321): [imagem enviada: 20250118_143200_diagrama.png]

────────────────────────────────────────────────────────────────────────────────────────────────────

[2025-01-18 14:33:45] @dev_lead (ID: 123456789):
Perfeito! Vamos analisar esse diagrama juntos.

────────────────────────────────────────────────────────────────────────────────────────────────────

[2025-01-18 14:35:10] Ana Tech (ID: 555666777): [documento enviado: 20250118_143510_relatorio.pdf]

────────────────────────────────────────────────────────────────────────────────────────────────────

[2025-01-18 14:36:00] @dev_lead (ID: 123456789):
Excelente trabalho, Ana! Vamos revisar esse relatório.

────────────────────────────────────────────────────────────────────────────────────────────────────

[2025-01-18 15:10:30] 📝 Título do grupo alterado para: Grupo de Desenvolvimento v2

────────────────────────────────────────────────────────────────────────────────────────────────────

[2025-01-18 15:15:45] 📌 Uma mensagem foi fixada

────────────────────────────────────────────────────────────────────────────────────────────────────

[2025-01-18 16:20:00] 👋 Maria saiu do grupo

────────────────────────────────────────────────────────────────────────────────────────────────────

```

## Vantagens do Novo Formato

### 📖 **Legibilidade**
- Separadores visuais claros
- Espaçamento adequado entre mensagens
- Formato consistente e profissional

### 🔍 **Navegação**
- Fácil localização de mensagens específicas
- Timestamps claros e organizados
- Identificação rápida de tipos de mensagem

### 💾 **Organização**
- Arquivo único por grupo/canal
- Ordem cronológica preservada
- Contexto completo da conversa

### 📱 **Compatibilidade**
- Encoding UTF-8 para caracteres especiais
- Formato de texto simples
- Compatível com qualquer editor de texto 