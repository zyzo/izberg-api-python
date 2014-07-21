import sys, os, json
sys.path[0:0] = [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from icebergsdk.api import IcebergAPI





def addProduct(id,email,first_name,last_name):

    api_handler = IcebergAPI()

    #Identification 
    api_handler.sso(email, first_name, last_name)

    #Get cart
    user_cart = api_handler.Cart.mine()

    #Find product
    product = api_handler.ProductOffer.find("52")

    #print propreties of the product you just found
    print product.description
    print product.price_with_vat
   
    #Add product to cart
    user_cart.addOffer(product)

    #print total amount of the cart
    print api_handler.Cart.mine().total_amount


def getInfos(id,email,first_name,last_name):

    api_handler = IcebergAPI()

    #fetch offer object
    product = api_handler.ProductOffer.find("52")

    print product.default_image_url
    print product.description
    for variation in product.variations:
        print "%s items available in size %s, %s euros" %(variation['stock'],variation['name'],variation['price'])

def cartInfos(id,email,first_name,last_name):

    api_handler = IcebergAPI()

    #Identification 
    api_handler.sso(email, first_name, last_name)

    user_cart = api_handler.Cart.mine()

    print user_cart.shipping_address
    print user_cart.total_amount
    print user_cart.estimated_shipping_country


def userInfos(id,email,first_name,last_name):

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


userInfos("52","lol@lol.fr","Yves","Durand")



