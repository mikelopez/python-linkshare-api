import urllib
import httplib2
from xml.dom import minidom
from datetime import datetime
import sys


from XMLReader import LinkShareXMLReader, LinkShareCouponXMLReader

#sys.path.append('../')

from settings import LS_API_TOKEN, LS_API_SUBMITURL, LS_API_HTTPGET_LOG, \
	LS_API_HTTPRESPONSE_LOG, LS_API_HTTPERRORS_LOG, LS_API_PROCESS_LOG

class LinkShareAPI:
	""" Linkshare API class for the merchandiser query tool """

	submiturl = LS_API_SUBMITURL
	default_submiturl = LS_API_SUBMITURL
	urldata_dict = {
		'keyword': '', 
		'mid': '',
		'pagenumber': '',
		'MaxResults': 20,
		'sorttype': '',
		'sort': '',

	}
	product_results = []
	token = LS_API_TOKEN
	logtime = datetime.now()
	debug = True

	response = None
	data = None

	#used for couponing and shit
	link_types = [
		'banner', 'text', 'product'
	]
	def __init__(self, token=None, debugbool=False):
		if token:
			self.token = token
		if debugbool:
			self.debug = debugbool

	def FetchHTTP(self, seturl=True):
		""" set the responsedata and actual data ready to be parsed"""
		if seturl:
			self.SetURL()

		# log keyword and geturl
		if self.debug:
			self._http_geturl_log()

		httpsend = httplib2.Http(timeout=20)
		try:
			self.response, self.data = httpsend.request(self.submiturl, 'GET', {})
			#print self.data
		except httplib2.ServerNotFoundError:
			self.response = None
			self.data = None

		if self.debug:
			self._http_response_log()


	def ProcessData(self):
		""" Process the data returned from fetch http"""
		if not self.data:
			return False
		dom = minidom.parseString(self.data)
		try:
			products = dom.getElementsByTagName('result')[0]
		except IndexError:
			products = None
			return False
		
		self.product_results=LinkShareXMLReader(products)
		if self.debug:
			self._process_log()
		return True
		

	def SetParameter(self, key, value):
		""" Set parameter - KEY MUST EXIST """
		if key in self.urldata_dict.keys():
			self.urldata_dict[key] = value
			return True
		else:
			return False

	def SetURL(self, overwrite=None):
		""" called directlry or from self.FetchHTTP() if seturl is set to True"""
		if overwrite:
			self.submiturl = overwrite
		else:
			#self.submiturl = LS_API_SUBMITURL
			self.submiturl = self.default_submiturl

		self.submiturl += 'token=%s' % (LS_API_TOKEN)
		for k,v in self.urldata_dict.items():
			if k == 'keyword': 
				self.submiturl += '&%s=%s' % (k, self.ParseKeyword(v))
			else:
				if not self.urldata_dict[k] == '':
					self.submiturl += '&%s=%s' % (k,v)

	def ParseKeyword(self, kw):
		""" parse the string here and return it back """
		return str(kw).replace(' ', '+')



	# logging stuff

	def _http_geturl_log(self):
		d = "%s:: SearchPhrase: %s\n" % (self.logtime, self.urldata_dict['keyword'])
		d += "%s:: GETURL: %s\n" % (self.logtime, self.submiturl)
		o=open(LS_API_HTTPGET_LOG, 'a')
		o.write(d)
		o.close()
	
	def _http_response_log(self):
		#d = "%s:: RESPONSE\n%s\n======DATA\n%s\n" % (self.logtime, self.response, self.data)
		d = "%s:: RESPONSE\n%s\n======DATA (RESULT)\n%s\n\n" % (self.logtime, self.response, self.product_results)
		o=open(LS_API_HTTPRESPONSE_LOG, 'a')
		o.write(d)
		o.close()


	def _http_errors_log(self, msg):
		d = "%s:: ERROR\n%s\n\n" % (self.logtime, msg)
		o=open(LS_API_HTTPERRORS_LOG, 'a')
		o.write(d)
		o.close()

	# added - not partof standard feature lists since its custom for client scripts
	def _process_log(self):
		d = "%s:: PROCESS: %s\n====\n%s\n" % (self.logtime, self.response, self.product_results)
		o=open(LS_API_PROCESS_LOG, 'a')
		o.write(d)
		o.close()
