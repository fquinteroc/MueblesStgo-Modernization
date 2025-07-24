from werkzeug.exceptions import HTTPException
from flask import jsonify

class APIError(HTTPException):
    code = 400
    description = 'API Error'

class BadRequest(APIError):
    code = 400
    description = 'Bad request'

class NotFound(APIError):
    code = 404
    description = 'Not found'

class Forbidden(APIError):
    code = 403
    description = 'Forbidden'