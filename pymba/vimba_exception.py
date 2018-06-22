# -*- coding: utf-8 -*-


class VimbaException(Exception):

    """
    An exception for the AVT Vimba API. It contains a message
    property which is a string indicating what went wrong.

    :param errorCode: Error code to be used to look up error message.
    """

    @property
    def message(self):
        return self._errorCodes[self.errorCode]

    @property
    def errorCode(self):
        return self._errorCode

    _errorCodes = {  # Vimba C API specific errors
        0: 	'No error.',
        -1: 	'Unexpected fault in VimbaC or driver.',
        -2: 	'VmbStartup() was not called before the current command.',
        -3: 	'The designated instance (camera, feature etc.) cannot be found.',
        -4: 	'The given handle is not valid, ensure device open.',
        -5: 	'Device was not opened for usage.',
        -6: 	'Operation is invalid with the current access mode.',
        -7: 	'One of the parameters was invalid (usually an illegal pointer).',
        -8: 	'The given struct size is not valid for this version of the API.',
        -9: 	'More data was returned in a string/list than space was provided.',
        -10:    'The feature type for this access function was wrong.',
        -11:    'The value was not valid; either out of bounds or not an increment of the minimum.',
        -12:    'Timeout during wait.',
        -13:    'Other error.',
        -14:    'Resources not available (e.g. memory).',
        -15:    'Call is invalid in the current context (e.g. callback).',
        -16:    'No transport layers were found.',
        -17:    'API feature is not implemented.',
        -18:   	'API feature is not supported.',
        -19:    'A multiple registers read or write was partially completed.',

        # Custom errors
        -50:	'Could not find the specified camera.',
        -51:	'Not enough memory to assign frame buffer.',
        -52:	'Invalid input.',
        -53:	'Could not find the specified feature.',
        -54:	'Could not find the specified interface.',

        # Miscellaneous errors
        -1000:	'Oops, unknown internal error code!',
        -1001:	'Oops, this VimbaFeature function is not yet implemented in pymba!'}

    def __init__(self, errorCode):
        # if error code does not match expected codes then assign invalid code
        if errorCode in self._errorCodes:
            self._errorCode = errorCode
        else:
            self._errorCode = -1000

        super(VimbaException, self).__init__(self.message)
