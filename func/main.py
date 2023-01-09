from http import HTTPStatus

from etria_logger import Gladsheim
from flask import request, Request
from heimdall_client import HeimdallStatusResponses
from heimdall_client.bifrost import Heimdall

from func.src.domain.enums.response.code import InternalCode
from func.src.domain.exceptions.exceptions import UnauthorizedError
from func.src.domain.request.model import WatchListSymbol
from func.src.domain.response.model import ResponseModel
from func.src.services.watch_list import WatchListService


async def remove_symbols(request: Request = request):
    raw_params = request.args.to_dict()
    x_thebes_answer = request.headers.get("x-thebes-answer")

    try:
        jwt_content, heimdall_status = await Heimdall.decode_payload(
            jwt=x_thebes_answer
        )
        if heimdall_status != HeimdallStatusResponses.SUCCESS:
            raise UnauthorizedError()

        watch_list_symbol = WatchListSymbol(**raw_params)
        unique_id = jwt_content["decoded_jwt"]["user"]["unique_id"]
        result = await WatchListService.delete_symbols(
            watch_list_symbol=watch_list_symbol, unique_id=unique_id
        )

        response = ResponseModel(
            success=result,
            code=InternalCode.SUCCESS,
            message="Symbols successfully deleted",
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ValueError as ex:
        message = "Invalid parameters"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message=message
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except UnauthorizedError as ex:
        message = "JWT invalid or not supplied"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message=message,
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response
    except Exception as ex:
        message = "Unexpected error occurred"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=message
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
