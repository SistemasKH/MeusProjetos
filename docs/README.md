# Classes, atributos e métodos

`models.py`

* Modelo é uma classe, ex, `EscalaResponsavel`
* Nome do campo é um atributo, exemplo, `data_inicio`
* Métodos da classe, exemplo, `__str__` ou `get_absolute_url`

Se você criar um método chamado `conta_horas`, este método é da classe `EscalaResponsavel`.

Se você criar um método e colocar `@property`, ex:

```
@property
def list_url(self):
    ...
```

`@property` significa um método que vira um atributo, ou seja, se o campo `data_inicio` é um atributo, o `list_url` também é um atributo.

No template

```
{% for object in object_list %}
    <td>{{ object.data_inicio }}</td>
    <td>{{ object.hora_inicio }}</td>
    <td>{{ object.list_url }}</td>
    <td>{{ object.conta_horas }}</td>
{% endfor %}
```

## self

É um valor que diz que o método é da própria classe, ou seja:

```python
class Pessoa:
    nome = 'Claudia'
    sobrenome = 'Hernandez'
    nome_completo = ''

    def full_name(self):
        return f'{self.nome} {self.sobrenome}'

    def save(self):
        nome_completo = self.full_name()
        self.save()
```