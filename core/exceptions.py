class AppException(Exception):
    status_code = 400
    error_type = "ApplicationError"

    def __init__(self, message: str):
        self.message = message


class RoleNotFoundException(AppException):
    status_code = 404
    error_type = "RoleNotFound"


class PermissionNotFoundException(AppException):
    status_code = 404
    error_type = "PermissionNotFound"


class PermissionDeniedException(AppException):
    status_code = 403
    error_type = "PermissionDenied"
