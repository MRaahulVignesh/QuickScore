
class DatabaseError(Exception):
    pass

class DuplicateError(Exception):
    pass

class InternalServerError(Exception):
    pass

class NotFoundError(Exception):
    pass

class AuthenticationError(Exception):
    pass

class ModelError(Exception):
    pass

class BadRequestError(Exception):
    pass