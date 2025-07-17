from fastapi.responses import JSONResponse

def standard_response(status: str, message: str, data=None, status_code=200):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status,
            "message": message,
            "data": data
        }
    )
