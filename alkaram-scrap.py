from turtle import color
from numpy import size
import requests
import pandas as pd
from bs4 import BeautifulSoup


website = "https://www.alkaramstudio.com/men/ready-to-wear/shalwar-kameez?_=1650863260179&is_ajax=1&p="
response = requests.get(website)
print(response.status_code)

soup = BeautifulSoup(response.content, "html.parser")
results = soup.find_all("div", {"class": "product-item-info"})

print(results)

product_name = []
product_price = []
product_color = []
product_size = []
product_code = []
product_detail = []
product_url = []


for i in range(1, 3):
    # website in variable
    website = (
        "https://www.alkaramstudio.com/men/ready-to-wear/shalwar-kameez?_=1650863260179&is_ajax=1&p="
        + str(i)
    )

    # request
    response = requests.get(website)

    # soup object
    soup = BeautifulSoup(response.content, "html.parser")

    # results
    results = soup.find_all("div", {"class": "product-item-info"})

    # print(len(results))

    for result in results:
        # name
        try:
            names = (
                result.find("a", {"class": "product-item-link"})
                .attrs["href"]
                .rsplit("-", 1)[0]
                .split("/")[3]
            )
            pid = (
                result.find("a", {"class": "product-item-link"})
                .attrs["href"]
                .rsplit("-", 1)[1]
            )
            url = f"https://www.alkaramstudio.com/{names}-{pid}"
            # print(url)
            responses = requests.get(url)

            # soup object
            soups = BeautifulSoup(responses.content, "html.parser")

            # results
            resultss = soups.find_all("div", {"class": "product-info-main"})

            for rel in resultss:
                print(url)
                # product_url.append(url)
                name = rel.find("span", class_="h1").text.strip()
                price = rel.find("span", class_="price").text.strip()
                color = (
                    rel.find("div", class_="product-sku")
                    .text.strip()
                    .split(" " and "-")[1]
                )
                size = "XS S M L XL"
                product_cod = (
                    rel.find("div", class_="product-sku")
                    .text.strip()
                    .rsplit(" ")[2]
                    .split("-")[0]
                )
                product_det = rel.find("ul", class_="links toggle_content").text.strip()

        except:
            pass
        product_url.append(url)
        product_name.append(name)
        product_price.append(price)
        product_color.append(color)
        product_size.append(size)
        product_code.append(product_cod)
        product_detail.append(product_det)


product_overview = pd.DataFrame(
    {
        "Link": product_url,
        "Name": product_name,
        "Price": product_price,
        "Color": product_color,
        "Size": product_size,
        "Product Code": product_code,
        "Product Details": product_detail,
    }
)
product_overview.to_excel("Men-r-to-w-shalwar-kameez.xlsx", index=False)
