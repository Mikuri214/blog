# -*- encoding: utf8 -*-
# python -m pip install Markdown
# python html-gen.py

import os
import glob
from os import path
import markdown

FROM_PATH = path.abspath('../')
TO_PATH   = path.abspath('../../kasicass.github.io')
SKIP_DIRS = ('poem', 'html-gen',)

def getFiles(pattern):
	fromPath = path.join(FROM_PATH, pattern)
	files = glob.glob(fromPath)

	result = []
	for filePath in files:
		sourceDir, _ = filePath.split(os.sep)[-2:]
		if sourceDir in SKIP_DIRS:
			continue

		result.append(filePath)

	return result


# link to github's repo .md
def genIndexFile(markdownFiles):
	print 'generating index.html'

	# prepare .md file
	#
	# # title
	# tag1
	# * [2018_10_23_xxx.md][1]
	# tag2
	# * ...
	# [1]:url
	# ...
	pre = 'https://github.com/kasicass/blog/blob/master/'

	tags  = []
	mds   = {}
	hrefs = {}

	# [(tag, file), ...]
	tag_files = [filePath.split(os.sep)[-2:] for filePath in markdownFiles]

	lastTag = None
	for tag, f in tag_files:
		if tag != lastTag:
			if lastTag != None:
				# 2018_10_31_xxx.md
				# 01_xxx.md
				year = mds[lastTag][0].split('_')[0]
				if len(year) == 4:
					# only revert it when it's blog article
					mds[lastTag].reverse()
					hrefs[lastTag].reverse()
			
			tags.append(tag)
			lastTag    = tag
			mds[tag]   = []
			hrefs[tag] = []

		mds[tag].append(f)
		hrefs[tag].append(pre + path.join(tag, f).replace('\\', '/'))

	result = []
	i = 1
	for tag in tags:
		result.append('## ' + tag)
		for f in mds[tag]:
			result.append('* [' + f + '][' + str(i) + ']')
			i += 1
	
	i = 1
	for tag in tags:
		for url in hrefs[tag]:
			result.append('[' + str(i) + ']:' + url)
			i += 1

	# print '\n'.join(result)

	# .md => .html
	html = '# kasicass\' blog\n' + '\n'.join(result)
	html = markdown.markdown(html.decode('utf-8'))
	html = '''
<html>
<head>
<meta charset="utf-8">
</head>
<body>''' + html + '''
</body>
</html>
'''

	indexFile = path.join(TO_PATH, 'index.html')
	with open(indexFile, 'w') as f:
		f.write(html.encode('utf-8'))

def main():
	# only generate index.html
	markdownFiles = getFiles('*/*.md')
	genIndexFile(markdownFiles)

if __name__ == '__main__':
	main()
