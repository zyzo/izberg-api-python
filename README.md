#Iceberg Python API

Iceberg API provides an entire set of functions and class to access and edit Iceberg data.

Table of Content
-------------
**Get started**

1. [Setup](##Setup)
2. [Cart](##Cart)
3. [Store](##Store)




##Setup

### Env variables

As you may have seen in the conf.py file, 3 environment variables ar needed to use the Iceperg python API: the Iceberg private key, the Iceberg secret key and the application namespace. These variables must be initiated as environment variables.

```python

export ICEBERG_API_PRIVATE_KEY=XXXXXX
export ICEBERG_APPLICATION_NAMESPACE=my_app
export ICEBERG_APPLICATION_SECRET_KEY=XXXXXX

```

### Log in 

There are two ways to log in:
    * By calling the sso function in the IcebergAPI() class, and passing 3 parameters wich are the user mail, first name and last name.
    * By passing directly two parameters in the IcebergAPI class wich are the access token and the username

```python
api_handler = IcebergAPI().sso("userEmail","userFirstName","userLastName")
```
```python
api_handler = IcebergAPI(access_token=accessToken, username="yvesdurant1032644")
```
##Offer

### Get offer

In order to fetch an offer, we need to call the <code>find</code> function within the <code>ProductOffer</code> Class, and passing the id of the requested product. Once we've got it, let's print some infos.


```python

#fetch offer object width the product ID
product = api_handler.ProductOffer.find("52")

#print infos
print product.default_image_url
print product.description
for variation in product.variations:
    print "%s items available in size %s, %s euros" %(variation['stock'],variation['name'],variation['price'])

```

##Cart

### Get infos of a user's cart

Retrieve the current logged in user's cart by calling the <code>.mine()</code> function within the class <code>Cart</code> .

```python

#cart object
user_cart = api_handler.Cart.mine()

#print infos
print user_cart.shipping_address
print user_cart.shipping_amount
print user_cart.total_amount
    
```

### Add product to cart

These few lines of code show you how to simply add a product to a specific user's cart, don't forget to pass the 4 required arguments.

```python

#Get cart
user_cart = api_handler.Cart.mine()

#fetch offer object width the product ID
product = api_handler.ProductOffer.find("52")

#print propreties of the product you just found
print product.description
print product.price_with_vat

#Add offer to the logged user's cart
user_cart.addOffer(product)

#print total amount of the cart
print api_handler.Cart.mine().total_amount
    
```

## User

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


## Store

### Get store infos

Retrieve infos about a store in the application. We are gonna look for the store number 11 and display infos about it. This number is allocated automatically by Iceberg, you can find your stores's IDs in the get request's response on the "merchant" section.

```python

store = api_handler.Store.find(11)

print store.name
print store.created_on
print store.long_description
print store.url

```



