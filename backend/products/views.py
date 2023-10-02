import requests
from bs4 import BeautifulSoup
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.models import Product  # Import your Product model


from .models import Product


@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)




@api_view(['POST'])
def scrape_and_add_product_ulta(request):
    try:
        if "url" not in request.data:
            return Response({"message": "URL is missing in the request data."}, status=400)

        URL = request.data.get("url")

        if not URL:
            return Response({"message": "URL is empty."}, status=400)

        # Initialize an empty list to store product information
        product_info = []

        # Loop through the product pages (assuming there are 46 pages)
        for page_number in range(1, 47):
            page_url = f"{URL}&page={page_number}"

            # Send an HTTP GET request to the page
            response = requests.get(page_url)

            # Check if the request was successful
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find all product elements on the page
                product_elements = soup.find_all("li", class_="ProductListingResults__productCard")

                for product_item in product_elements:
                    product_dict = {}

                    # Extract product name
                    product_name_element = product_item.find("span", class_="ProductCard__product")
                    if product_name_element:
                        product_name = product_name_element.get_text(strip=True)
                        product_dict["ProductName"] = product_name

                        # Check if a product with the same name already exists in the database
                        existing_product = Product.objects.filter(product_name=product_name).first()

                        if not existing_product:
                            # Add the "store" field to the product_dict
                            product_dict["Store"] = "ulta"

                            # Extract product link
                            product_link_element = product_item.find("a", class_="Link_Huge--secondary")
                            if product_link_element:
                                product_link = product_link_element['href']
                                product_dict["ProductLink"] = product_link

                            # Extract product brand
                            product_brand_element = product_item.find("span", class_="ProductCard__brand")
                            if product_brand_element:
                                product_brand = product_brand_element.get_text(strip=True)
                                product_dict["ProductBrand"] = product_brand

                            # Extract product rating if available
                            product_rating_element = product_item.find("div", class_="ReviewStarsCard")
                            if product_rating_element:
                                product_rating = product_rating_element.find("span", class_="sr-only").get_text(strip=True)
                                product_dict["ProductRating"] = product_rating

                            # Extract product reviews if available
                            product_reviews_element = product_item.find("span", class_="Text-ds--body-3")
                            if product_reviews_element:
                                product_reviews = product_reviews_element.get_text(strip=True)
                                product_dict["ProductReviews"] = product_reviews

                            # Extract product price
                            product_price_element = product_item.find("span", class_="Text-ds--black")
                            if product_price_element:
                                product_price = product_price_element.get_text(strip=True)
                                product_dict["ProductPrice"] = product_price

                            # Extract product image URL
                            product_image_element = product_item.find("div", class_="ProductCard__image").find("img")
                            if product_image_element:
                                product_image_url = product_image_element['src']
                                product_dict["ProductImageURL"] = product_image_url

                                
                            # Create a new Product object and save it to the database
                            new_product = Product(**product_dict)
                            new_product.save()

                            # Append the product information to the list
                            product_info.append(product_dict)

            else:
                return Response({"message": f"Failed to retrieve page {page_number}.", "products": product_info}, status=500)

        return Response({"products": product_info})

    except Exception as e:
        return Response({"message": f"An error occurred: {str(e)}", "products": product_info}, status=500)
    




