# Conectar o relógio Garmin

Scripts usando o [cliente Python oficial da Garmin](https://github.com/garmin/connect-personal-api-python)
pra acessar seus próprios dados de saúde/treino do Garmin Connect com uma
**chave de API pessoal** — sem senha, sem autenticação em duas etapas, sem
bloqueio por bot (esse era o jeito antigo, não-oficial, que usávamos antes e
que dava bastante dor de cabeça com rate limit).

**Importante sobre o que isso faz:** fala com a nuvem do Garmin Connect (a
mesma conta usada pelo app Garmin Connect no celular), não faz pareamento
direto via USB/Bluetooth com o relógio. Seu relógio já precisa estar
sincronizado com sua conta Garmin Connect (pelo app no celular) pra os
dados aparecerem aqui.

## Requisitos

- **Python 3.12 ou mais recente** (o pacote oficial exige isso)
- Uma conta Garmin Connect

## 1. Gerar sua chave de API pessoal

No site/app do Garmin Connect: **Configurações → Chave de API pessoal**
(ou direto em https://connect.garmin.com/app/settings/personalApiToken).

- Escolha a validade (30 dias a 1 ano)
- A chave só aparece **uma vez** — copie e guarde num lugar seguro
- A Garmin avisa por e-mail cerca de uma semana antes de expirar
- Se precisar gerar uma nova, tem que excluir a antiga primeiro (ela para de funcionar na hora)

## 2. Instalação

```bash
cd garmin-connect
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Testar a conexão (`connect.py`)

Rode no **seu terminal, na sua máquina** (não em um chat):

```bash
python3 connect.py
```

Ele pede a chave ali mesmo no terminal (`getpass`, não aparece na tela e
não é enviada a mais ninguém além dos servidores do Garmin). Pra não
digitar toda vez, exporte antes:

```bash
export GARMIN_PERSONAL_API_KEY="sua-chave-aqui"
```

(evite deixar isso num arquivo de histórico de shell persistente sem
necessidade.)

## Baixar todos os seus dados (`export_data.py`)

```bash
python3 export_data.py
```

Isso baixa e salva em arquivos `.json` dentro de `garmin-connect/data/`
(pasta ignorada pelo git — seus dados de saúde nunca vão pro repositório):

- `data/profile.json` — configurações de perfil, zonas de frequência cardíaca
- `data/trends.json` — tendências de passos, sono, HRV, body battery, estresse, hidratação, peso, atividades de bem-estar
- `data/daily/AAAA-MM-DD.json` — um arquivo por dia com frequência cardíaca, sono, HRV, SpO2 e idade de aptidão física (métricas que só têm endpoint de um dia por vez)
- `data/activities.json` — lista de atividades
- `data/activities/<id>.json` — detalhe e treinos de cada atividade

Por padrão pega **os últimos 7 dias** e **até 20 atividades**. Pode pedir mais:

```bash
python3 export_data.py --days 30 --activities-limit 100
```

Para baixar também o arquivo original de cada atividade (.zip com o FIT):

```bash
python3 export_data.py --download-files
```

## Uso em rotina automática (`daily_snapshot.py`)

`connect.py` e `export_data.py` são feitos pra rodar com você digitando a
chave no seu terminal. Uma rotina agendada (ex: um briefing diário) roda
sozinha, sem ninguém pra digitar nada — então `daily_snapshot.py` lê a
chave da variável de ambiente `GARMIN_PERSONAL_API_KEY` em vez de pedir
interativamente.

**Nunca digite a chave no chat.** Cadastre `GARMIN_PERSONAL_API_KEY` nas
configurações do seu ambiente Claude Code (fora deste repositório e fora
de qualquer conversa) — o script só lê essa variável do ambiente onde ele
roda.

```bash
GARMIN_PERSONAL_API_KEY=... python3 daily_snapshot.py
```

Ele imprime um JSON com frequência cardíaca, sono, estresse, body
battery, HRV e idade de aptidão física de hoje. Se a chave estiver
ausente, expirada ou revogada, ele só imprime o motivo em stderr e sai —
não trava esperando alguém digitar algo.

## Domínio de rede (ambientes de nuvem / rotinas)

Se estiver rodando num ambiente de nuvem com acesso à rede restrito
("Custom"/"Personalizado"), libere este domínio:

```
personal.connectapi.garmin.com
```

É o único host usado pela API pessoal — tanto pra trocar a chave por um
token quanto pra buscar os dados.
