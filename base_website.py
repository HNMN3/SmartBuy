from abc import abstractmethod, ABC

from pymongo import MongoClient


class BaseWebsite(ABC):
    # Database Info
    db_host = "82.217.36.166"
    db_user = "shoper"
    db_password = "mody1"
    db_name = "shoper_ebay_api"
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

    def search_products(self, keyword, product_collection, limit=20):
        search_query = (self.mongo_db[product_collection].find(
            {'$text': {"$search": keyword}}
        ).limit(limit))
        products = []
        for document in search_query:
            product = dict()
            for field_key, field_path in self.output_fields.items():
                product[field_key] = self.get_field_value(document, field_path)
            products.append(product)
        return products

    @staticmethod
    def get_field_value(json_obj, field_path):
        field_path = field_path.split('.')
        field_val = json_obj
        for field_key in field_path:
            field_val = field_val[field_key]
        return field_val
