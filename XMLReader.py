def LinkShareCouponXMLReader(products):
	"""
	[<DOM Element: categories at 0x8b68dec>,
	<DOM Element: promotiontypes at 0x8b6f02c>, 
	<DOM Element: offerdescription at 0x8b6f1ec>, 
	<DOM Element: offerstartdate at 0x8b6f24c>, 
	<DOM Element: offerenddate at 0x8b6f2ac>, 
	# optional couponcode
	# optional couponrstriction
	<DOM Element: clickurl at 0x8b6f30c>, 
	<DOM Element: impressionpixel at 0x8b6f36c>, 
	<DOM Element: advertiserid at 0x8b6f3cc>, 
	<DOM Element: advertisername at 0x8b6f42c>, 
	<DOM Element: network at 0x8b6f4cc>]

	"""
	product_results = []
	if not products:
		return False

	for i in products.childNodes:
		#print i.getAttribute('type')
		#print dir(i)
		if i.getAttribute('type') == 'TEXT':
			if str(i.nodeName) == 'link':
				#print dir(i)
				#print i.getElementsByTagName('clickurlass')[0].firstChild.data
				description, start_date, end_date, mid, merchant_name, coupon_code = \
					None, None, None, None, None, None  

				# list dict that defines the API keys with our return names
				api_keys = {'offerdescription': 'description',
					'offerstartdate': 'start_date', 
					'offerenddate': 'end_date',
					'advertiserid': 'mid',
					'advertisername': 'advertisername',
					'couponcode': 'coupon_code',
					'clickurl': 'clickurl'	}

				parsed_data = {}
				for k,v in api_keys.items():
					if i.getElementsByTagName(k):
						parsed_data[v] = i.getElementsByTagName(k)[0].firstChild.data

				product_results.append(parsed_data)

	return product_results

def LinkShareXMLReader(products):
	product_results=[]
	if not products:
		return False
	
	"""
		# 0 [<DOM Element: mid at 0x830d80c>, 
		# 1 <DOM Element: merchantname at 0x830d86c>, 
		# 2 <DOM Element: linkid at 0x830d8ec>, 
		# 3 <DOM Element: createdon at 0x830d94c>, 
		# 4 <DOM Element: sku at 0x830d9ac>, 
		# 5 <DOM Element: productname at 0x830da2c>, 
		# 6 <DOM Element: category at 0x830da8c>, 
		# 7 <DOM Element: price at 0x830db8c>, 
		# 8 <DOM Element: upccode at 0x830dc6c>, 
		# 9 <DOM Element: description at 0x830dcac>, 
		# 10 <DOM Element: keywords at 0x830ddac>, 
		# 11 <DOM Element: linkurl at 0x830de0c>, 
		# 12 <DOM Element: imageurl at 0x830de6c>]
	"""

	for i in products.childNodes:
		if str(i.nodeName) == 'item':
			addit = True
			try:
				mid = i.childNodes[0].firstChild.data
			except:
				mid = 'nothing'
				addit = False
			try:
				merchantname = i.childNodes[1].firstChild.data
			except:
				merchantname = 'nothing'
				#addit = False
			try:
				linkid = i.childNodes[2].firstChild.data
			except:
				linkid = 'nothing'
				addit = False
			try:
				sku = i.childNodes[4].firstChild.data
			except:
				sku = 'nothing'
			try:
				productname = i.childNodes[5].firstChild.data
			except:
				productname = 'nothing'
				addit = False
			try:
				categorypri = i.childNodes[6].childNodes[0].firstChild.data
			except:
				categorypri = 'nothing'
			try:
				categorysec = i.childNodes[6].childNodes[1].firstChild.data
			except:
				categorysec = 'nothing'
			try:
				price = i.childNodes[7].firstChild.data
			except:
				price = 'nothing'
				addit = False
			try:
				upccode = i.childNodes[8].firstChild.data
			except:
				upccode = 'nothing'
			try:
				desclong = i.childNodes[9].childNodes[1].firstChild.data
			except:
				desclong = 'nothing'
			try:
				descshort = i.childNodes[9].childNodes[0].firstChild.data
			except:
				descshort = 'nothing'
			try:
				keywords = i.childNodes[10].firstChild.data
			except:
				keywords = 'nothing'
			try:
				linkurl = i.childNodes[11].firstChild.data
			except:
				linkurl = 'nothing'
				addit = False
			try:
				imgurl = i.childNodes[12].firstChild.data
			except:
				imgurl = 'nothing'
				addit = False
			
			if addit:	
				product_results.append({
					'merchantname':merchantname,
					'merchantid': mid,
					'linkid':linkid,
					'productname':productname,
					'category_pri':categorypri,
					'category_sec':categorysec,
					'price':price,
					'description_short':descshort,
					'description_long':desclong,
					'keywords':keywords,
					'linkurl':linkurl,
					'imgurl':imgurl,
					'sku':sku,
					'upccode':upccode
				})
	return product_results



