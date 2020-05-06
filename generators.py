"""
Code to turn text into a set of WordArt artifacts

Using phrasemachine (Handler etal, 2016, EMNLP) 
-- author's implementation -- https://github.com/slanglab/phrasemachine
-- Original paper -- Bag of What? Simple Noun Phrase Extraction for Text Analysis -- http://brenocon.com/handler2016phrases.pdf
"""

import phrasemachine
import spacy
from spacy.tokenizer import Tokenizer
from collections import Counter
import re
from artifacts import BlockQute, CodeBlock, Image, WordArt, Model3D

nlp = spacy.load("en_core_web_sm")

## custom tokenizer to keep **, * intact
match_re = re.compile(r'''\*{1,2}''')
nlp.tokenizer = Tokenizer(nlp.vocab, token_match=match_re.match)

_SENTENCE_ = "margin:auto; text-align:center;"
_PHRASE_ = "font-size:150% !important;"
_ENTITY_ = "font-weight:bold; color:#436591;"

def merge_spans(spans):
	"""
	Merge overlapping spans returned by phrasemachine
	"""
	# assume spans are ordered, increasing
	merged = []
	for span in spans:
		if len(merged)==0:
			merged.append(span)
			continue
		
		addflag = True
		for i in range(len(merged)):
			m = merged[i]
			
			if span[1] < m[0]:
				addflag=False
				continue
			
			elif ((span[0] >= m[0] and span[0]<=m[1]) 
				  or (span[1] >= m[0] and span[1]<=m[1])):
				merged[i] = (min(span[0],m[0]), max(span[1],m[1]))
				addflag=False
				
		if addflag:
			merged.append(span)
			
	return merged

def highlight_ner(tokens):
	""" Highlight named entities """
	arr = []
	for t in tokens:
		if t.ent_iob_ != 'O':
			# class = t.ent_type_
			# arr.append(f'<span style="{_ENTITY_}">{t.text}</span>')
			arr.append(f'<span class="entity">{t.text}</span>')
		else:
			arr.append(t.text)
	
	text = ' '.join(arr)
	text = re.sub(r'\s([?.,!"](?:\s|$))', r'\1', text) # remove whitespace before punctuation 

	return text

def tok_to_text(tokens):
	arr = [t.text for t in tokens]

	text = ' '.join(arr)
	text = re.sub(r'\s([?.,!"](?:\s|$))', r'\1', text) # remove whitespace before punctuation 

	return text

def add_markdown_formatting(html):
	## ** for bold
	html = re.sub(r'\*\*([^\*]+)\*\*', r'<span class="bold"/>\1</span>', html)

	## * for italic
	html = re.sub(r'\*([^\*]+)\*', r'<span class="italic"/>\1</span>', html)

	return html

def to_html(tokens, spans):
	""" HTML Markup """
	curr = 0
	content = []
	if len(spans) == 0:
		content.append(highlight_ner(tokens))
	else:
		for lo,hi in spans:
			if lo >= hi:
				continue
			content.append(tok_to_text(tokens[curr:lo]))

			# content.append(f'<span style="{_PHRASE_}">{highlight_ner(tokens[lo:hi])}</span>')
			# text = highlight_ner(tokens[lo:hi])
			# if len(text) > 0:
			# 	content.append(f'<span class="emphasize">{text}</span>')
			
			text = tok_to_text(tokens[lo:hi])
			if len(text) > 0:
				content.append(f'<span class="emphasize">{text}</span>')
			curr = hi

	# html = f'<div style="{_SENTENCE_}">{" ".join(content)}</div>'
	html = f'<div class="wordart">{" ".join(content).strip()}</div>'
	html = add_markdown_formatting(html)
	return html
	

def wordartify(text):

	doc = nlp(text)
	artifacts = []

	for sent in doc.sents:
		tokens = [token.text for token in sent]
		pos = [token.pos_ for token in doc]
		res = phrasemachine.get_phrases(tokens=tokens, postags=pos, output="token_spans")
		spans = merge_spans(res['token_spans'])
		
		phrases = [tokens[lo:hi] for lo,hi in spans]
		html = to_html([token for token in sent], spans)

		artifacts.append(WordArt(html))
		
	return artifacts


def get_room_artifacts(text):

	## In markdown different sections are separated by line breaks
	# parts = re.split('\\n.?\\n', text) #text.split('\n\n')
	parts = re.split(u'[\n\u200b\r]+', text)
	artifacts = []

	hiddenBlock = False

	# for span in parts:
	i = 0
	while i < len(parts):
		span = parts[i].strip()
		# print(span)


		## Hidden Blocks - not shown in VR
		if not hiddenBlock and span.startswith("~"):
			hiddenBlock = True
			i += 1
			continue
		elif hiddenBlock and not span.startswith("~"):
			i += 1
			continue
		elif hiddenBlock and span.startswith("~"):
			hiddenBlock = False
			i += 1
			continue

		## Section Headers
		if span.startswith('#'):
			i += 1
			continue

		## Theme (extended syntax)
		elif span.startswith("$"):
			i += 1
			continue

		## Audio
		## adds audioSrc to the preceeding artifact
		elif span.startswith("^"):
			match = re.search('\^\(([^\n]*)\)', span)
			audioSrc = match.group(1)
			artifacts[-1].audioSrc = audioSrc

		## > Block quotes
		elif span.startswith('>'):
			artifacts.append(BlockQute(span[2:]))
			# continue

		## Code block
		elif span.startswith('```'):
			# aggregate all lines inside the codeblock
			while not span.endswith('```'):
				i += 1
				span += '\n' + parts[i]

			match = re.search('^```([^\n]*)', span)
			lang = match.group(1)
			_, end = match.span(1)
			code = span[end:-3]
			artifacts.append(CodeBlock(lang, code.strip()))

		elif '\n```' in span:
			subsplit = span.split('\n```')
			artifacts += wordartify(subsplit[0])

			parts[i] = '```' + '\n```'.join(subsplit[1:])
			continue

		## Image ![alt image text](img.jpg)
		elif span.startswith('!['):
			alt = re.search('^!\[(.*)\]', span).group(1)
			src = re.search('\((.*)\)', span).group(1)
			artifacts.append(Image(src, alt))

		## 3D models &[name](src.GLTF)
		elif span.startswith("&"):
			# TODO!
			name = re.search('^&\[(.*)\]', span).group(1)
			src = re.search('\((.*)\)', span).group(1)
			artifacts.append(Model3D(src, name))
		

		## WordArt from Text
		else:
			artifacts += wordartify(span)

		i += 1

	return [a.dict() for a in artifacts]

if __name__ == '__main__':
	# text = 'Malloci is a tool that uses Natural Language Processing and information visualization techniques to generate WebVR content from traditional web content. This content is curated to facilitate ease of consumption for the user, across a variety of VR platforms and browsers.'
	# text = 'And this is just some text'
	# artifacts = wordartify(text)
	# print([a.dict() for a in artifacts])


	txt = "## dogs\n\n![dog with money](img/dog1.jpg)\n\nAnd this is just some text\n\n> This is a <em>very long</em> line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can into a blockquote. \n\n```json\n{\n    \"test\":\"attribute\",\n    \"Hope\":\"It works!\"\n}\n```\n\n![1](img/dog3.jpg)\n\n![2](img/dog4.jpg)\n\n![3](img/dog5.jpg)\n\n\n\nCheck if we can swipe to preview VR\n\n"
	print(get_room_artifacts(txt))


