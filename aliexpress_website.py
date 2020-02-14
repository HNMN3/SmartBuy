from base_website import BaseWebsite


class AliExpressWebsite(BaseWebsite):
    sort_field = "target_sale_price"
    db_name = "shoper_aliexpress_api"
    website_name = 'aliexpress'

    def get_product_collection(self, site_id=None):
        return "products"

    def set_output_fields(self):
        self.output_fields = {
            "title": "product_title",
            "promotion_link": "promotion_link",
            "category_name": "first_level_category_name",
            "thumbnail": "product_main_image_url",
            "price": "target_sale_price"
        }
