#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import json

URL = 'https://api.telegra.ph/'

class ErrorWorker(Exception):

	def __init__(self, msg, function, result):
		super(ErrorWorker, self).__init__('Error en proceso de trabajo. {0}'.format(msg))
		self.function = function
		self.result = result


def exchange(method, *args, **kwargs):
	'''Procesa las peticiones recibidas y retorna datos.
	'''
	info_web = requests.get('%s/%s' % (URL, method), params=kwargs)
	content = info_web.content.decode('utf-8')
	if info_web.status_code == 404:
		raise ErrorWorker('Error en método exchange() código HTTP 404 - Not Found', method, content)
	dictionary = json.loads(content)
	if dictionary['ok'] == False:
		raise ErrorWorker('Error en método exchange()', method, dictionary['error'])
	return dictionary['result']

def exchange_path(method, path, *args, **kwargs):
	'''Redirige los datos recibidos al método exchange().
	'''
	exchange('%s/%s' % (method, path), *args, **kwargs)
