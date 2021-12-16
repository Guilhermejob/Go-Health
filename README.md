# Go Health

## documentação

#

### O problema a ser solucionado

Cada vez mais a alimentação do brasileiro vem piorando drasticamente, altos consumos de açucares, sal, gorduras ruins tem sido rotina na nossa alimentação, refeições equilibradas são necessárias para que nosso corpo consiga realizar as atividades diárias. E muitas vezes essas pessoas querem melhorar sua qualidade de vida através da alimentação porem ou não sabem como, ou não tem tempo para sair e procurar um nutricionista.

### A Solução

Analisando um dos maiores problemas citados geralmente é o tempo, muitas vezes as pessoas relamente querem mudar de vida na questão alimentícia, porem, muitas vezes por causa de uma rotina muito agitada, a pessoa não se permite reservar um tempinho para sair a procura de um bom nutricionista, e que atenda a suas necessidades, pensando nisso, achamos na tecnologia uma solução de aproximar profissionais nutricionistas e pacientes, o Go Health faz essa ligação de paciente e nutricionista da melhor forma possível.

#

## Instalação

- Primeiro faça o fork deste [repositório](https://gitlab.com/issdomingoss/capstone3-go-health).

- Em seguida faça um git clone para a sua maquina

- Crie o ambiente um ambiente [virtual em python](https://docs.python.org/pt-br/3/tutorial/venv.html)

```
$ python -m venv venv --upgrade-deps
```

- Entre no ambiente virtual

```
$ source venv/bin/activate
```

- Instale as dependencias no arquivo `requirements.txt`

```
$ pip install -r requirements.txt
```

- Configure suas variáveis segundo o arquivo `.env.example`

  - Não esqueça de criar o seu banco de dados e adicionar no .env

- Crie as tabelas no banco de dados através do comando

```
$ flask db upgrade
```

- Inicie a aplicação local através do comando

```
$ flask run
```

- A aplicação inicializará na rota http://127.0.0.1:5000/. Você deverá ver algo semelhante ao snippet logo abaixo no seu terminal:

```
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 112-925-941
```

#

## Documentação das rotas e retornos

Você pode acessar a documentação das rotas clicando em [Doc API](https://documenter.getpostman.com/view/18771913/UVR8poBq)

#

## Desenvolvedores responsáveis pelo projeto

- [Italo Domingos](https://www.linkedin.com/in/issdomingos/)
- [Guilherme Job](https://www.linkedin.com/in/guilherme-armesto-job/)
- [Lorena Belo](https://www.linkedin.com/in/lorena-belo-873828a7/)
- [Gabriel dos Prazeres](https://www.linkedin.com/in/gabrieldosprazeres/)
- [Miqueias Carvalho](https://www.linkedin.com/in/miqueias-carvalho-dos-santos/)
