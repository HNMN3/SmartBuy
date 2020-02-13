from flask import request
from flask_restful import Resource

from ebay_website import EbayWebsite


class SearchView(Resource):
    available_websites = {
        'ebay': EbayWebsite
    }
    website_objs = dict()

    def __init__(self):
        super(SearchView, self).__init__()

        # Update objs dict
        for website_key, website_class in self.available_websites.items():
            website_obj = website_class()
            website_obj.connect_to_db()
            website_obj.set_output_fields()
            self.website_objs[website_key] = website_obj

    def post(self):
        data = request.json
        websites = data.get('websites')
        search_keyword = data.get('search_keyword')
        invalid_websites = []
        valid_websites = []
        for website in websites:
            if website and website.get('name') in self.available_websites:
                valid_websites.append(website)
            else:
                invalid_websites.append(website.get('name'))

        if invalid_websites:
            response = {'error': ("We don't work with following sites yet: {}"
                                  .format(', '.join(invalid_websites))),
                        'status': 400, }
            return response
        all_products = list()
        result_limit = 40
        total_len = 0
        for website in valid_websites:
            website_name = website.get('name')
            site_ids = website.get('site_ids')
            collections_processed = set()
            website_obj = self.website_objs[website_name]
            for site_id in site_ids:
                product_collection = website_obj.get_product_collection(site_id)
                if product_collection in collections_processed:
                    continue
                collections_processed.add(product_collection)
                try:
                    site_products = website_obj.search_products(search_keyword,
                                                                product_collection)
                except Exception as e:
                    print(e)
                    site_products = list()
                total_len += len(site_products)
                all_products += site_products
                if total_len >= result_limit:
                    break
        return {
            'total_products': total_len,
            'status': 200,
            'products': all_products
        }
