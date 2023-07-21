import requests

class RequestError(Exception):
    pass

class DownloadError(RequestError):
    pass

class ParsingError(Exception):
    pass

def handle_request_error(e):
    if isinstance(e, requests.exceptions.RequestException):
        raise DownloadError(f"Failed to download CSV. Error: {e}")
    else:
        raise RequestError(f"An error occurred during the request. Error: {e}")

def handle_parsing_error(e):
    raise ParsingError(f"An error occurred while parsing the CSV. Error: {e}")
