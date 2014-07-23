#### Get infos of a specific offer

Let's fetch some specific informations about an offer, display the image url, description, and get stock, size and price for each variation. 

<pre>

def offerInfos():

    #instanciate Iceberg API
    api_handler = IcebergAPI()

    #fetch offer object width the product ID
    product = api_handler.ProductOffer.find("52")

    #print infos
    print product.default_image_url
    print product.description
    for variation in product.variations:
        print "%s items available in size %s, %s euros" %(variation['stock'],variation['name'],variation['price'])

</pre>
* * *

#### Add product to cart

These few lines of code show you how to simply add a product to a specific user's cart, don't forget to pass the 4 required arguments.

<pre>

def addProduct(email,first_name,last_name):

    #instanciate Iceberg API
    api_handler = IcebergAPI()

    #Identification 
    api_handler.sso(email, first_name, last_name)

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
    
</pre>
* * *


#### Get infos of a user's cart

Let's retrieve a user's cart object and display its shipping_adress, shipping amount and total amount.

<pre>

def cartInfos(email,first_name,last_name):

    #instanciate Iceberg API
    api_handler = IcebergAPI()

    #Identification 
    api_handler.sso(email, first_name, last_name)

    #cart object
    user_cart = api_handler.Cart.mine()

    #print infos
    print user_cart.shipping_address
    print user_cart.shipping_amount
    print user_cart.total_amount
    

</pre>
* * *


#### Get user infos

Retrieve specific infos about a user

<pre>

def userInfos(email,first_name,last_name):

    api_handler = IcebergAPI()

    #Identification 
    api_handler.sso(email, first_name, last_name)

    me = api_handler.User.me()
    
    #print me.to_JSON()
    print me.username
    print me.first_name
    print me.last_name
    print me.email
    print me.timezone
</pre>
* * *


#### Get store infos

Retrieve infos about a store in the application. We are gonna look for the store number 11 and display infos about it. This number is allocated automatically by Iceberg, you can find your stores's IDs in the get request's response on the "merchant" section.

<pre>

def storeInfos():

    api_handler = IcebergAPI()

    store = api_handler.Store.find(11)

    print store.name
    print store.created_on
    print store.long_description
    print store.url
</pre>



