import json
import os.path
import jsonschema
from jsonschema.exceptions import ValidationError, SchemaError
from settings import LOG_CFG_PATH, SCHEMA_PATH
from applier.dataservice import ApplyStoreDSO
from applier.utils.annotation import Annot
from applier.utils.log import Logger
from applier.apply import Apply
from applier.utils.error import FiRMSApplyJSONException, FiRMSApplyInvalidArgsException
from collections import defaultdict
from bunch import Bunch as dict2obj


@Annot.to_string
class Errands:
    """Context manager class to perform pre- and post-work for Apply.
    """

    @Annot.lazy_init
    def __init__(self, input_payload, **meta):
        """Constructor for `Errands` class. Instantiates `ApplyStoreDSO` for database operations.

        Args:
            input_payload (:obj:`bytes`): JSON input payload for apply.
            **meta: metadata information as keyword arguments.

        Returns:
            None
        """
        self.input_payload = input_payload
        self.__db = ApplyStoreDSO(prefetch=True, **meta)  # create data service object

    def __enter__(self):
        """This method runs when execution flow enters
        the code block inside the `with`. This is being used
        to do some pre-work before calling Apply module.
        """
        self.__prelims()
        return self

    def __exit__(
            self, exc_type, exc_val, exc_tb
    ):  # __exit__() method receives arguments containing details
        # of any exception raised in the with block.
        """This will perform some post apply work.This method is always called,
        even if an exception is raised.
        """
        if exc_type:
            logger.error(
                f"[Correlation ID: {self.corr_id}] [Ticket No: {self.ticket_no}] "
                f"[Username: {self.user}] > ({exc_type}:{exc_val})",
                exc_info=True,
            )
            return (
                False
            )  # False will re-raise the exception(if any) after __exit__ returns
            # return True to avoid propagating the exception(if any).
        self.__epilogue()
        return True

    def __prelims(self):
        """This method performs the following:

        .. code-block:: none

            > Check if we have any trace of the requested reference-id in our data-store.

        """
        logger.info(
            f"[Correlation ID: {self.corr_id}] [Ticket No: {self.ticket_no}] "
            f"[Username: {self.user}] > pre-work .."
        )

        # check status
        self.trace = self.__chk_status(self.__db.status)

        # do some more checks ..
        # e.g. self.somemore = self.__somemore()
        # ...

    def __epilogue(self):
        logger.info(
            f"[Correlation ID: {self.corr_id}] [Ticket No: {self.ticket_no}] "
            f"[Username: {self.user}] > post-work .."
        )

    def __chk_status(self, status):
        """
        Call different methods based on the given status

        .. code-block:: none

          if status is 'pending' then call _pending()
          if status is 'completed' then call _completed()
          and so on ..

        Args:
            status (str): new/pending/completed or published

        Returns:
            str: `cached result` from database if status is completed or published, `None` if
            pending and `False` if new.

        """
        return getattr(self, f"_{status}")()

    def _new(self):
        """
        This gets called when status is `new`
        """
        logger.info(
            f"[Correlation ID: {self.corr_id}] [Ticket No: {self.ticket_no}] "
            f"[Username: {self.user}] > new request"
        )
        return False

    def _pending(self):
        """
        This gets called when status is `pending`
        """
        logger.info(
            f"[Correlation ID: {self.corr_id}] [Ticket No: {self.ticket_no}] "
            f"[Username: {self.user}] > DUPLICATE!! Request is already being processed"
        )
        return None

    def _completed(self):
        """
        This gets called when status is `completed`,it returns cached apply-result
        from local data store.
        """
        logger.info(
            f"[Correlation ID: {self.corr_id}] [Ticket No: {self.ticket_no}] "
            f"[Username: {self.user}] > DUPLICATE!! Request has already been completed. "
            f"Fetching cached result from local DB."
        )
        return self.__db.cached_result

    def _published(self):
        """
        This gets called when status is `published`, it returns cached apply-result
        from local data store
        """
        logger.info(
            f"[Correlation ID: {self.corr_id}] [Ticket No: {self.ticket_no}] "
            f"[Username: {self.user}] > DUPLICATE!! Request has already been completed + published. "
            f"Fetching cached result from local DB."
        )
        return self.__db.cached_result

    def __decode_json(self, input_payload):

        """
        Convert byte array to a string with decode()
        and then parse json string object to dict
        """
        appl_json = []
        try:
            appl_json = json.loads(input_payload.decode())
            logger.debug(
                f"[Correlation ID: {self.corr_id}] [Ticket No: {self.ticket_no}] "
                f"[Username: {self.user}] > input payload is decoded and parsed successfully"
            )
        except Exception as e:
            logger.error(
                f"[Correlation ID: {self.corr_id}] [Ticket No: {self.ticket_no}] "
                f"[Username: {self.user}] > JSON Parsing failed.{e}",
                exc_info=True
            )
            raise FiRMSApplyJSONException("JSON Parsing failed.", e)

        return appl_json

    def __validate_payload(self, input_payload):
        """This method decodes and parses the given payload. In addition, it also validates the
        structure of the payload against a schema.

        Args:
            input_payload (:obj:`bytes`): JSON input payload

        Returns:
            :obj:`dict`: decoded JSON input payload

        Raises:
            FiRMSApplyJSONException: if validation fails

        """
        # decode & parse json
        input_payload = self.__decode_json(input_payload)

        # read the jsonschema file
        with open(f"{SCHEMA_PATH}/request.schema.json") as fl:
            schema = json.load(fl)

        logger.debug(
            f"[Correlation ID: {self.corr_id}] [Ticket No: {self.ticket_no}] "
            f"[Username: {self.user}] > JSON schema: {schema}"
        )
        try:
            jsonschema.validate(input_payload, schema)
            logger.info(
                f"[Correlation ID: {self.corr_id}] [Ticket No: {self.ticket_no}] "
                f"[Username: {self.user}] > input payload structure is validated "
                f"successfully against the schema"
            )
        except (ValidationError, SchemaError, Exception) as e:
            logger.error(
                f"[Correlation ID: {self.corr_id}] [Ticket No: {self.ticket_no}] "
                f"[Username: {self.user}] > Failed to validate payload against the schema.{e}",
                exc_info=True
            )
            raise FiRMSApplyJSONException(
                "Failed to validate payload against the schema.", e
            )

        return input_payload

    @property
    def input_payload(self):
        return self.__input_payload

    @input_payload.setter
    def input_payload(self, value):
        """setter method for input payload. Validation of payload is being done here.

        Args:
            value (:obj:`bytes`): JSON input payload

        Raises:
            FiRMSApplyInvalidArgsException: if value is empty
        """
        if not value:
            raise FiRMSApplyInvalidArgsException("'input_payload' cannot be empty")

        self.__input_payload = self.__validate_payload(value)


