# PyTelegraphAPI
Éste es una API para [Telegra.ph](https://telegra.ph/api) escrita en Python 3. En la clase `Telegraph` se define diferentes funciones para crear y editar la cuenta de usuario de [Telegra.ph](https://telegra.ph); permitiendo la publicación y edición de artículos, como también la obtención de estadística de los mismos.

## Instalación
Copia y pega el directorio **pytelegraph** al espacio de trabajo. Pronto lo haré más fácil, y si me envías un _pull request_..., ¡mejor!

## Uso
Puedes crear un objeto `Telegraph` desde un `token`, o pedir crear una cuenta nueva.

Para crear un objeto apartir de una cuenta existente, puedes crear un objeto `Account` y pasarlo al constructor de la clase `Telegraph`, o usar su método de clase `.new_from_token(access_token)`.

```python
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pytelegraph

# un token cualquiera
my_token = "xcvbnm123456789es3un3ejemplo3xd"

# un objeto Account que tenías ya preparado...
account = get_account_from_anywhere()

# creamos un objeto Telegraph desde Account:
my_telegraph = pytelegram.Telegraph(account)

# creamos un objeto Telegraph desde token:
my_telegraph = pytelegram.Telegraph.new_from_token(token)
```

Por otro lado, para crear una cuenta nueva:

```python
pytelegraph.Telegraph.new_from_new_account(
    short_name="Daniela",
    author_name="Daniela Peralta",
    author_url="https://t.me/DanielaPeralta" # Espero que nadie... se cree esta cuenta y me toque cambiar este ejemplo :v
)
```

Si tenéis problema con la visualización por culpa de los logs, podéis quitarlo:

```python
import logging
import pytelegraph

pytelegraph.logger.setLevel(logging.ERROR)
```

Otra cosa, ¡Hay documentación en el código! (y en [Telegra.ph](https://telegra.ph/api))
