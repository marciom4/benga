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
