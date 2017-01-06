#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''Define los diferentes tipos de datos que telegraph procesa.'''

class Element:

	def __init__(self):
		'''Método de Inicialización, debe se sobreescrita.
		'''
		raise NotImplementedError
	
	def to_import(self, dictionary)	:
		'''Importa datos desde un diccionario de datos.

		:param dictionary: diccionario con datos necesarios.
		'''
		for k,v in dictionary.items():
			self.__dict__[k] = v
	
	def __str__(self):
		'''Exporta los datos como un diccionario.
		'''
		new_dict = {}
		for k,v in self.__dict__.items():
			if v != None:
				new_dict[k] = v
		return str(new_dict)

class Account(Element):

	def __init__(self, short_name, author_name, author_url, access_token=None, auth_url=None, page_count=None):
		'''Inicializa la clase administradora de la cuenta de usuario.

		:param short_name: corto nombre usado para la identificación interna.
		:param author_name: nombre usado en cada artículo.
		:param author_url: URL que hace referencia al autor.
		:param access_token: opcional. Token de acceso a la cuenta de telegraph.
		:param auth_url: opcional. URL para acceder a telegra.ph desde el navegador.
		:param page_count: opcional. número de páginas de la cuenta.
		'''
		self.short_name = short_name
		self.author_name = author_name
		self.author_url = author_url
		self.access_token = access_token
		self.auth_url = auth_url
		self.page_count = page_count

class PageList(Element):

	def __init__(self, total_count=0, pages=[]):
		'''Define una lista de artículos de telegraph.
		El más reciente, está en primer lugar.
		:param total_count: entero que significa el número total.
		:param pages: lista de objetos Page.
		'''
		self.total_count = total_count
		self.pages = pages

class PageViews(Element):

	def __init__(self, views):
		'''Define un elemento con datos de vista de página.

		:param views: número de vista de una página.
		'''
		self.views = views

class Page(Element):

	def __init__(self, path, url, title, description, author_name=None, auth_url=None, image_url=None, content=[], views=0, can_edit=None):
		'''Inicializa un objeto Page, propio de un artículo.

		:param path: ruta de la página.
		:param url: URL de la página.
		:param title: título de la página.
		:param description: descripción de la página.
		:param author_name: opcional. Nombre del autor, éste se mostrarás bajo el título.
		:param author_url: opcional, URL a algún perfil del autor.
		:param image_url: opcional. URL a la imagen de la página.
		:param content: opcional. Lista de objetos Content.
		:param views: número de vista de la página.
		:param can_edit: opcional. Es retornado si hemos pasado el access_token. Es `True` si podemos editar.
		'''
		self.path = path
		self.url = url
		self.title = title
		self.description = description
		self.author_name = author_name
		self.author_url = author_url
		self.image_url = image_url
		self.content = content
		self.views = views
		self.can_edit = can_edit
