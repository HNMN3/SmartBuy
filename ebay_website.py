from base_website import BaseWebsite


class EbayWebsite(BaseWebsite):
    sort_field = "sellingStatus.currentPrice.value"
    db_name = "shoper_ebay_api"
    website_name = 'ebay'

    def get_product_collection(self, site_id=None):
        return "products_{}".format(site_id)

    def set_output_fields(self):
        self.output_fields = {
            "title": "title",
            "promotion_link": "promotion_link",
            "category_name": "primaryCategory.categoryName",
            "thumbnail": "galleryURL",
            "price": "sellingStatus.convertedCurrentPrice.value",
            "currency": "sellingStatus.convertedCurrentPrice._currencyId"
        }
