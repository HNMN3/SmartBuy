'''
Created by auto_sdk on 2019.12.16
'''
from top.api.base import RestApi
class AliexpressAffiliateOrderGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.app_signature = None
		self.fields = None
		self.order_numbers = None

	def getapiname(self):
		return 'aliexpress.affiliate.order.get'
