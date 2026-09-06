# Conectar o relógio Garmin

Script simples usando [python-garminconnect](https://github.com/cyberjunky/python-garminconnect)
para conectar sua conta Garmin Connect a este computador.

**Importante sobre o que isso faz:** essa biblioteca fala com a nuvem do
Garmin Connect (a mesma conta usada pelo app Garmin Connect no celular),
não faz pareamento direto via USB/Bluetooth com o relógio. Ou seja, seu
relógio já precisa estar sincronizado com sua conta Garmin Connect (pelo
app no celular) para os dados aparecerem aqui.

## Requisitos

- Python 3.12 ou mais recente
- Uma conta Garmin Connect

## Instalação

```bash
cd garmin-connect
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

Rode no **seu terminal, na sua máquina** (não em um chat):

```bash
python3 connect.py
```

O script vai pedir seu e-mail e sua senha do Garmin Connect ali mesmo no
terminal. A senha é digitada com `getpass`, então não aparece na tela e
não é enviada a mais ninguém além dos servidores do Garmin. Se sua conta
tiver autenticação em duas etapas, ele também pede o código de
verificação.

Depois de logar com sucesso, o script salva um token de sessão em
`~/.garminconnect` — nas próximas execuções você não precisa digitar a
senha de novo (o token é renovado automaticamente).

Para não digitar o e-mail toda vez, você pode exportar antes de rodar:

```bash
export GARMIN_EMAIL="seu-email@exemplo.com"
```

(evite exportar a senha em `GARMIN_PASSWORD` num histórico de shell
persistente — prefira deixar o script perguntar com `getpass`.)

## Baixar todos os seus dados (`export_data.py`)

Depois de conectar com `connect.py` (a sessão já fica salva), rode:

```bash
python3 export_data.py
```

Isso baixa e salva em arquivos `.json` dentro de `garmin-connect/data/`
(pasta ignorada pelo git — seus dados de saúde nunca vão pro repositório):

- `data/profile.json` — perfil, dispositivos, equipamentos, recordes pessoais, metas
- `data/trends.json` — tendências de passos, sono, frequência cardíaca de repouso, calorias, body battery, VO2 máx, HRV
- `data/daily/AAAA-MM-DD.json` — um arquivo por dia com sono detalhado, estresse, SpO2, respiração, hidratação, composição corporal, prontidão de treino
- `data/activities.json` — lista de atividades
- `data/activities/<id>.json` — detalhe e splits de cada atividade

Por padrão ele pega **os últimos 7 dias** e **até 20 atividades**, de propósito,
porque a Garmin também limita quantas requisições você pode fazer por vez
(foi o erro 429 que vimos antes). Depois que um run pequeno funcionar sem
erro, pode pedir mais:

```bash
python3 export_data.py --days 30 --activities-limit 100
```

Para baixar também o arquivo original de cada atividade (FIT/GPX/etc, dentro
de um .zip por padrão):

```bash
python3 export_data.py --download-files
```

Se der erro de limite de requisições (429) no meio do processo, não tem
problema: tudo que já foi baixado até ali já está salvo em `data/`. Espere
um tempo e rode de novo.
