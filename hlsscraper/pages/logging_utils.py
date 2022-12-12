import logging
import sys
import traceback


def setup_logging_to_file(filename: str) -> None:
    """Setup logging to log to a file."""
    logging.basicConfig(
        filename=filename,
        filemode="w",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def extract_function_name() -> str:
    """Extracts failing function name from Traceback object."""
    tb = sys.exc_info()[-1]
    stk = traceback.extract_tb(tb, 1)
    fname = stk[0][3]
    return str(fname)


def log_exception(e: Exception) -> None:
    """Logs exception with traceback."""
    logging.error(
        "Function {function_name} raised {exception_class} ({exception_docstring}): {exception_message}".format(
            function_name=extract_function_name(),  # this is optional
            exception_class=e.__class__,
            exception_docstring=e.__doc__,
            exception_message=str(e),
        )
    )
