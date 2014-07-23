#Iceberg Python API

Iceberg API provides an entire set of functions and class to access and edit Iceberg data.

Table of Content
-------------
**Get started**

1. [Setup](#setup)
2. [Resources](#resources)
3. [Methods](#methods)
4. [ProductOffer](#productOffer)
5. [Cart](#cart)
5. [Orders](#orders)




Setup
-------------

### Env variables

As you may have seen in the conf.py file, 2 environment variables ar needed to use the Iceberg python API: the Iceberg secret key and the application namespace. These variables must be initiated as environment variables.

```python

export ICEBERG_APPLICATION_NAMESPACE=my_app
export ICEBERG_APPLICATION_SECRET_KEY=XXXXXX

```

### Log in 

* There are two ways to log in:
 * By calling the sso function in the IcebergAPI() class, and passing 3 parameters wich are the user mail, first name and last name.
 * By passing directly two parameters in the IcebergAPI class wich are the access token and the username

```python
api_handler = IcebergAPI().sso("userEmail","userFirstName","userLastName")
```
```python
api_handler = IcebergAPI(access_token=XXXX, username=XXXX)
```

Resources
-------------

 * You have access to the following resources directly through the main IcebergAPI object:
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

For examples:
```python
api_handler.User()
api_handler.ProductOffer()
```

Methods
-------------

 * Methods are functions allowing you to access and manipulate the resources, the one we are going to use:
     * <code>find()</code> allows you to fetch a specific element within a list of elements, it can be product offers, products, orders.
     * <code>save()</code> allows you to update data about a store, offer, product etc... that has been modified.
     * <code>search()</code> returns a list of elements matching the requested parameter, the parameter can be a proprety like price, color, variation etc...
     * <code>to_JSON()</code> allow you to visualize the entirety of an object, JSON serialized.

For example:
```python
api_handler.ProductOffer.find("52")
api_handler.ProductOffer.find("52").to_JSON()
api_handler.ProductOffer.find("52").save()
```

ProductOffer
-------------

Offers differs from products, a product can not be added to a cart, the product is the physical object defined by it's brand, model, colors etc ... When someone by a product on a marketplace, he actually orders a specific offer from a specific merchant corresponding to a product.<br>
We are here going to deal with offers, or more accurately product offers.

### Get productOffer

In order to fetch an offer, we need to call the <code>find()</code> method within the <code>ProductOffer</code> Class, and passing the id of the requested product. Once we've got it, let's print some infos.


```python

offer = api_handler.ProductOffer.find("52")

print offer.default_image_url
print offer.description

for variation in offer.variations:
    print "%s items available in size %s, %s euros" %(variation['stock'],variation['name'],variation['price'])

```

### Edit productOffer

To edit an offer, you must be logged as a staff user. Simply fetch the object using the <code>find()</code> method again, then edit the product's attributes you want to change. And finally call the <code>save()</code> method upon your product object.


```python

    offer = api_handler.ProductOffer.find("52")

    offer.previous_price ="40.00"
    offer.default_image_url ="myimage.png"

    offer.save()
```

Cart
-------------

### Get infos of a user's cart

Retrieve the current logged in user's cart by calling the <code>mine()</code> method within the class <code>Cart</code> .

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

### Get order infos

Orders are available in your dashboard.
* Each Order is divided into 3 parts:
    * The Order object contains the summary of the order: total amount, adress, shipping, and the list of merchants concerned by the order (for example, 3 products have been ordered, 2 of them belong to merchant_1 and 1 of them belongs to merchand_2).
    * The MerchantOrder object: It contains all the infos a merchant recieves when an order is made and one or more products of the order are his.(for example, merchant_1 recieves a list of 2 items)
    * The OrderItem object contains the product informations and size.

Orders, Merchant Orders and Items are available in the /order section of your dashboard.
Let's display infos about the order number 11.

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

Retrieve specific infos about a user

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

Retrieve infos about a store in the application. We are gonna look for the store number 11 and display infos about it. This number is allocated automatically by Iceberg, you can find your stores's IDs in the get request's response on the "merchant" section.

```python

store = api_handler.Store.find(11)

print store.name
print store.created_on
print store.long_description
print store.url

```



