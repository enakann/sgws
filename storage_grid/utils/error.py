import sys


class FiRMSApplierException(Exception):

    """
      Base class for all exceptions raised by it's subclasses

    """

    def __init__(self, info, excp=None):

        super(FiRMSApplierException, self).__init__(info)

        self.info = info
        self.exception = excp
        self.name = self.__class__.__name__


class FiRMSApplyDBException(FiRMSApplierException):
    """ raised if any problem occurs during db ops """

    pass


class FiRMSApplyJSONException(FiRMSApplierException):
    """ raised if any problem occurs during json ops"""

    pass


class FiRMSApplyInvalidArgsException(FiRMSApplierException):
    """ raised if arguments to the methods are invalid"""

    pass