@Annot.to_string
class Job:
    """This class facilitates the process of applying configurations on the firewall
    devices after meeting certain prerequisites.
    Instantiate this class and call `do` method to initiate the apply process

    synopsis::

        from job import Job
        j = Job(
            input_payload,
            corr_id   =   "<reference id>",
            ticket_no =   "<ticket no for port opening request>",
            user      =   "<user who is executing the script>"
        )
        response = j.do()
    """

    @Annot.lazy_init
    def __init__(self, input_payload, **meta):
        """constructor for `Job` class.

        Args:
            input_payload (:obj:`bytes`): JSON input payload for apply.
            **meta: metadata information as keyword arguments.
        """
        self.input_payload = input_payload
        self.meta = meta

    def do(self):
        """This method uses context manager to do the task in this sequential order:

        .. code-block:: none

            > pre-work
            > run Apply
            > post-work

        Args:
            None

        Returns:
            str: Apply result in JSON formatted string
        """
        logger.debug(
            f"[Correlation ID: {self.corr_id}] [Ticket No: {self.ticket_no}] "
            f"[Username: {self.user}] > Begin ..."
        )

        with Errands(self.input_payload, **self.meta) as __res:

            if __res.trace == False:
                logger.info(
                    f"[Correlation ID: {self.corr_id}] [Ticket No: {self.ticket_no}] "
                    f"[Username: {self.user}] > {self.input_payload}"
                )

                appl = Apply(__res.input_payload, **self.meta)
                app_res = appl.run()

                return app_res

            else:
                return __res.trace


if __name__ == "__main__":
    print(Job.__doc__)