from abc import abstractmethod, ABCMeta

from pymongo import MongoClient


class BaseWebsite:
    __metaclass__ = ABCMeta
    # Database Info
    db_host = "82.217.36.166"
    db_user = "shoper"
    db_password = "mody1"
    db_name = ""
    website_name = ""
    db_port = 27017

    # Search field
    search_field = ""
    sort_field = ""

    # Fields to return in output
    output_fields = dict()

    def __init__(self):
        self.client = None
        self.mongo_db = None

    def connect_to_db(self):
        self.client = MongoClient("mongodb://{}:{}@{}:{}/{}"
                                  .format(self.db_user, self.db_password,
                                          self.db_host, self.db_port, self.db_name))
        self.mongo_db = self.client[self.db_name]

    @abstractmethod
    def get_product_collection(self, site_id=None):
        pass

    @abstractmethod
    def set_output_fields(self):
        pass

    @abstractmethod
    def put_extra_field(self, product):
        pass

    def get_output_fields(self, product_list):
        new_product_list = list()
        for product in product_list:
            product_obj = dict(website=self.website_name)
            for field_key, field_path in self.output_fields.items():
                self.put_extra_field(product)
                product_obj[field_key] = self.get_field_value(product, field_path)
            new_product_list.append(product_obj)
        return new_product_list

    def get_search_query(self, keyword, product_collection, limit):
        # Select required fields
        field_dict = dict()

        for val in self.output_fields.values():
            field_dict[val] = 1

        field_dict[self.sort_field] = 1
        field_dict['_id'] = 0

        return (self.mongo_db[product_collection].find(
            {'$text': {"$search": keyword}}, field_dict
        ).sort([(self.sort_field, 1)]).limit(limit))

    @abstractmethod
    def search_products(self, keyword, aspect_filters, category_ids, item_filters,
                        page_num=1, sort_order=False, limit=100):
        pass

    @staticmethod
    def get_field_value(json_obj, field_path):
        field_path = field_path.split('.')
        field_val = json_obj
        for field_key in field_path:
            field_val = field_val.get(field_key)
        return field_val

    def get_price(self):
        pass
