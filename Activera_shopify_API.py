{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "oYphYddU4tMS",
    "jp-MarkdownHeadingCollapsed": true
   },
   "source": [
    "# **Data Representation and Design (BAX 422)**\n",
    "\n",
    "### **Code Submission**\n",
    "\n",
    "### **Team:** ***Priyanka Iyer*** and ***Karishma Mehta***\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "t9b2dEBq8xbT"
   },
   "source": [
    "# **Activera: Optimizing E-commerce Operations with Shopify API**\n",
    "\n",
    "For this project, we created our own store on Shopify called Activera which is an e-retail business selling affordable and high quality women’s activewear clothing.\n",
    "\n",
    "The three problems that are being solved:\n",
    "1. **Real-Time Inventory Management:** Preventing running out of products or accidentally selling more than available by keeping the inventory updated in real time.\n",
    "2. **Product Information Synchronization:** Making sure product details like descriptions, prices, sizes and images are always accurate across the store.\n",
    "3. **Order Tracking and Fulfillment:** Giving customers live updates on their orders, from the time of purchase to delivery, for seamless order tracking.\n",
    "\n",
    "To showcase this we have used various libraries and created functions to bring ease of access in product information and tracking.\n",
    "\n",
    "Because Shopify is a complex platform, the store has to give permissions for making changes through Admin API like read and write products, inventory, tracking, orders, etc."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "4RbPuMn4QJtz",
    "outputId": "0fad2b4d-4372-4cec-cda7-dad4c3ebe8f9"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: shopifyapi in /opt/anaconda3/lib/python3.12/site-packages (12.7.0)\n",
      "Requirement already satisfied: pyactiveresource>=2.2.2 in /opt/anaconda3/lib/python3.12/site-packages (from shopifyapi) (2.2.2)\n",
      "Requirement already satisfied: PyJWT>=2.0.0 in /opt/anaconda3/lib/python3.12/site-packages (from shopifyapi) (2.8.0)\n",
      "Requirement already satisfied: PyYAML>=6.0.1 in /opt/anaconda3/lib/python3.12/site-packages (from shopifyapi) (6.0.1)\n",
      "Requirement already satisfied: six in /opt/anaconda3/lib/python3.12/site-packages (from shopifyapi) (1.16.0)\n"
     ]
    }
   ],
   "source": [
    "!pip install --upgrade shopifyapi\n",
    "import shopify\n",
    "import time\n",
    "import requests\n",
    "import json\n",
    "from functools import lru_cache\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "id": "qttYvfSHQOfA"
   },
   "outputs": [],
   "source": [
    "# The credentials of our Shopify Store\n",
    "SHOPIFY_STORE_URL = \"a1rrg1-y3.myshopify.com\"\n",
    "API_ACCESS_TOKEN = \"put_token_hered\"\n",
    "API_VERSION = \"2025-01\"\n",
    "\n",
    "# Setting up the Shopify session\n",
    "shop_url = f\"https://{SHOPIFY_STORE_URL}/admin/api/{API_VERSION}\"\n",
    "shopify.Session.setup(api_key=\"a1f9d38f81cdbd7b3a7cabc02f8e1f44\", secret=\"3b8ccfd559f479ced6e4edd0090b8ee4\")\n",
    "session = shopify.Session(shop_url, API_VERSION, API_ACCESS_TOKEN)\n",
    "shopify.ShopifyResource.activate_session(session)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "pPhtCp4w6Led"
   },
   "source": [
    "Using APIs we created new products in Shopify which directly gets added in the inventory, implementing the GraphQL Admin API and following the documentation. GraphQL constructs endpoint needed to send API requests."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "QZJRuaY15oz0",
    "outputId": "8699a41b-0236-42f9-ca84-d40ff46f1b1b"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✅ Product Created Successfully! Product ID: gid://shopify/Product/8909418561794\n"
     ]
    }
   ],
   "source": [
    "GRAPHQL_URL = f\"https://{SHOPIFY_STORE_URL}/admin/api/{API_VERSION}/graphql.json\"\n",
    "\n",
    "\n",
    "headers = {\n",
    "    \"Content-Type\": \"application/json\",\n",
    "    \"X-Shopify-Access-Token\": API_ACCESS_TOKEN\n",
    "}\n",
    "\n",
    "# Creating new product using GraphQL mutation\n",
    "create_product_query = \"\"\"\n",
    "mutation {\n",
    "  productCreate(input: {\n",
    "    title: \"FLURRY HALF ZIP MOCK NECK TOP\",\n",
    "    productType: \"Tops\",\n",
    "    status: ACTIVE\n",
    "  }) {\n",
    "    product {\n",
    "      id\n",
    "      title\n",
    "    }\n",
    "    userErrors {\n",
    "      field\n",
    "      message\n",
    "    }\n",
    "  }\n",
    "}\n",
    "\"\"\"\n",
    "\n",
    "response = requests.post(GRAPHQL_URL, headers=headers, json={\"query\": create_product_query})\n",
    "\n",
    "if response.status_code == 200:\n",
    "    data = response.json()\n",
    "    if \"errors\" in data or data[\"data\"][\"productCreate\"][\"userErrors\"]:\n",
    "        print(\"Shopify API Error:\", data)\n",
    "    else:\n",
    "        product_id = data[\"data\"][\"productCreate\"][\"product\"][\"id\"]\n",
    "        print(f\"Product Created Successfully! Product ID: {product_id}\")\n",
    "else:\n",
    "    print(f\"API Request Failed: {response.status_code}, {response.text}\")\n",
    "\n",
    "# status code 200 means it is sucessful and will parse a json response."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "W6yx-s5c62kR"
   },
   "source": [
    "# **Business Problem 1: Real-Time Inventory Management**\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Inventory Management Functions\n",
    "\n",
    "Now we created functions to handle invenotry management. Whenever there is a need to view the entire inventory or even parts of it, we may use it.\n",
    "\n",
    "The Caching function is used to return the cached result instead of making another API call"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {
    "id": "-xiJkWMvZ89m"
   },
   "outputs": [],
   "source": [
    "\n",
    "@lru_cache(maxsize=50)\n",
    "def prod_id(product_title):\n",
    "    \"\"\"Get the product ID by searching for a product name/title\"\"\"\n",
    "    products = shopify.Product.find()\n",
    "    for product in products:\n",
    "        if product.title.lower() == product_title.lower():\n",
    "            return product.id\n",
    "    return None\n",
    "\n",
    "def inventory_management(product_id):\n",
    "    \"\"\"Access the inventory and check the available quantity for a product\"\"\"\n",
    "    product = shopify.Product.find(product_id)\n",
    "    inventory_data = []\n",
    "    for variant in product.variants:\n",
    "        inventory_data.append({\n",
    "            \"Product Title\": product.title,\n",
    "            \"Variant\": variant.title,\n",
    "            \"Tracking Status\": variant.inventory_management,\n",
    "            \"Available Quantity\": variant.inventory_quantity\n",
    "        })\n",
    "        time.sleep(1)\n",
    "    return pd.DataFrame(inventory_data)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "nR9roJrHbh8V",
    "outputId": "a0e9f6b7-bd61-4850-c167-b90d98d0a67d"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "INVENTORY MANAGEMENT\n"
     ]
    },
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "Enter a Product Name:  Momentum Seamless Tee\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Inventory Status for Momentum Seamless Tee\n",
      "            Product Title          Variant Tracking Status  Available Quantity\n",
      "0   Momentum Seamless Tee       Gray / 2XL         shopify                   3\n",
      "1   Momentum Seamless Tee        Gray / XL         shopify                   3\n",
      "2   Momentum Seamless Tee         Gray / L         shopify                   3\n",
      "3   Momentum Seamless Tee         Gray / M         shopify                   2\n",
      "4   Momentum Seamless Tee         Gray / S         shopify                   2\n",
      "5   Momentum Seamless Tee        Gray / XS         shopify                   2\n",
      "6   Momentum Seamless Tee       Gray / 2XS         shopify                   2\n",
      "7   Momentum Seamless Tee      Green / 2XL         shopify                   2\n",
      "8   Momentum Seamless Tee       Green / XL         shopify                   2\n",
      "9   Momentum Seamless Tee        Green / L         shopify                   3\n",
      "10  Momentum Seamless Tee        Green / M         shopify                   3\n",
      "11  Momentum Seamless Tee        Green / S         shopify                   3\n",
      "12  Momentum Seamless Tee       Green / XS         shopify                   2\n",
      "13  Momentum Seamless Tee      Green / 2XS         shopify                   2\n",
      "14  Momentum Seamless Tee  Rose gold / 2XL         shopify                   3\n",
      "15  Momentum Seamless Tee   Rose gold / XL         shopify                   3\n",
      "16  Momentum Seamless Tee    Rose gold / L         shopify                   3\n",
      "17  Momentum Seamless Tee    Rose gold / M         shopify                   3\n",
      "18  Momentum Seamless Tee    Rose gold / S         shopify                   2\n",
      "19  Momentum Seamless Tee   Rose gold / XS         shopify                   2\n",
      "20  Momentum Seamless Tee  Rose gold / 2XS         shopify                   2\n",
      "21  Momentum Seamless Tee      Brown / 2XL         shopify                   3\n",
      "22  Momentum Seamless Tee       Brown / XL         shopify                   3\n",
      "23  Momentum Seamless Tee        Brown / L         shopify                   2\n",
      "24  Momentum Seamless Tee        Brown / M         shopify                   2\n",
      "25  Momentum Seamless Tee        Brown / S         shopify                   3\n",
      "26  Momentum Seamless Tee       Brown / XS         shopify                   3\n",
      "27  Momentum Seamless Tee      Brown / 2XS         shopify                   2\n",
      "28  Momentum Seamless Tee      Black / 2XL         shopify                   2\n",
      "29  Momentum Seamless Tee       Black / XL         shopify                   2\n",
      "30  Momentum Seamless Tee        Black / L         shopify                   2\n",
      "31  Momentum Seamless Tee        Black / M         shopify                   3\n",
      "32  Momentum Seamless Tee        Black / S         shopify                   1\n",
      "33  Momentum Seamless Tee       Black / XS         shopify                   3\n",
      "34  Momentum Seamless Tee      Black / 2XS         shopify                   2\n"
     ]
    }
   ],
   "source": [
    "# Call the Inventory Management Function\n",
    "\n",
    "print(\"INVENTORY MANAGEMENT\")\n",
    "product_title = input(\"Enter a Product Name: \")\n",
    "product_id = prod_id(product_title)\n",
    "if product_id:\n",
    "    print(f\"Inventory Status for {product_title}\")\n",
    "    inventory_df = inventory_management(product_id)\n",
    "    print(inventory_df)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "A9EqCha97Ubt"
   },
   "source": [
    "# **Business Problem 2: Product Information Synchronization**\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Product Search Functions.\n",
    "\n",
    "Here we have created functions to get the details of all products in the store and then to search for a particular product by its product name."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {
    "id": "k70toETDhY8k"
   },
   "outputs": [],
   "source": [
    "\n",
    "def all_products():\n",
    "    \"\"\"Get all the products in the store and their details\"\"\"\n",
    "    products = shopify.Product.find()\n",
    "    product_list = []\n",
    "    for product in products:\n",
    "        sizes = set()\n",
    "        colors = set()\n",
    "        for variant in product.variants:\n",
    "            if variant.option1 and variant.option1.lower() != \"default title\":\n",
    "                colors.add(variant.option1)\n",
    "            if variant.option2 and variant.option2.lower() != \"default title\":\n",
    "                sizes.add(variant.option2)\n",
    "        product_list.append({\n",
    "            \"Product ID\": product.id,\n",
    "            \"Title\": product.title,\n",
    "            \"Price\": product.variants[0].price,\n",
    "            \"Colors\": list(colors),\n",
    "            \"Sizes\": list(sizes)\n",
    "        })\n",
    "        time.sleep(1.5)\n",
    "    return product_list\n",
    "\n",
    "def product_search(product_name):\n",
    "    \"\"\"Search for products by name (partial match included) and return in the form of a dataframe\"\"\"\n",
    "    products = all_products()\n",
    "    matching_products = [product for product in products if product_name.lower() in product[\"Title\"].lower()]\n",
    "    return pd.DataFrame(matching_products) if matching_products else None\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {
    "id": "SHpx1CKJhpnH"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "PRODUCT SEARCH\n"
     ]
    },
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "Enter Product Name to search for:  Momentum Seamless Tee\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Product Search Results:\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Product ID</th>\n",
       "      <th>Title</th>\n",
       "      <th>Price</th>\n",
       "      <th>Colors</th>\n",
       "      <th>Sizes</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>8906773135618</td>\n",
       "      <td>Momentum Seamless Tee</td>\n",
       "      <td>39.00</td>\n",
       "      <td>[Green, Gray, Black, Brown, Rose gold]</td>\n",
       "      <td>[L, 2XL, M, XS, S, XL, 2XS]</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "      Product ID                  Title  Price  \\\n",
       "0  8906773135618  Momentum Seamless Tee  39.00   \n",
       "\n",
       "                                   Colors                        Sizes  \n",
       "0  [Green, Gray, Black, Brown, Rose gold]  [L, 2XL, M, XS, S, XL, 2XS]  "
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# Call the Product Search Function\n",
    "print(\"PRODUCT SEARCH\")\n",
    "product_name = input(\"Enter Product Name to search for: \").strip()\n",
    "product_results = product_search(product_name)\n",
    "if product_results is not None:\n",
    "    print(\"Product Search Results:\")\n",
    "    display(product_results)\n",
    "else:\n",
    "    print(\"Sorry! This product does not exist :(\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "azrzUOmT9XaE"
   },
   "source": [
    "# **Business Problem 3: Order Tracking and Fulfillment**\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Order Tracking Function\n",
    "\n",
    "Here we have created functions to get the details of all orders placed and then to search for a particular order by the name of the customer who placed that order. \n",
    "\n",
    "The order status (Fulfilled/Unfulfilled) is also displayed.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 59,
   "metadata": {
    "id": "r0kghAf60Iim"
   },
   "outputs": [],
   "source": [
    "def all_orders():\n",
    "    \"\"\"Get all the orders placed and their details\"\"\"\n",
    "    orders = shopify.Order.find()\n",
    "    order_list = []\n",
    "    for order in orders:\n",
    "        fulfillment_status = \"Fulfilled\" if order.fulfillment_status == \"fulfilled\" else \"Unfulfilled\"\n",
    "        order_list.append({\n",
    "            \"Order ID\": order.id,\n",
    "            \"Customer First Name\": order.customer.first_name if order.customer else \"Guest\",\n",
    "            \"Customer Last Name\": order.customer.last_name if order.customer else \"\",\n",
    "            \"Total Price\": order.total_price,\n",
    "            \"Status\": order.financial_status,\n",
    "            \"Fulfillment Status\": fulfillment_status,\n",
    "            \"Created At\": order.created_at\n",
    "        })\n",
    "        time.sleep(1)\n",
    "    return order_list\n",
    "\n",
    "def order_search_bycustomer(customer_name):\n",
    "    \"\"\"Search for order by the name of the customer that placed the order (partial match included) and return in the form of a dataframe\"\"\"\n",
    "    orders = all_orders()\n",
    "    matching_orders = [\n",
    "        order for order in orders\n",
    "        if customer_name.lower() in (f\"{order['Customer First Name']} {order['Customer Last Name']}\".strip().lower() if order[\"Customer First Name\"] else \"\")\n",
    "    ]\n",
    "    return pd.DataFrame(matching_orders) if matching_orders else None"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 60,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 125
    },
    "id": "LlSqV3DX0TKN",
    "outputId": "c8fcb02f-86d6-4b6e-9d61-8f398c3d042b"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Enter Customer Name to Search Orders: Harry\n",
      "Order Search Results:\n"
     ]
    },
    {
     "data": {
      "application/vnd.google.colaboratory.intrinsic+json": {
       "summary": "{\n  \"name\": \"order_results\",\n  \"rows\": 1,\n  \"fields\": [\n    {\n      \"column\": \"Order ID\",\n      \"properties\": {\n        \"dtype\": \"number\",\n        \"std\": null,\n        \"min\": 6191670034690,\n        \"max\": 6191670034690,\n        \"num_unique_values\": 1,\n        \"samples\": [\n          6191670034690\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"Customer First Name\",\n      \"properties\": {\n        \"dtype\": \"string\",\n        \"num_unique_values\": 1,\n        \"samples\": [\n          \"Harry\"\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"Customer Last Name\",\n      \"properties\": {\n        \"dtype\": \"string\",\n        \"num_unique_values\": 1,\n        \"samples\": [\n          \"Smith\"\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"Total Price\",\n      \"properties\": {\n        \"dtype\": \"string\",\n        \"num_unique_values\": 1,\n        \"samples\": [\n          \"45.99\"\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"Status\",\n      \"properties\": {\n        \"dtype\": \"string\",\n        \"num_unique_values\": 1,\n        \"samples\": [\n          \"paid\"\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"Fulfillment Status\",\n      \"properties\": {\n        \"dtype\": \"string\",\n        \"num_unique_values\": 1,\n        \"samples\": [\n          \"Unfulfilled\"\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"Created At\",\n      \"properties\": {\n        \"dtype\": \"object\",\n        \"num_unique_values\": 1,\n        \"samples\": [\n          \"2025-02-04T11:19:18-08:00\"\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    }\n  ]\n}",
       "type": "dataframe",
       "variable_name": "order_results"
      },
      "text/html": [
       "\n",
       "  <div id=\"df-f3f4a459-e6a5-4912-89fc-e55b225ebd43\" class=\"colab-df-container\">\n",
       "    <div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Order ID</th>\n",
       "      <th>Customer First Name</th>\n",
       "      <th>Customer Last Name</th>\n",
       "      <th>Total Price</th>\n",
       "      <th>Status</th>\n",
       "      <th>Fulfillment Status</th>\n",
       "      <th>Created At</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>6191670034690</td>\n",
       "      <td>Harry</td>\n",
       "      <td>Smith</td>\n",
       "      <td>45.99</td>\n",
       "      <td>paid</td>\n",
       "      <td>Unfulfilled</td>\n",
       "      <td>2025-02-04T11:19:18-08:00</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>\n",
       "    <div class=\"colab-df-buttons\">\n",
       "\n",
       "  <div class=\"colab-df-container\">\n",
       "    <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-f3f4a459-e6a5-4912-89fc-e55b225ebd43')\"\n",
       "            title=\"Convert this dataframe to an interactive table.\"\n",
       "            style=\"display:none;\">\n",
       "\n",
       "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\" viewBox=\"0 -960 960 960\">\n",
       "    <path d=\"M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z\"/>\n",
       "  </svg>\n",
       "    </button>\n",
       "\n",
       "  <style>\n",
       "    .colab-df-container {\n",
       "      display:flex;\n",
       "      gap: 12px;\n",
       "    }\n",
       "\n",
       "    .colab-df-convert {\n",
       "      background-color: #E8F0FE;\n",
       "      border: none;\n",
       "      border-radius: 50%;\n",
       "      cursor: pointer;\n",
       "      display: none;\n",
       "      fill: #1967D2;\n",
       "      height: 32px;\n",
       "      padding: 0 0 0 0;\n",
       "      width: 32px;\n",
       "    }\n",
       "\n",
       "    .colab-df-convert:hover {\n",
       "      background-color: #E2EBFA;\n",
       "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
       "      fill: #174EA6;\n",
       "    }\n",
       "\n",
       "    .colab-df-buttons div {\n",
       "      margin-bottom: 4px;\n",
       "    }\n",
       "\n",
       "    [theme=dark] .colab-df-convert {\n",
       "      background-color: #3B4455;\n",
       "      fill: #D2E3FC;\n",
       "    }\n",
       "\n",
       "    [theme=dark] .colab-df-convert:hover {\n",
       "      background-color: #434B5C;\n",
       "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
       "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
       "      fill: #FFFFFF;\n",
       "    }\n",
       "  </style>\n",
       "\n",
       "    <script>\n",
       "      const buttonEl =\n",
       "        document.querySelector('#df-f3f4a459-e6a5-4912-89fc-e55b225ebd43 button.colab-df-convert');\n",
       "      buttonEl.style.display =\n",
       "        google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
       "\n",
       "      async function convertToInteractive(key) {\n",
       "        const element = document.querySelector('#df-f3f4a459-e6a5-4912-89fc-e55b225ebd43');\n",
       "        const dataTable =\n",
       "          await google.colab.kernel.invokeFunction('convertToInteractive',\n",
       "                                                    [key], {});\n",
       "        if (!dataTable) return;\n",
       "\n",
       "        const docLinkHtml = 'Like what you see? Visit the ' +\n",
       "          '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
       "          + ' to learn more about interactive tables.';\n",
       "        element.innerHTML = '';\n",
       "        dataTable['output_type'] = 'display_data';\n",
       "        await google.colab.output.renderOutput(dataTable, element);\n",
       "        const docLink = document.createElement('div');\n",
       "        docLink.innerHTML = docLinkHtml;\n",
       "        element.appendChild(docLink);\n",
       "      }\n",
       "    </script>\n",
       "  </div>\n",
       "\n",
       "\n",
       "  <div id=\"id_c032cb24-4854-463b-886f-ed3cfdf3b335\">\n",
       "    <style>\n",
       "      .colab-df-generate {\n",
       "        background-color: #E8F0FE;\n",
       "        border: none;\n",
       "        border-radius: 50%;\n",
       "        cursor: pointer;\n",
       "        display: none;\n",
       "        fill: #1967D2;\n",
       "        height: 32px;\n",
       "        padding: 0 0 0 0;\n",
       "        width: 32px;\n",
       "      }\n",
       "\n",
       "      .colab-df-generate:hover {\n",
       "        background-color: #E2EBFA;\n",
       "        box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
       "        fill: #174EA6;\n",
       "      }\n",
       "\n",
       "      [theme=dark] .colab-df-generate {\n",
       "        background-color: #3B4455;\n",
       "        fill: #D2E3FC;\n",
       "      }\n",
       "\n",
       "      [theme=dark] .colab-df-generate:hover {\n",
       "        background-color: #434B5C;\n",
       "        box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
       "        filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
       "        fill: #FFFFFF;\n",
       "      }\n",
       "    </style>\n",
       "    <button class=\"colab-df-generate\" onclick=\"generateWithVariable('order_results')\"\n",
       "            title=\"Generate code using this dataframe.\"\n",
       "            style=\"display:none;\">\n",
       "\n",
       "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
       "       width=\"24px\">\n",
       "    <path d=\"M7,19H8.4L18.45,9,17,7.55,7,17.6ZM5,21V16.75L18.45,3.32a2,2,0,0,1,2.83,0l1.4,1.43a1.91,1.91,0,0,1,.58,1.4,1.91,1.91,0,0,1-.58,1.4L9.25,21ZM18.45,9,17,7.55Zm-12,3A5.31,5.31,0,0,0,4.9,8.1,5.31,5.31,0,0,0,1,6.5,5.31,5.31,0,0,0,4.9,4.9,5.31,5.31,0,0,0,6.5,1,5.31,5.31,0,0,0,8.1,4.9,5.31,5.31,0,0,0,12,6.5,5.46,5.46,0,0,0,6.5,12Z\"/>\n",
       "  </svg>\n",
       "    </button>\n",
       "    <script>\n",
       "      (() => {\n",
       "      const buttonEl =\n",
       "        document.querySelector('#id_c032cb24-4854-463b-886f-ed3cfdf3b335 button.colab-df-generate');\n",
       "      buttonEl.style.display =\n",
       "        google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
       "\n",
       "      buttonEl.onclick = () => {\n",
       "        google.colab.notebook.generateWithVariable('order_results');\n",
       "      }\n",
       "      })();\n",
       "    </script>\n",
       "  </div>\n",
       "\n",
       "    </div>\n",
       "  </div>\n"
      ],
      "text/plain": [
       "        Order ID Customer First Name Customer Last Name Total Price Status  \\\n",
       "0  6191670034690               Harry              Smith       45.99   paid   \n",
       "\n",
       "  Fulfillment Status                 Created At  \n",
       "0        Unfulfilled  2025-02-04T11:19:18-08:00  "
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# Call the Order Track Function\n",
    "customer_name = input(\"Enter the name of the Customer who placed the order: \").strip()\n",
    "order_results = order_search_bycustomer(customer_name)\n",
    "if order_results is not None:\n",
    "    print(\"Order Search Results:\")\n",
    "    display(order_results)\n",
    "else:\n",
    "    print(\"Sorry! We could not find such an order :(\")\n",
    "\n",
    "shopify.ShopifyResource.clear_session()\n"
   ]
  }
 ],
 "metadata": {
  "colab": {
   "provenance": []
  },
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