@api_view(['POST'])
def scrape_and_add_product_buymebeauty(request):
    try:
        if "url" not in request.data:
            return Response({"message": "URL is missing in the request data."}, status=400)

        URL = request.data.get("url")

        if not URL:
            return Response({"message": "URL is empty."}, status=400)

        # Initialize an empty list to store product information
        product_info = []
        
        # Loop through the product pages (assuming there are 4 pages for demonstration)
        for page_number in range(1, 5):
            page_url = f"{URL}?currentPage={page_number}"
            # Send an HTTP GET request to the page
            print(page_url)
            
            # Set headers to mimic a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
            
            response = requests.get(page_url, headers=headers, timeout=10)
            print(response)
            
            # Check if the request was successful
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                print(soup)
                
                # Find all product elements on the page
                product_elements = soup.find_all("li", class_="product")
                
                for product_item in product_elements:
                    product_dict = {}
                    
                    # Extract product name
                    product_name_element = product_item.find("h3", class_="card-title")
                    if product_name_element:
                        product_name = product_name_element.find("a").text.strip()
                        product_dict["Product Name"] = product_name

                        # Check if a product with the same name already exists in the database
                        existing_product = Product.objects.filter(ProductName=product_name).first()

                        if not existing_product:
                            # Add the "store" field to the product_dict
                            product_dict["Store"] = "Buy Me Beauty"

                            # Extract product link
                            product_link_element = product_name_element.find("a")
                            if product_link_element:
                                product_link = product_link_element['href']
                                product_dict["Product Link"] = product_link

                            # Extract product rating if available
                            product_rating = product_item.find("span", class_="stamped-product-reviews-badge")
                            if product_rating:
                                product_rating = product_rating.text.strip()
                                product_dict["Product Rating"] = product_rating

                            # Extract product price
                            product_price = product_item.find("span", class_="price--main").text.strip()
                            product_dict["Product Price"] = product_price

                            # Extract product image URL
                            product_image_element = product_item.find("img", class_="card-image")
                            if product_image_element:
                                product_image_url = product_image_element['data-srcset'].split()[-2]
                                product_dict["Product Image URL"] = product_image_url

                            # Create a new Product object and save it to the database
                            # new_product = Product(**product_dict)
                            # new_product.save()

                            # Append the product information to the list
                            product_info.append(product_dict)

            else:
                return Response({"message": f"Failed to retrieve page {page_number}.", "products": product_info}, status=500)

        return Response({"products": product_info})

    except Exception as e:
        return Response({"message": f"An error occurred: {str(e)}", "products": product_info}, status=500)
    


@api_view(['POST'])
def scrape_and_add_product_clinique(request):
    try:
        if "url" not in request.data:
            return Response({"message": "URL is missing in the request data."}, status=400)

        URL = request.data.get("url")

        if not URL:
            return Response({"message": "URL is empty."}, status=400)

        # Initialize an empty list to store product information
        product_info = []

        # Send an HTTP GET request to the page
        print(f"Scraping URL: {URL}")

        # Set headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        response = requests.get(URL, headers=headers, timeout=10)
        print(response)

        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup)

            # Find all product elements on the page
            product_elements = soup.find_all("li", class_="swiper-slide")

            for product_item in product_elements:
                product_dict = {}

                # Extract product name
                product_name_element = product_item.find("h2", class_="mt-2.5")
                if product_name_element:
                    product_name = product_name_element.text.strip()
                    product_dict["Product Name"] = product_name

                    # Check if a product with the same name already exists in the database
                    existing_product = Product.objects.filter(ProductName=product_name).first()

                    if not existing_product:
                        # Add the "store" field to the product_dict
                        product_dict["Store"] = "Clinique"

                        # Extract product link
                        product_link_element = product_item.find("a", href=True)
                        if product_link_element:
                            product_link = product_link_element['href']
                            product_dict["Product Link"] = product_link

                        # Extract product rating if available
                        product_rating_element = product_item.find("div", class_="star-ratings")
                        if product_rating_element:
                            product_rating = product_rating_element['style'].split(':')[-1]
                            product_dict["Product Rating"] = product_rating

                        # Extract product price
                        product_price_element = product_item.find("span", data_product_target="price")
                        if product_price_element:
                            product_price = product_price_element.text.strip()
                            product_dict["Product Price"] = product_price

                        # Extract product image URL
                        product_image_element = product_item.find("img", data_action="error->image-error#mainImageError")
                        if product_image_element:
                            product_image_url = product_image_element['src']
                            product_dict["Product Image URL"] = product_image_url

                        # Create a new Product object and save it to the database
                        # new_product = Product(**product_dict)
                        # new_product.save()

                        # Append the product information to the list
                        product_info.append(product_dict)

        else:
            return Response({"message": f"Failed to retrieve the page.", "products": product_info}, status=500)

        return Response({"products": product_info})

    except Exception as e:
        return Response({"message": f"An error occurred: {str(e)}", "products": product_info}, status=500)


def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return Response({"message": "Product deleted!"})
