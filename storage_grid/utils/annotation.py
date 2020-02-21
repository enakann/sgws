from functools import wraps
from applier import ALLOWED_HEADERS
from applier.utils.error import FiRMSApplyInvalidArgsException


class Annot:
    """`Annot` class aims to annnotate classes, functions to reduce boilerplate codes.
    """

    def to_string(cls):
        """decorator to auto generate a __str__() implementation.
        
        Args:
            cls (obj): class
    
        Returns:
            cls (obj): __str__() implemented class
        """

        def __str__(self):
            attrs = ", ".join(f"{k}={v}" for k, v in vars(self).items())
            return "%s(%s)" % (type(self).__name__, attrs)

        cls.__str__ = __str__
        return cls

    def lazy_init(f):
        """decorator to iterate through kwargs, validate and set them as instance variables.
      
        Args:
            method (obj): __init__()

        Returns:
            method (obj): decrorated __init__() method
 
        Raises:
            FiRMSApplyInvalidArgsException: if any mandatory arguments is missing
        """

        @wraps(f)
        def decorator(self, *args, **kwargs):

            present = set(ALLOWED_HEADERS).difference(set(kwargs.keys()))

            if present:
                raise Exception(
                    f"Mandatory headers missing. Expected: {ALLOWED_HEADERS}"
                )
            else:
                for key, value in kwargs.items():
                    if not value:
                        raise FiRMSApplyInvalidArgsException(f"'{key}' cannot be empty")

                    setattr(self, key, value)

            return f(self, *args, **kwargs)

        return decorator
