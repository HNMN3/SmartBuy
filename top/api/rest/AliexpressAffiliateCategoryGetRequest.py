'''
Created by auto_sdk on 2019.09.19
'''
from top.api.base import RestApi
class AliexpressAffiliateCategoryGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.app_signature = None

	def getapiname(self):
		return 'aliexpress.affiliate.category.get'
