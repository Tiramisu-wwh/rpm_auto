"""
自定义异常类 - 提供更精确的错误处理
"""
from typing import Optional, Dict, Any

class RPMTestException(Exception):
    """RPM测试框架基础异常类"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message

class ConfigurationError(RPMTestException):
    """配置错误异常"""
    
    def __init__(self, message: str, config_key: Optional[str] = None):
        super().__init__(message, "CONFIG_ERROR", {"config_key": config_key})
        self.config_key = config_key

class AuthenticationError(RPMTestException):
    """认证错误异常"""
    
    def __init__(self, message: str, username: Optional[str] = None, response_code: Optional[int] = None):
        super().__init__(message, "AUTH_ERROR", {
            "username": username,
            "response_code": response_code
        })
        self.username = username
        self.response_code = response_code

class APIRequestError(RPMTestException):
    """API请求错误异常"""
    
    def __init__(self, message: str, method: str, url: str, status_code: Optional[int] = None, 
                 response_text: Optional[str] = None):
        super().__init__(message, "API_ERROR", {
            "method": method,
            "url": url,
            "status_code": status_code,
            "response_text": response_text
        })
        self.method = method
        self.url = url
        self.status_code = status_code
        self.response_text = response_text

class NetworkError(RPMTestException):
    """网络错误异常"""
    
    def __init__(self, message: str, url: str, retry_count: int = 0):
        super().__init__(message, "NETWORK_ERROR", {
            "url": url,
            "retry_count": retry_count
        })
        self.url = url
        self.retry_count = retry_count

class ValidationError(RPMTestException):
    """数据验证错误异常"""
    
    def __init__(self, message: str, field_name: Optional[str] = None, 
                 expected_value: Optional[Any] = None, actual_value: Optional[Any] = None):
        super().__init__(message, "VALIDATION_ERROR", {
            "field_name": field_name,
            "expected_value": expected_value,
            "actual_value": actual_value
        })
        self.field_name = field_name
        self.expected_value = expected_value
        self.actual_value = actual_value

class TestDataError(RPMTestException):
    """测试数据错误异常"""
    
    def __init__(self, message: str, data_file: Optional[str] = None, data_key: Optional[str] = None):
        super().__init__(message, "TEST_DATA_ERROR", {
            "data_file": data_file,
            "data_key": data_key
        })
        self.data_file = data_file
        self.data_key = data_key

class TimeoutError(RPMTestException):
    """超时错误异常"""
    
    def __init__(self, message: str, timeout_seconds: int, operation: Optional[str] = None):
        super().__init__(message, "TIMEOUT_ERROR", {
            "timeout_seconds": timeout_seconds,
            "operation": operation
        })
        self.timeout_seconds = timeout_seconds
        self.operation = operation

class BusinessLogicError(RPMTestException):
    """业务逻辑错误异常"""
    
    def __init__(self, message: str, business_code: Optional[str] = None, 
                 business_message: Optional[str] = None):
        super().__init__(message, "BUSINESS_ERROR", {
            "business_code": business_code,
            "business_message": business_message
        })
        self.business_code = business_code
        self.business_message = business_message