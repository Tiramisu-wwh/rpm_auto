"""
配置管理器 - 统一管理所有配置
"""
import os
import yaml
from typing import Dict, Any, Optional, List
from pathlib import Path
from common.logger import Logger
from common.security_util import SecurityUtil

logger = Logger().get_logger()

class ConfigManager:
    """配置管理器，支持环境变量覆盖和多环境配置"""
    
    _instance: Optional['ConfigManager'] = None
    _config: Dict[str, Any] = {}
    _config_loaded: bool = False
    
    def __new__(cls) -> 'ConfigManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._config_loaded:
            self._load_config()
            self._config_loaded = True
    
    def _load_config(self) -> None:
        """加载配置文件"""
        try:
            config_dir = Path(__file__).parent.parent / "config"
            
            # 获取环境标识
            env = os.getenv("TEST_ENV", "default")
            logger.info(f"当前环境: {env}")
            
            # 加载主配置文件
            main_config_file = config_dir / "config.yaml"
            if main_config_file.exists():
                with open(main_config_file, 'r', encoding='utf-8') as f:
                    self._config = yaml.safe_load(f) or {}
                logger.info(f"加载主配置文件: {main_config_file}")
            else:
                logger.warning(f"主配置文件不存在: {main_config_file}")
                self._config = {}
            
            # 加载环境特定配置
            if env != "default":
                env_config_file = config_dir / f"config_{env}.yaml"
                if env_config_file.exists():
                    with open(env_config_file, 'r', encoding='utf-8') as f:
                        env_config = yaml.safe_load(f) or {}
                        self._config.update(env_config)
                    logger.info(f"加载环境配置文件: {env_config_file}")
            
            # 环境变量覆盖
            self._override_with_env_vars()
            
            # 验证配置安全性
            self._validate_security()
            
            # 设置默认值
            self._set_defaults()
            
            logger.info("配置加载完成")
            
        except Exception as e:
            logger.error(f"配置加载失败: {str(e)}")
            raise ConfigurationError(f"配置加载失败: {str(e)}")
    
    def _override_with_env_vars(self) -> None:
        """使用环境变量覆盖配置"""
        env_mappings = {
            "BASE_URL": "base_url",
            "USERNAME": "username", 
            "PASSWORD": "password",
            "CAPTCHA": "captcha",
            "TIMEOUT": "timeout",
            "MAX_RETRIES": "max_retries",
            "LOG_LEVEL": "log_level",
            "ALLURE_RESULTS_DIR": "allure_results_dir"
        }
        
        overridden_keys = []
        for env_key, config_key in env_mappings.items():
            env_value = os.getenv(env_key)
            if env_value:
                # 类型转换
                if config_key in ["timeout", "max_retries"]:
                    try:
                        env_value = int(env_value)
                    except ValueError:
                        logger.warning(f"环境变量 {env_key} 值无效，使用默认值")
                        continue
                elif config_key in ["debug"]:
                    env_value = env_value.lower() in ['true', '1', 'yes', 'on']
                
                self._config[config_key] = env_value
                overridden_keys.append(config_key)
        
        if overridden_keys:
            logger.info(f"环境变量覆盖配置项: {overridden_keys}")
    
    def _validate_security(self) -> None:
        """验证配置安全性"""
        security_issues = SecurityUtil.validate_config_security(self._config)
        if security_issues:
            for issue in security_issues:
                logger.warning(f"安全警告: {issue}")
    
    def _set_defaults(self) -> None:
        """设置默认配置值"""
        defaults = {
            "timeout": 30,
            "max_retries": 3,
            "log_level": "INFO",
            "allure_results_dir": "./allure-results",
            "verify_ssl": True,
            "pool_connections": 10,
            "pool_maxsize": 20
        }
        
        for key, default_value in defaults.items():
            if key not in self._config:
                self._config[key] = default_value
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值，支持嵌套键（如：database.host）"""
        try:
            keys = key.split('.')
            value = self._config
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            
            return value
        except Exception as e:
            logger.warning(f"获取配置项 '{key}' 失败: {str(e)}")
            return default
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值"""
        try:
            keys = key.split('.')
            config = self._config
            
            # 导航到最后一级
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            config[keys[-1]] = value
            logger.debug(f"设置配置项: {key} = {value}")
        except Exception as e:
            logger.error(f"设置配置项 '{key}' 失败: {str(e)}")
            raise ConfigurationError(f"设置配置项失败: {str(e)}")
    
    def get_api_config(self) -> Dict[str, Any]:
        """获取API相关配置"""
        return {
            "base_url": self.get("base_url"),
            "timeout": self.get("timeout", 30),
            "max_retries": self.get("max_retries", 3),
            "verify_ssl": self.get("verify_ssl", True),
            "pool_connections": self.get("pool_connections", 10),
            "pool_maxsize": self.get("pool_maxsize", 20)
        }
    
    def get_auth_config(self) -> Dict[str, str]:
        """获取认证相关配置"""
        return {
            "username": self.get("username"),
            "password": self.get("password"),
            "captcha": self.get("captcha")
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """获取日志相关配置"""
        return {
            "log_level": self.get("log_level", "INFO"),
            "log_file": self.get("log_file"),
            "log_format": self.get("log_format"),
            "log_max_size": self.get("log_max_size", "10MB"),
            "log_backup_count": self.get("log_backup_count", 5)
        }
    
    def get_allure_config(self) -> Dict[str, Any]:
        """获取Allure相关配置"""
        return {
            "results_dir": self.get("allure_results_dir", "./allure-results"),
            "report_dir": self.get("allure_report_dir", "./allure-report"),
            "clean_results": self.get("allure_clean_results", True)
        }
    
    def validate_required_config(self, required_keys: List[str]) -> None:
        """验证必需的配置项是否存在"""
        missing_keys = []
        for key in required_keys:
            if self.get(key) is None:
                missing_keys.append(key)
        
        if missing_keys:
            error_msg = f"缺少必需的配置项: {missing_keys}"
            logger.error(error_msg)
            raise ConfigurationError(error_msg)
    
    def get_safe_config(self) -> Dict[str, Any]:
        """获取脱敏后的配置（用于日志记录）"""
        return SecurityUtil.sanitize_data(self._config.copy())
    
    def reload_config(self) -> None:
        """重新加载配置"""
        logger.info("重新加载配置...")
        self._config.clear()
        self._config_loaded = False
        self._load_config()
        self._config_loaded = True

class ConfigurationError(Exception):
    """配置错误异常"""
    pass