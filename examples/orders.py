# -*- coding: utf-8 -*-

from datetime import datetime

import logging
logger = logging.getLogger(__name__)

def pass_3d_secure_page(url):
    import time
    from selenium import webdriver

    driver = webdriver.Chrome()

    try:
        driver.get(url)
        time.sleep(3) # Wait 5 secs to be sure browser will go to step2

        driver.find_element_by_name("password").send_keys('secret3')
        driver.find_element_by_name("submit").click()

        # Waiting (max : 10s) for mangopay redirection to return_url (that test sent - see few lines above )
        # for i in range(10):
        #     if check_string in driver.current_url:
        #         break
        #     else:
        #         time.sleep(1)
        time.sleep(3)
    finally:
        driver.quit()

    return True


def create_order(username, access_token, productoffer_id = None):
    from icebergsdk.api import IcebergAPI
    from icebergsdk.exceptions import IcebergClientError

    api_handler = IcebergAPI(username = username, access_token = access_token)
    
    # User
    api_user = api_handler.User.me()

    # New Cart
    cart = api_handler.Cart()
    cart.debug = True
    cart.save()

    product_offer = api_handler.ProductOffer.find(int(productoffer_id))

    # Add To Cart
    cart.addOffer(product_offer)
    cart.fetch()

    # Address
    if not cart.shipping_address:
        user_addresses = api_user.addresses()

        if len(user_addresses) == 0:
            # Create an address
            user_address = api_handler.Address()
            user_address.name = "Test"
            user_address.first_name = "Florian"
            user_address.last_name = "Poullin"
            user_address.address = "325 rue de charenton"
            # user_address.address2 
            user_address.zipcode = "75012"
            user_address.city = "Paris"
            # user_address.state = 
            user_address.user = api_user
            user_address.country = api_handler.Country.search({'code': 'FR'})[0][0]
            # user_address.phone = 
            # user_address.digicode
            # user_address.company
            # user_address.floor
            user_address.save()

        else:
            user_address = user_addresses[0]

        cart.shipping_address = user_address
        cart.save()

    if cart.has_changed():
        cart.save()


    if cart.status != "20": # Valide
        raise Exception('Should be valide')

    # Payment
    try:
        form_data = cart.form_data()
    except IcebergClientError, e:
        if 90001 in e.error_codes and api_user.is_staff: # User Birthday
            profile = api_user.profile()
            profile.birth_date = datetime.strptime('Jun 3 1980', '%b %d %Y')
            profile.save()

            form_data = cart.form_data()
        else:
            raise e

    order = cart.createOrder({
        'pre_auth_id': form_data['id']
    })

    # Create Card Alias
    import urllib, urllib2

    url = form_data['CardRegistrationURL']

    params = {
        "data": form_data['PreregistrationData'],
        "accessKeyRef": form_data['AccessKey'],
        "cardNumber": "4970101122334471",
        "cardExpirationDate": "1015", # Should be in the future
        "cardCvx": "123"
    }
    params_enc = urllib.urlencode(params)
    request = urllib2.Request(url, params_enc)
    page = urllib2.urlopen(request)
    content = page.read()
    card_registration_data = content.replace('data=', '')

    print card_registration_data

    order.authorizeOrder({
        "data": card_registration_data
    })

    if hasattr(order.payment, 'redirect_url'): # 3D Secure
        print "Need 3D Secure"
        pass_3d_secure_page(order.payment.redirect_url)
        order.updateOrderPayment()



    return True


