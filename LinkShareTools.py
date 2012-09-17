from lxml import html

def getlinks_spreadsheet_text(data):
	""" this function finds the elements from the split text"""
	data_split = data.split('|')
	link_code = str(data_split[0]).replace('\r','').replace('\n','')
	price = None
	parse_text = html.fromstring(link_code)
	extens = ['.jpg','.JPG','.gif','.GIF','.png','.PNG']
	html_image = None
	html_link = None

	for img in parse_text.cssselect('img'):
		for exten in extens:
			if exten in img.get('src'):
				html_image = img.get('src')

	html_title = str(data_split[3]).replace('\r','').replace('\n','')
	html_title_fromhtml = None

	# if theres a name in the link tag and its not the same as spreadsheet	
	# some people put diff values in the column and in the link tag
	# link tag is always the one that works so fall back to that one
	
	for a in parse_text.cssselect('a'):
		html_title_fromhtml = a.text

	if html_title_fromhtml:
		if not html_title == html_title_fromhtml:
			html_title = html_title_fromhtml

	end_date = data_split[5]
	try:
		end_date_day = end_date.split('/')[1]
		end_date_month = end_date.split('/')[0]
		expires = 'y'
	except IndexError:
		expires = 'n'
		end_date_month = None
		end_date_day = None

	if expires == 'n':
		try:
			end_date_day = end_date.split('/')[1]
			end_date_month = end_date.split('/')[0]
			expires = 'y'
		except IndexError:
			expires = 'n'
			end_date_month = None
			end_date_day = None
		


	for spaces in html_title.split(' '):
		if '$' in spaces and '.' in spaces:
			price = spaces.replace('$','').replace(',','').replace('-','')
	
	for a in parse_text.cssselect('a'):
		html_link = a.get('href')

	merchant_text = str(data_split[1]).replace('\r','').replace('\n','')

	return {
		'html_link': html_link,
		'html_image': html_image,
		'html_title': html_title,
		'price': price,
		'merchant_text': merchant_text,
		'expires': expires,
		'end_date_day': end_date_day,
		'end_date_month': end_date_month,
	}
	
