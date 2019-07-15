#!/usr/bin/python3
# -*- coding: utf-8 -*-

import abc
import json

AVAILABLE_TAGS = [
	"a", "aside", "b", "blockquote", "br",
	"code", "em", "figcaption", "figure",
	"h3", "h4", "hr", "i", "iframe", "img",
	"li", "ol", "p", "pre", "s", "strong",
	"u", "ul", "video"
]

AVAILABLE_ATTRIBUTES = ["href", "src"]

class Node(metaclass=abc.ABCMeta):
	"""Clase abstracta para representar un nodo DOM."""
	@abc.abstractmethod
	def __call__(self):
		pass

	@classmethod
	@abc.abstractmethod
	def new_from(cls, obj):
		pass

class NodeException(Exception):
	pass

class NodeString(Node, str):
	"""Un nodo de texto."""
	def __init__(self, *args, **kwargs):
		Node.__init__(self)
		str.__init__(*args, **kwargs)

	def __call__(self):
		return str(self)

	@classmethod
	def new_from(cls, obj):
		if not isinstance(obj, str):
			raise NodeException("obj is not str")
		return cls(obj)

class NodeElement(Node):
	"""Un nodo de elemento DOM."""
	def __init__(self, tag=None, attrs=None, children=None):
		Node.__init__(self)
		self.tag = tag
		self.attrs = attrs
		self.children = children
		# revisar que la tag sea válida
		if not self.tag in AVAILABLE_TAGS:
			raise NodeException("The tag name is weird: %s" % self.tag)
		# si tiene attrs, revisar su tipo
		if self.attrs:
			for k in self.attrs.keys():
				if not k in AVAILABLE_ATTRIBUTES:
					raise NodeException("The attrs name is weird: %s" % k)
		# si tiene children, revisar su tipo
		if self.children:
			for child in self.children:
				if not isinstance(child, Node):
					raise NodeException(
						"The children list has a weird object type: %s" % type(child))

	def __call__(self):
		dictionary = dict(tag=self.tag)
		if self.attrs:
			dictionary["attrs"] =self.attrs
		if self.children:
			dictionary["children"] =[child() for child in self.children]
		return dictionary

	@classmethod
	def new_from(cls, obj):
		if isinstance(obj, str):
			dictionary = json.loads(obj)
		elif isinstance(obj, dict):
			dictionary = obj
		else:
			raise NodeException("obj is neither str nor dict")
		tag = dictionary.get("tag")
		attrs = dictionary.get("attrs")
		children = None
		if dictionary.get("children"):
			children = list()
			for child in dictionary["children"]:
				if isinstance(child, dict):
					children.append(cls.new_from(child))
				else:
					children.append(NodeString.new_from(child))
		return cls(tag, attrs, children)