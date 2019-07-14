#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import logging


# Preparando un objeto de Logger
logger = logging.getLogger("Telegraph")
console_output_handler = logging.StreamHandler(sys.stderr)
console_output_handler.setFormatter(
	logging.Formatter("%(asctime)s (%(filename)s:%(lineno)d) %(levelname)s - %(name)s: \"%(message)s\"")
)
logger.addHandler(console_output_handler)
logger.setLevel(logging.INFO)


import pytelegraph.elements as elements
import pytelegraph.worker as worker

class Telegraph:
	"""La clase *Telegraph* define un objeto telegraph con métodos para un fácil
	manejo y administración de publicación minimalista en https://telegra.ph

	Para acceder a la documentación de Telegraph,
	id al [sitio oficial de Telegraph](https://telegra.ph/api)
	"""

	def __init__(self, account):
		"""Crea un nuevo objeto para una `account` proporcionada.

		:param account: cuenta en Telegraph
		"""
		self.account = account

	@classmethod
	def new_from_token(cls, access_token):
		"""Crea un nuevo objeto Telegraph desde un token.

		Realiza una consulta para descargar toda la información de la cuenta al
		que pertenece dicho token, para luego, crear un objeto `Account` válido.

		:param access_token: token de acceso.
		"""
		fields = [
			"short_name", "author_name", "author_url",
			"auth_url", "page_count", "short_name",
			"author_name", "author_url"
		]
		try:
			account = elements.Account.new_empty()
			dictionary = worker.exchange(
				method="getAccountInfo",
				access_token=access_token,
				fields=fields)
			account.to_import(dictionary)
			return cls(account)
		except worker.ErrorWorker as e:
			logger.critical("No puedo obtener la información de esta cuenta [%s]: %s" % (e.function, e.result))
			raise e
		except Exception as e:
			logger.error("Error %s" % e)
			raise e

	def create_account(self, short_name, author_name, author_url="https://telegra.ph/api"):
		"""Crea una cuenta nueva en Telegraph.

		Con este método podéis crear un cuenta nueva. Será
		retorndo un objeto `Account`, el cual tendrá también
		un `access_token`: útil para realizar cambios futuros.

		:param short_name: corto nombre usado para la identificación interna.
		:param author_name: nombre usado en cada artículo.
		:param author_url: URL que hace referencia al autor.
		"""
		try:
			dictionary = worker.exchange(
				method="createAccount",
				short_name=short_name,
				author_name=author_name,
				author_url=author_url
			)
			self.account.to_import(dictionary)
			return self.account
		except worker.ErrorWorker as e:
			logger.error("No puedo crear la cuenta nueva [%s]: %s" % (e.function, e.result))
			raise e

	def edit_account_info(self, short_name=None, author_name=None, author_url=None):
		"""Edita la información de una cuenta.

		Para esto, los valores que sean pasados por argumento, serán
		editados en el perfil de la cuenta de Telegraph. Si no se pasa
		nada, no se editará nada.

		:param short_name: si es definido, cambiamos el short_name.
		:param author_name: si es definido, cambiamos el author_name.
		:param author_url: si es definido, cambiamos el author_url.
		"""
		if not any([short_name, author_name, author_url]):
			logger.warning("No se generarán cambiamos en el perfil por falta de datos")
			return None
		if self.account.access_token is None:
			logger.warning("El access_token es nulo.")
			return None
		try:
			dictionary = worker.exchange(
				method="editAccountInfo",
				access_token=self.account.access_token,
				short_name=short_name,
				author_name=author_name,
				author_url=author_url
			)
			self.account.to_import(dictionary)
			return self.account
		except worker.ErrorWorker as e:
			logger.error("No puedo editar la cuenta nueva [%s]: %s" % (e.function, e.result))
			raise e

	def get_account_info(self, fields=["short_name", "author_name", "author_url"]):
		"""obtiene información de la cuenta.

		Este método permite obtener información de dicha cuenta.
		Para esto, tenéis que especificar en la tupla `fields`
		los campos requeridos. Los campos disponibles son:
		- short_name
		- author_name
		- author_url
		- auth_url
		- page_count

		:param fields: tupla que contiene una lista de string con los campos requeridos.

		Ejemplo:
		>>> get_account_info(fields=("auth_url", "page_count"))
		"""
		if self.account.access_token is None:
			logger.warning("El access_token es nulo.")
			return None
		try:
			dictionary = worker.exchange(
				method="getAccountInfo",
				access_token=self.account.access_token,
				fields=fields
			)
			self.account.to_import(dictionary)
			return self.account
		except worker.ErrorWorker as e:
			logger.error("No puedo obtener la información de esta cuenta [%s]: %s" % (e.function, e.result))
			raise e

	def revoke_access_token(self):
		"""Cambia el token de una cuenta de Telegraph.

		Este método intercambia el anterior token de la
		cuenta de Telegraph y genera uno nuevo. También
		permite cambiar el valor de `auth_url`.
		"""
		if self.account.access_token is None:
			logger.warning("El access_token es nulo.")
			return None
		try:
			dictionary = worker.exchange(
				method="revokeAccessToken",
				access_token=sefl.account.access_token
			)
			new_token = dictionary["access_token"]
			new_auth_url = dictionary["auth_url"]
			self.account.access_token = new_token
			self.account.auth_url = new_auth_url
			return True
		except worker.ErrorWorker as e:
			logger.error("No puedo revocar token [%s]: %s" % (e.function, e.result))
			raise e

	def create_page(self, title, author_name, author_url, content, return_content=False):
		"""Crea una nueva página/artículo.

		Permite crear un nuevo artículo, con los datos enviados.
		Si `return_content` es `True`, será retornado un objeto
		`Page`.

		:param title: título del artículo.
		:param author_name: nombre a mostrar del autor.
		:param author_url: URL del perfil del autor.
		:param content: lista de objetos `Node`, ver http://telegra.ph/api#Node
		:param return_content: toma valor `True` para retornar un objeto `Page`. Es `False` por defecto.
		"""
		if self.account.access_token is None:
			logger.warning("El access_token es nulo.")
			return None
		try:
			dictionary = worker.exchange(
				method="createPage",
				access_token=self.account.access_token,
				title=title,
				author_name=author_name,
				author_url=author_url,
				content=content,
				return_content=return_content
			)
			new_page = elements.Page.new_empty()
			new_page.to_import(dictionary)
			return new_page
		except worker.ErrorWorker as e:
			logger.error("No puedo obtener las vistas [%s]: %s" % (e.function, e.result))
			raise e

	def edit_page(self, path, title, content, author_name, author_url, return_content=False):
		"""Permite editar un artículo existente.

		Al terminar, retorna un objeto `Page`.

		:param path: ruta del artículo.
		:param title: título del artículo.
		:param content: contenido del artículo, lista de `Node`, ver http://telegra.ph/api#Node
		:param author_name: nombre del autor, se mostrará bajo el título del artículo.
		:param author_url: URL del perfil del autor.
		:param return_content: toma valor `True` para retornar un objeto `Page`. Es `False` por defecto.
		"""
		if self.account.access_token is None:
			logger.warning("El access_token es nulo.")
			return None
		try:
			dictionary = worker.exchange_path(
				method="editPage",
				path=path,
				access_token=self.account.access_token,
				title=title,
				content=content,
				author_name=author_name,
				author_url=author_url,
				return_content=return_content
			)
			new_edited_page = elements.Page(None,None,None,None)
			new_edited_page.to_import(dictionary)
			return new_edited_page
		except worker.ErrorWorker as e:
			logger.error("No puedo editar esa página [%s]: %s" % (e.function, e.result))
			raise e

	def get_page(self, path, return_content=False):
		"""Retorna un objeto `Page` de una página solicitada.

		:param path: ruta del artículo.
		:param return_content: toma valor `True` para retornar un objeto `Page`. Es `False` por defecto.
		"""
		try:
			dictionary = worker.exchange_path(
				method="getPage",
				path=path,
				return_content=return_content
			)
			new_got_page = elements.Page(None,None,None,None)
			new_got_page.to_import(dictionary)
			return new_got_page
		except worker.ErrorWorker as e:
			logger.error("No puedo obtener una página [%s]: %s" % (e.function, e.result))
			raise e

	def get_page_list(self, offset=0, limit=50):
		"""Permite obtener una lista de páginas de dicha cuenta.

		Retorna una lista, ordenada por orden de creación, perteneciente
		a la cuenta de Telegraph. Lo retorna mediante un objeto
		`PageList`.

		:param offset: número secuencial de la primera página a devolver.
		:param limit: limites de página a devolver.
		"""
		if self.account.access_token is None:
			logger.warning("El access_token es nulo.")
			return None
		try:
			dictionary = worker.exchange(
				method="getPageList",
				access_token=self.account.access_token,
				offset=offset,
				limit=limit
			)
			new_page_list = elements.PageList(**dictionary)
			return new_page_list
		except worker.ErrorWorker as e:
			logger.error("No puedo obtener la lista de páginas [%s]: %s" % (e.function, e.result))
			raise e

	def get_views(self, path, year=None, month=None, day=None, hour=None):
		"""Retorna el número de vistas de una página en un tiempo específico.

		:param path: ruta del artículo.
		:param year: entero que indica el año para buscar.
		:param month: entero que indica el mes para buscar.
		:param day: entero que indica el día para buscar.
		:param hour: entero que indica la hora para buscar.
		"""
		try:
			dictionary = worker.exchange_path(
				method="getViews",
				path=path,
				year=year,
				month=month,
				day=day,
				hour=hour
			)
			new_views = elements.PageViews(0)
			new_views.to_import(dictionary)
			return new_views
		except worker.ErrorWorker as e:
			logger.error("No puedo obtener las vistas [%s]: %s" % (e.function, e.result))
			raise e