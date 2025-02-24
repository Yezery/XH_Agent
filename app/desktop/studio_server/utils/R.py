from fastapi import HTTPException


def success(data=None, message="请求成功"):
    return {"success": True, "message": message, "data": data}

def error(status_code=500, message=None, error=None):
    error_detail = {
        "message": message,
        "error_info": error
    }
    raise HTTPException(status_code=status_code, detail=error_detail)