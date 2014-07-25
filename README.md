#Iceberg Python API

[![Build Status](https://travis-ci.org/Iceberg-Marketplace/Iceberg-API-PYTHON.png)](https://travis-ci.orgIceberg-Marketplace/Iceberg-API-PYTHON) [![Coverage Status](https://coveralls.io/repos/Iceberg-Marketplace/Iceberg-API-PYTHON/badge.png)](https://coveralls.io/r/Iceberg-Marketplace/Iceberg-API-PYTHON)


The Iceberg API provides an entire set of functions and classes to access and edit Iceberg data.

Table of Content
-------------
**Get started**

1. [Setup](#setup)
2. [Resources](#resources)
3. [Methods](#methods)
4. [ProductOffer](#productoffer)
5. [Products](#products)
6. [Cart](#cart)
7. [Orders](#orders)




Setup
-------------

### Env variables

As you may have seen in the conf.py file, 2 environment variables are needed to use the Iceberg python API: the Iceberg secret key and the application namespace. These variables must be initiated as environment variables.

```python

export ICEBERG_APPLICATION_NAMESPACE=my_app
export ICEBERG_APPLICATION_SECRET_KEY=XXXXXX

```

### Log in 

* There are two ways to log in:
 * By calling the <code>sso()</code> method on the **IcebergAPI()** class, and passing 3 parameters wich are the user mail, first name and last name.
 * By passing directly two parameters in the **IcebergAPI()** class wich are the access token and the username

```python
api_handler = IcebergAPI().sso("userEmail","userFirstName","userLastName")
```
```python
api_handler = IcebergAPI(access_token=XXXX, username=XXXX)
```

Resources
-------------

 * You have access to the following resources directly through the main **IcebergAPI()** object:
     * ProductVariation
     * ProductOffer
     * Product
     * MerchantOrder
     * Order
     * Application
     * Store
     * User
     * Profile
     * Cart
     * Country
     * Address
     * Payment

For example:
```python
api_handler.User()
api_handler.ProductOffer()
```

Methods
-------------

 * Methods are functions allowing you to access and manipulate the resources, the one we are going to use:
     * <code>find()</code> allows you to fetch a specific element within a list of elements, it can be product offers, products, orders.
     * <code>save()</code> allows you to update data about a store, offer, product etc... that has been modified.
     * <code>search()</code> returns a tuple, the first variable contains elements matching the requested parameter, the parameter can be a proprety like price, color, variation etc... the second returned variable contains info about the provided list.
     * <code>to_JSON()</code> returns a JSON serialized string containing the entirety of an object.

For example:
```python
api_handler.ProductOffer.find("52")
api_handler.ProductOffer.find("52").to_JSON()
api_handler.ProductOffer.find("52").save()
```

ProductOffer
-------------

Offers differs from products, a product can not be added to a cart, the product is the physical object defined by its brand, model, colors etc ... When someone by a product on a marketplace, he actually orders an offer linked to a product from a specific merchant.<br>
We are here going to deal with offers, or more accurately **productOffers**.

### Get productOffer

In order to fetch a **productOffer**, we need to call the <code>find()</code> method on the **ProductOffer** class, and passing the id of the requested product. Once we've got it, let's print some infos.


```python

offer = api_handler.ProductOffer.find("52")

print offer.default_image_url
print offer.description

for variation in offer.variations:
    print "%s items available in size %s, %s euros" %(variation['stock'],variation['name'],variation['price'])

```

### Edit productOffer

To edit an offer, you must be logged as a staff user. Simply fetch the object using the <code>find()</code> method again, then edit the product's attributes you want to change. And finally call the <code>save()</code> method upon your offer object.


```python

    offer = api_handler.ProductOffer.find("52")

    offer.previous_price ="40.00"
    offer.default_image_url ="myimage.png"

    offer.save()
```

Products
-------------

### Search for a range of products

Not every proprety of **Product** or **ProductOffer** can be scanned with the <code>search()</code> method, but a lot can be, like name, gender, made_in, description etc...<br>
Let's look for every product wich name's contains the string "Robe". The meta variable contains info about the returned list.
```python
products, meta = api_handler.Product.search({"name__icontains": "Robe"})

print meta
for product in products:
    print product.to_JSON()
```


Cart
-------------

Even when they are offline, users have a cart empty or containing offers awaiting to be validated or canceled. We can manipulate a user's cart easily.

### Get infos of a user's cart

Retrieve the current logged in user's cart by calling the <code>mine()</code> method within the class **Cart**.

```python

user_cart = api_handler.Cart.mine()

print user_cart.shipping_address
print user_cart.shipping_amount
print user_cart.total_amount
    
```

### Add product to cart

Edit a user's cart by adding an offer, and then print the amount of the updated cart for example.

```python

user_cart = api_handler.Cart.mine()

offer = api_handler.ProductOffer.find("52")

user_cart.addOffer(offer)

print api_handler.Cart.mine().total_amount
    
```

Orders
-------------

Each **Order** and **merchantOrder** are identified with a unique id.

### Get order infos

* Each order is divided into 3 parts:
    * The **Order** class contains the summary of the order: total amount, adress, shipping, and the list of merchants concerned by the order (for example, 3 products have been ordered, 2 of them belong to merchant_1 and 1 of them belongs to merchand_2).
    * The **MerchantOrder** class contains all the infos a merchant recieves when an order is made and one or more products of the order are his.(for example, merchant_1 recieves a list of 2 items)
    * The **OrderItem** class contains the product informations and size.

**Orders**, **MerchantOrder** and **OrderItems** are available in the /order section of your dashboard.
Let's display infos about the **MerchantOrder** number 6.

```python

merchant_order = api_handler.MerchantOrder.find(6)

print merchant_order.amount
print merchant_order.shipping_address.city
print merchant_order.shipping_address.country
print merchant_order.shipping_address.zipcode

```

User
-------------

### Get user infos

Using the <code>me()</code> method on the **User** class returns infos about the currently logged in user.

```python

me = api_handler.User.me()

#print me.to_JSON()
print me.username
print me.first_name
print me.last_name
print me.email
print me.timezone

```

Store
-------------

### Get store infos

Retrieve infos about a **Store** in the application. We are going to look for the store number 11 and display infos about it. This number is allocated automatically by Iceberg, you can find your stores's IDs in the GET request's response on the "merchant" section.

```python

store = api_handler.Store.find(11)

print store.name
print store.created_on
print store.long_description
print store.url

```



