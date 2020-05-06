"""
Artifact generation functions
"""
import re

class BlockQute():
	type = 'block quote'
	def __init__(self, text):
		self.text = ' '.join(text.split('\n>'))
		self.audioSrc = None
	def dict(self):
		return {'type':self.type, 'text':self.text,'audioSrc': self.audioSrc}

class CodeBlock():
	type = 'code block'
	def __init__(self, lang, code):
		self.lang = lang
		self.code = code
		self.audioSrc = None
	def dict(self):
		return {'type':self.type, 'lang':self.lang, 'code':self.code, 'audioSrc': self.audioSrc}

class Image():
	type = 'image'
	def __init__(self, src, alt):
		self.src = src
		self.alt = alt
		self.audioSrc = None
	def dict(self):
		return {'type':self.type, 'src':self.src, 'alt':self.alt, 'audioSrc': self.audioSrc}

class Model3D():
	type = '3D'
	def __init__(self, src, name):
		self.src = src
		self.name = name
		self.audioSrc = None
	def dict(self):
		return {'type':self.type, 'src':self.src, 'name':self.name, 'audioSrc': self.audioSrc}

class WordArt():
	type = 'word art'
	def __init__(self, html):
		self.html = html
		self.audioSrc = None
	def dict(self):
		return {'type':self.type, 'html':self.html, 'audioSrc': self.audioSrc}





