# -*- coding: utf-8 -*-

# import logging
# logger = logging.getLogger('icebergsdk.exceptions')


class IcebergError(Exception):
    pass


class IcebergMissingApplicationSettingsError(IcebergError):
    pass


class IcebergNoHandlerError(IcebergError):
    pass


class IcebergConnectionError(IcebergError):
    pass


class IcebergAuthenticationError(IcebergError):
    pass


class IcebergBadRequestError(IcebergError):
    pass


class IcebergTransitionError(IcebergError):
    pass


class IcebergInternalServerError(IcebergError):
    pass


class IcebergRateLimitExceeded(IcebergError):
    pass


class IcebergNotAuthorized(IcebergError):
    pass


class IcebergReadOnlyError(IcebergError):
    pass


class IcebergMissingSsoData(IcebergError):
    pass


class IcebergMultipleObjectsReturned(IcebergError):
    pass


# API
class IcebergAPIError(IcebergError):
    def __init__(self, response=None, url=None):
        self.status_code = None
        self.error_codes = []
        self.message = ''
        self.url = url
        self.data = None

        if response is not None:
            self.status_code = response.status_code

            try:
                self.data = response.json()
            except:
                self.data = response
            else:
                if 'errors' in self.data:
                    for error in self.data['errors']:
                        if isinstance(error, basestring):
                            self.message += error
                        else:
                            if 'code' in error:
                                self.error_codes.append(error['code'])
                            self.message += error['msg']
                if 'error' in self.data:
                    if isinstance(self.data['error'], basestring):
                        self.message += self.data['error']
                    else:
                        self.message += self.data['error']['msg']

        Exception.__init__(self, self.message)

    def __str__(self):
        if len(self.message) > 0:
            message = self.message
        else:
            message = self.data
        return "Error in %s! %s : %s: %s" % (self.url, self.status_code, self.error_codes, message)


class IcebergObjectNotFound(IcebergAPIError):
    pass


class IcebergServerError(IcebergAPIError):
    pass


class IcebergClientError(IcebergAPIError):
    pass


class IcebergClientUnauthorizedError(IcebergError):
    pass


class ApplicationNotFound(IcebergError):
    pass
