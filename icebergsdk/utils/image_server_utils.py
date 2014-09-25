# -*- coding: utf-8 -*-


def build_resized_image_url(image_server_url, original_url, width, height, process_mode="crop"):
    """
    Convert an image url to the appropriate image server format to get a resized version of the image.
    Needs attributes : width, height and process_mode.
    NB: the original_url needs to be publicly accessible (as it will be downloaded by the image server).
    """
    SUPPORTED_MODES = ["crop", "fit"]

    if process_mode not in SUPPORTED_MODES:
        raise Exception("unkwnown process mode '%s'. should be one of %s" % (process_mode, SUPPORTED_MODES))

    if not image_server_url:
        ## no image server, returning the origin url
        return original_url
     
    cleaned_url = original_url.replace("http://","").replace("https://","").replace("//","") ## no protocol nor //
    return "%s/ext/%s/%sx%s/%s" % (image_server_url, process_mode, width, height, cleaned_url)