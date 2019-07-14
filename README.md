# PyTelegraphAPI
Éste es una API para [Telegra.ph](https://telegra.ph/api) escrita en Python 3. En su clase `Telegraph` se define diferentes funciones para crear y editar cuentas de usuario de [Telegra.ph](https://telegra.ph); permitiendo también la edición, publicación y obtención de estadística de las publicaciones publicadas.

## Instalación
Por el momento, la única forma de usarlo es copiar el directorio __pytelegraph__ al espacio de trabajo. Pronto lo haré más fácil y si me envías un _pull request_..., ¡mejor!

## Uso
Lo primero en hacer, es crear un objeto de la clase `Telegraph`:
```python
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pytelegraph

# creamos un objeto Telegraph:
my_telegraph = pytelegram.Telegraph()
```

Para crear una cuenta nueva:
```python
my_telegraph.create_account(
    short_name="Daniela",
    author_name="Daniela Peralta",
    author_url="https://t.me/DanielaPeralta" # Espero que nadie, ahora, se cree esta cuenta y me toque cambiar este ejemplo :v
)

# listo, ahora en los futuros métodos, cuando necesitéis el `access_token`,
# podéis usar el de la última cuenta creada con: 
last_access_token = my_telegraph.access_token
```

Si tenéis problema con la visualización por culpa de los logs, podéis quitarlo cambiando el siguiente código:
```python
# dentro de : ./pytelegraph/__init__.py
# línea 13. Cambiad:
logger.setLevel(logging.INFO)
# por:
logger.setLevel(logging.ERROR)
# ahora, sólo se mostrará logs si sucede un error grave
```

Otra cosa, ¡Hay documentación en el código! (y en [Telegra.ph](https://telegra.ph/api))
