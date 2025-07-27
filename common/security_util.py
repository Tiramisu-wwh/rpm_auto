"""
安全工具类 - 处理敏感信息脱敏
"""
import re
import json
import hashlib
from typing import Any, Dict, List, Union, Optional

class SecurityUtil:
    """安全工具类"""
    
    # 敏感字段关键词
    SENSITIVE_KEYWORDS = [
        'password', 'passwd', 'pwd', 'secret', 'token', 'key', 'auth',
        'credential', 'authorization', 'captcha', 'code', 'otp', 'checkkey',
        'session', 'cookie', 'sign', 'signature', 'access_token', 'refresh_token'
    ]
    
    # URL敏感参数模式
    URL_SENSITIVE_PATTERNS = [
        (r'([?&](?:password|token|key|auth|captcha|checkkey)=)[^&\s]+', r'\1***'),
        (r'(Authorization:\s*)[^\s]+', r'\1Bearer ***'),
        (r'(Cookie:\s*)[^\r\n]+', r'\1***'),
    ]
    
    # JSON敏感字段模式
    JSON_SENSITIVE_PATTERNS = [
        (r'("(?:password|token|key|auth|captcha|checkkey)"\s*:\s*")[^"]+(")', r'\1***\2'),
        (r'("(?:password|token|key|auth|captcha|checkkey)"\s*:\s*)(\d+)', r'\1***'),
    ]
    
    @classmethod
    def sanitize_data(cls, data: Any) -> Any:
        """脱敏处理数据"""
        if data is None:
            return None
        elif isinstance(data, dict):
            return cls._sanitize_dict(data)
        elif isinstance(data, list):
            return [cls.sanitize_data(item) for item in data]
        elif isinstance(data, str):
            return cls._sanitize_string(data)
        elif isinstance(data, (int, float, bool)):
            return data
        else:
            return str(data)
    
    @classmethod
    def _sanitize_dict(cls, data: Dict) -> Dict:
        """脱敏字典数据"""
        sanitized = {}
        for key, value in data.items():
            if cls._is_sensitive_field(key):
                sanitized[key] = cls._mask_value(value)
            else:
                sanitized[key] = cls.sanitize_data(value)
        return sanitized
    
    @classmethod
    def _sanitize_string(cls, data: str) -> str:
        """脱敏字符串中的敏感信息"""
        if not data:
            return data
            
        # 尝试脱敏JSON字符串
        try:
            json_data = json.loads(data)
            return json.dumps(cls.sanitize_data(json_data), ensure_ascii=False)
        except (json.JSONDecodeError, TypeError):
            pass
        
        # 脱敏URL中的敏感参数
        result = data
        for pattern, replacement in cls.URL_SENSITIVE_PATTERNS:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        # 脱敏JSON格式字符串中的敏感字段
        for pattern, replacement in cls.JSON_SENSITIVE_PATTERNS:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return result
    
    @classmethod
    def _is_sensitive_field(cls, field_name: str) -> bool:
        """判断是否为敏感字段"""
        if not isinstance(field_name, str):
            return False
        field_lower = field_name.lower()
        return any(keyword in field_lower for keyword in cls.SENSITIVE_KEYWORDS)
    
    @classmethod
    def _mask_value(cls, value: Any) -> str:
        """遮蔽敏感值"""
        if value is None:
            return None
        
        str_value = str(value)
        if len(str_value) == 0:
            return ""
        elif len(str_value) <= 3:
            return "***"
        elif len(str_value) <= 8:
            return str_value[:1] + "***" + str_value[-1:]
        else:
            return str_value[:2] + "***" + str_value[-2:]
    
    @classmethod
    def generate_request_id(cls, method: str, url: str) -> str:
        """生成请求ID用于日志追踪"""
        content = f"{method}:{url}:{hash(str(time.time()))}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    @classmethod
    def validate_config_security(cls, config: Dict[str, Any]) -> List[str]:
        """验证配置安全性，返回安全问题列表"""
        issues = []
        
        # 检查是否有明文密码
        for key, value in config.items():
            if cls._is_sensitive_field(key) and isinstance(value, str):
                if len(value) > 0 and not value.startswith('***'):
                    issues.append(f"配置项 '{key}' 可能包含明文敏感信息")
        
        # 检查URL中是否包含敏感信息
        base_url = config.get('base_url', '')
        if any(keyword in base_url.lower() for keyword in ['password', 'token', 'key']):
            issues.append("base_url 中可能包含敏感信息")
        
        return issues