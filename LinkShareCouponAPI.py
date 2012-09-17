import urllib
import httplib2
from xml.dom import minidom
from datetime import datetime
import sys
from LinkShareAPI2 import *


class LinkShareCouponAPI(LinkShareAPI):
  """ Coupon api for Linkshare """
  promotion_types = [
      {'General Promotion': 1},
      {'Buy One / Get One': '2'},
      {'Clearance': '3'},
      {'Free Shipping': '7'},
      {'Gift with Purchase': '9'},
      {'Percentage off': '11'},
      {'Deal of the Day/Week': '14'},
      {'Black Friday': '30'},
      {'Cyber Monday': '31'},

  ]
  urldata_dict = {
    'mid': '36342',
    'resultsperpage': '500',
    #'promotiontype': 1
    'type': 'text',
  }
  submiturl = 'http://couponfeed.linksynergy.com/coupon?'
  default_submiturl = 'http://couponfeed.linksynergy.com/coupon?'
  
  def ProcessData(self):
    """ Process the data returned from fetch http"""
    if not self.data:
      return False
    dom = minidom.parseString(self.data)
    try:
      products = dom.getElementsByTagName('couponfeed')[0]
    except IndexError:
      products = None
      return False

    self.product_results=LinkShareCouponXMLReader(products)
    if self.debug:
      self._process_log()
    return True

  def _http_geturl_log(self):
    d = "%s:: GETURL: %s\n" % (self.logtime, self.submiturl)
    o=open(LS_API_HTTPGET_LOG, 'a')
    o.write(d)
    o.close()

  
  # overwrite base.ProcessData
  
