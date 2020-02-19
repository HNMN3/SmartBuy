## Requirements:  
- Python 2.7

## Deploying the project:  
- Put the project zip file on server  
- Extract it  
- Install the required libraries using following command:  
    > pip install -r requirements.txt

## Running the server
- Use following command to start the server:
    > gunicorn -b 127.0.0.1:5000 app:app
- Note: You need to do the nginx setup also to redirect the request to your gunicorn
  server running on 127.0.0.1:5000, so that it's accessible from outside world.

## API Docs
### Search API:  
*Specifications:*
- POST: /search
- Sample URL: http://127.0.0.1:8000/search
- Sample Request:
```json
{
    "search_keyword": "bride dress",
    "websites": [
        "ebay",
        "aliexpress"
    ],
    "page_num": 1
}
```
- All keys in above JSON are self-explanatory
- Sample Response:
```json
{
  "status": 200,
  "aspect_stats": [
    {
      "valueHistogram": [
        {
          "count": "3281",
          "_valueName": "Beading"
        },
        {
          "count": "871",
          "_valueName": "Crystal/Diamante"
        }
      ],
      "_name": "Detailing"
    }
  ],
  "total_products": 100,
  "products": [
    {
      "website": "ebay",
      "promotion_link": "https://rover.ebay.com/rover/1/711-53200-19255-0/1?campid=5338077955&customid=womensathleticapparel&toolid=10018&mpre=https://www.ebay.com/itm/Ever-Pretty-US-Lace-Half-Sleeve-White-Wedding-Dress-A-Line-Mother-Bride-Gowns-/143481451524?var=0",
      "title": "Ever-Pretty US Lace Half Sleeve White Wedding Dress A-Line Mother Of Bride Gowns",
      "price": 22.39,
      "currency": "USD",
      "thumbnail": "https://thumbs1.ebaystatic.com/pict/04040_0.jpg",
      "category_name": "Dresses"
    },
    {
      "website": "aliexpress",
      "promotion_link": "http://s.click.aliexpress.com/s/j3koOeFLLzRpUH0UgEhWSGVzyPRzMsB84eJel6WTHCtL0JACexsCQyiPAPIsZhLTQtsG0AK29GRT9h1xl10OVmmTMI1VvoLSChYKMmFWMMel83o9wO6LN5BY1mBELHnnLCg39xq6ZP5JHllhJ0ZrX0HFyz3TrCKywtLmNuqMPqb9VF49jg2RIhGXUVnN1lGdpcggMuLeqLUaMg996kkfRY0vzLLyjjvypiIJ3tLv6xlAiyh9FDD9cMEGSfj2LcXK7pRDgSGcAqIQdjhDedacK6id416qW9aTXB38Ejoiy31ywF3Gm6ZmDiNn0zh9QjRe1LkUo5DghX56M2DapyGeBh8X0e0A0KjNKYM2qjZdbMsGmR2qpKhaM4rp",
      "title": "Elegant Wedding <font><b>Dresses</b></font> 2020 Ever Pretty EB07833WH A-Line V-Neck Lace Appliques Formal <font><b>Dresses</b></font> For <font><b>Bride</b></font> Tulle Mariage Gelinlik",
      "price": 30.99,
      "currency": "USD",
      "thumbnail": "https://ae01.alicdn.com/kf/HTB1Ek4dV9zqK1RjSZFHq6z3CpXaE/Elegant-Wedding-font-b-Dresses-b-font-2020-Ever-Pretty-EB07833WH-A-Line-V-Neck-Lace.jpg_350x350.jpg",
      "category_name": "Weddings & Events"
    }
  ],
  "category_stats": [
    {
      "count": "87942",
      "childCategoryHistogram": [
        {
          "count": "64752",
          "categoryId": "260033",
          "categoryName": "Specialty"
        }
      ],
      "categoryId": "11450",
      "categoryName": "Clothing, Shoes & Accessories"
    }
  ],
  "timeout_error_sites": []
}
```
- Major fields in the Response are:  
    - products: contains the list of products matching the given keyword.  
    - aspect_stats: This contains the specification of the products along with their count.
    - category_stats: This contains the product categories along with their counts.
    - timeout_error_sites: This contains the list of sites which were not able to produce output in give time frame.
