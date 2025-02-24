from typing import NoReturn


def raise_exhaustive_enum_error(value: NoReturn) -> NoReturn:
    raise ValueError(f"{value}")

ERROR_CODE_MAPPING = {
    400: "请求无效，请检查输入参数。",
    401: "认证失败，请检查 API Key。",
    402: "账户余额不足，请充值。",
    403: "无权限访问，请检查权限设置。",
    404: "请求的资源未找到。",
    429: "请求过多，请稍后再试。",
    500: "服务器内部错误，请联系管理员。",
}

def error_code_to_message(code: int) -> str:
    return ERROR_CODE_MAPPING.get(code, "未知错误")