# from fastapi import Request, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.exceptions import RequestValidationError
# from pydantic import ValidationError
# # from schemas import ErrorResponse

# from core.logger import get_logger


# logger = get_logger("exception")


# async def global_exception_handler(request: Request, exc: Exception):
#     # Request Validation Error (for query/path parameters)
#     if isinstance(exc, RequestValidationError):
#         errors = {}
#         for error in exc.errors():
#             field = ".".join(str(loc) for loc in error["loc"])
#             errors[field] = error["msg"]

#         return JSONResponse(
#             status_code=422,
#             content=ErrorResponse(
#                 status_code=422,
#                 error_type="RequestValidationError",
#                 message="Request validation failed",
#                 details=errors,
#             ).model_dump(),
#         )

#     # Pydantic Validation Error (For body)
#     if isinstance(exc, ValidationError):
#         errors = {}
#         for error in exc.errors():
#             field = ".".join(str(loc) for loc in error["loc"])
#             errors[field] = error["msg"]

#         return JSONResponse(
#             status_code=422,
#             content=ErrorResponse(
#                 status_code=422,
#                 error_type="ValidationError",
#                 message="Validation failed",
#                 details=errors,
#             ).model_dump(),
#         )

#     # FastAPI HTTP Exception (404, 401, etc)
#     if isinstance(exc, HTTPException):
#         return JSONResponse(
#             status_code=exc.status_code,
#             content=ErrorResponse(
#                 status_code=exc.status_code,
#                 error_type="HTTPException",
#                 message=str(exc.detail),
#                 details=None,
#             ).model_dump(),
#         )

#     # Unknown Error (500)
#     logger.exception("Unhandled server error occurred", exc_info=exc)
#     return JSONResponse(
#         status_code=500,
#         content=ErrorResponse(
#             status_code=500,
#             error_type="InternalServerError",
#             message="An unexpected error occurred",
#             details=None,
#         ).model_dump(),
#     )
