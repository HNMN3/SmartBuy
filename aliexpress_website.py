from base_website import BaseWebsite
import top.api
import top
from top.api.base import TopException


class AliExpressWebsite(BaseWebsite):
    sort_field = "target_sale_price"
    db_name = "shoper_aliexpress_api"
    website_name = 'aliexpress'

    def __init__(self):
        super(AliExpressWebsite, self).__init__()

        # Ali express credentials
        self.app_key = '28324225'
        self.secret = 'd38fe5397ded393a3bdc07d017788588'
        self.app_signature = 'qXdMo8DCJaH'
        self.tracking_id = "saydtel3sr"

        self.ali_express = top.api.AliexpressAffiliateProductQueryRequest()
        self.ali_express.set_app_info(top.appinfo(self.app_key, self.secret))

        self.ali_express.app_signature = self.app_signature
        self.ali_express.target_currency = "USD"
        self.ali_express.target_language = "EN"
        self.ali_express.fields = "app_sale_price"
        self.ali_express.page_size = 50
        self.ali_express.tracking_id = self.tracking_id

    def get_product_collection(self, site_id=None):
        return "products"

    def set_output_fields(self):
        self.output_fields = {
            "title": "product_title",
            "promotion_link": "promotion_link",
            "category_name": "first_level_category_name",
            "thumbnail": "product_main_image_url",
            "price": "price",
            "currency": "currency"
        }

    def put_extra_field(self, product):
        currency, price = product['target_sale_price'].split()
        product['price'] = float(price)
        product['currency'] = currency

    def search_products(self, keyword, aspect_filters, category_ids, item_filters,
                        page_num=1, sort_order=False, limit=100):
        self.ali_express.keywords = keyword
        if category_ids:
            self.ali_express.category_ids = ",".join(category_ids)

        if sort_order:
            self.ali_express.sort = 'SALE_PRICE_ASC'
        else:
            self.ali_express.sort = ''
        self.ali_express.page_no = page_num
        try:
            product_response = self.ali_express.getResponse()
            product_response = product_response[
                'aliexpress_affiliate_product_query_response']

            response_code = int(product_response['resp_result']['resp_code'])
            if response_code == 405:
                return {'error': "Search limit exceeded!!"}
            aspect_stats = list()
            category_stats = list()

            products = product_response['resp_result']['result']['products'][
                'product']
            result = {
                'products': self.get_output_fields(products),
                'aspect_stats': aspect_stats,
                'category_stats': category_stats
            }
            return result
        except TopException:
            return {'error': "Service is down due to unknown issue!!"}
        except Exception as unknown_err:
            print("Error in fetching products for keyword: {}"
                  .format(keyword))
            print(unknown_err)
            import traceback
            traceback.print_exc()
            return {'error': "Service is down due to unknown issue!!"}
