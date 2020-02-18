from flask import request
from flask_restful import Resource

from ebay_website import EbayWebsite
from aliexpress_website import AliExpressWebsite


class SearchView(Resource):
    available_websites = {
        'ebay': EbayWebsite,
        'aliexpress': AliExpressWebsite
    }
    website_objs = dict()

    def __init__(self):
        super(SearchView, self).__init__()

        # Update objs dict
        for website_key, website_class in self.available_websites.items():
            website_obj = website_class()
            # website_obj.connect_to_db()
            website_obj.set_output_fields()
            self.website_objs[website_key] = website_obj

    def post(self):
        data = request.json
        websites = data.get('websites')
        search_keyword = data.get('search_keyword')
        aspect_filters = data.get('aspect_filters') or dict()
        category_ids = data.get('category_ids') or list()
        item_filters = data.get('item_filters') or dict()
        page_num = data.get('page_num') or 1
        sort_order = data.get('sort_order') or False

        if not search_keyword:
            return {"error": "Search keyword is necessary", 'status': 400}

        invalid_websites = []
        valid_websites = []
        for website_name in websites:
            if website_name in self.available_websites:
                valid_websites.append(website_name)
            else:
                invalid_websites.append(website_name)

        if invalid_websites:
            response = {'error': ("We don't work with following sites yet: {}"
                                  .format(', '.join(invalid_websites))),
                        'status': 400, }
            return response
        all_products = list()
        total_len = 0
        all_aspect_stats = list()
        all_category_stats = list()
        for website_name in valid_websites:
            website_obj = self.website_objs[website_name]
            search_products = list()
            aspect_stats = list()
            category_stats = list()
            try:
                search_data = website_obj.search_products(
                    search_keyword, aspect_filters, category_ids,
                    item_filters, page_num, sort_order
                )
                search_products = search_data.get('products') or list()
                aspect_stats = search_data.get('aspect_stats') or list()
                category_stats = search_data.get('category_stats') or list()
            except Exception as e:
                print(e)
                import traceback
                traceback.print_exc()
            total_len += len(search_products)
            all_products += search_products

            # TODO: process the aspect and category stats
            all_aspect_stats += aspect_stats
            all_category_stats += category_stats
        return {
            'total_products': total_len,
            'status': 200,
            'products': all_products,
            # 'aspect_stats': all_aspect_stats,
            # 'category_stats': all_category_stats
        }
