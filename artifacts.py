"""
Artifact generation functions
"""
import re

class BlockQute():
	type = 'block quote'
	def __init__(self, text):
		self.text = text
	def dict(self):
		return {'type':self.type, 'text':self.text}

class CodeBlock():
	type = 'code block'
	def __init__(self, lang, code):
		self.lang = lang
		self.code = code
	def dict(self):
		return {'type':self.type, 'lang':self.lang, 'code':self.code}

class Image():
	type = 'image'
	def __init__(self, src, alt):
		self.src = src
		self.alt = alt
	def dict(self):
		return {'type':self.type, 'src':self.src, 'alt':self.alt}

class WordArt():
	type = 'word art'
	def __init__(self, html):
		self.html = html
	def dict(self):
		return {'type':self.type, 'html':self.html}





