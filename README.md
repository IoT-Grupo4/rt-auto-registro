# Dependências

* python3-pip
* Tornado
* PyYAML

# Instalação

Conforme executada no Ubuntu 16.04:

```bash
$ sudo apt-get install python3-pip
$ sudo pip3 install -r requeriments.txt
```

# Execução

```bash
python3 app.py
```

# Configuração

Parâmetros devem ser editados no arquivo `config.yaml`.

# Funcionamento

O código checa a existência do arquivo de token (conforme configurado em `config.yaml`). Caso não exista, solicita um novo e salva a string do token no arquivo. Caso exista, não faz nada.

É possível inserir o código dos sensores criando uma classe Handler apropriada com um método para monitorar constantemente os sensores. Exemplo:

```python
class SensorHandler

@gen.coroutine
def start_sensors(self):
    while True:
        # Adiconar leitura dos sensores aqui e chamar outros metodos sob demanda

```

Assim, em `app.py`, podemos fazer:

```python
from handlers.SensorHandler import SensorHandler
# [...]
sensor_handler = SensorHandler()
# [...]
request_handler = RequestHandler(http_client)
register_handler = RegisterHandler(request_handler)
register_handler.register_device()
sensor_handler.start_sensors() # inicia monitoramento dos sensores
# [...]
```

O ioLoop do tornado se encarrega de manter o código sempre em execução.

TO-DO: Enviar arquivo de configuração do Supervisor para fazer o código rodar como um daemon em segundo plano sem intervenção e reiniciando sozinho em caso de exceções.
