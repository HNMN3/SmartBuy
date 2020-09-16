import json

from ebaysdk.finding import Connection as FindingAPI
from requests.exceptions import ConnectionError

from base_website import BaseWebsite


class EbayWebsite(BaseWebsite):
    sort_field = "sellingStatus.currentPrice.value"
    db_name = "shoper_ebay_api"
    website_name = 'ebay'

    # CODES
    UNKNOWN_ERROR = 500
    LIMIT_EXCEEDED = 410
    OK = 200

    def __init__(self):
        super(EbayWebsite, self).__init__()
        self.finding_api = FindingAPI(
            appid='sample_app_id', config_file=None)

    def call_api(self, search_criteria):
        try:
            # Calling the api
            res = self.finding_api.execute('findItemsAdvanced', search_criteria)
            return res, self.OK
        except ConnectionError as conn_err:
            # This gets called when daily call limit is over
            # Stopping the code here
            print(conn_err)
            return None, self.LIMIT_EXCEEDED
        except Exception as unknown_err:
            print("Error in fetching products for search criteria: {}"
                  .format(search_criteria))
            print(unknown_err)
            return None, self.UNKNOWN_ERROR

    def put_extra_field(self, product):
        url = product.get("viewItemURL")
        promotion_link = ("https://rover.ebay.com/rover/1/link/1?"
                          "campid=sample_camp_id&"
                          "toolid=10018&mpre=%s" % url)
        product['promotion_link'] = promotion_link
        product['price'] = float(self.get_field_value(product,
                                                      "sellingStatus.convertedCurrentPrice.value"))

    def get_product_collection(self, site_id=None):
        return "products_{}".format(site_id)

    def set_output_fields(self):
        self.output_fields = {
            "title": "title",
            "category_name": "primaryCategory.categoryName",
            "thumbnail": "galleryURL",
            "price": "price",
            "currency": "sellingStatus.convertedCurrentPrice._currencyId",
            "promotion_link": "promotion_link"
        }

    def search_products(self, keyword, aspect_filters, category_ids, item_filters,
                        page_num=1, sort_order=False, limit=100):
        aspect_filters_list = list()
        for key, val in aspect_filters.items():
            aspect_obj = {
                "aspectName": key,
                "aspectValueName": val
            }
            aspect_filters_list.append(aspect_obj)
        search_criteria = {
            "outputSelector": ['AspectHistogram', 'SellerInfo', 'CategoryHistogram',
                               'GalleryInfo', 'StoreInfo', 'UnitPriceInfo'],
            "keywords": keyword,
            "aspectFilter": aspect_filters_list,
            "categoryId": category_ids,
            "itemFilter": item_filters,
            "paginationInput": {
                "entriesPerPage": limit,
                "pageNumber": page_num or 1
            },
        }
        if sort_order:
            search_criteria["sortOrder"] = "PricePlusShippingLowest"
        res, code = self.call_api(search_criteria)
        if code == self.OK:
            data = json.loads(res.json())
            products = list()
            aspect_stats = list()
            category_stats = list()

            if (data and data.get('searchResult')
                    and data.get('searchResult').get('item')):
                products = data['searchResult']['item']

            if (data and data.get('aspectHistogramContainer')
                    and data.get('aspectHistogramContainer').get('aspect')):
                aspect_stats = data['aspectHistogramContainer']['aspect']

            if (data and data.get('categoryHistogramContainer')
                    and data.get('categoryHistogramContainer')
                            .get('categoryHistogram')):
                category_stats = data['categoryHistogramContainer'][
                    'categoryHistogram']

            result = {
                'products': self.get_output_fields(products),
                'aspect_stats': aspect_stats,
                'category_stats': category_stats
            }
            return result
        elif code == self.LIMIT_EXCEEDED:
            return {'error': "Search limit exceeded!!"}
        else:
            return {'error': "Service is down due to unknown issue!!"}
