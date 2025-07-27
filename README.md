# RPM自动化测试框架

基于 `pytest + requests + allure` 的接口自动化测试框架，支持登录认证、验证码处理、数据驱动、日志记录、报告生成等功能。

## 🚀 功能特性

- ✅ **自动登录**: 支持验证码自动获取和token管理，带重试机制
- ✅ **业务封装**: ContractAPI、ProjectAPI等业务化封装，测试用例更清晰
- ✅ **数据驱动**: YAML配置测试数据，支持参数化测试
- ✅ **日志记录**: 详细的请求响应日志，自动脱敏敏感信息
- ✅ **报告生成**: 精美的中文Allure测试报告，包含步骤、附件、趋势分析
- ✅ **重试机制**: 网络异常、服务器错误自动重试，提升稳定性
- ✅ **断言工具**: 丰富的响应断言方法（AssertUtil）
- ✅ **环境管理**: 支持多环境配置切换，环境变量覆盖
- ✅ **异常处理**: 完善的错误处理和超时控制
- ✅ **安全防护**: 敏感信息自动脱敏，配置安全验证
- ✅ **配置管理**: 统一配置管理器，支持环境变量覆盖
- ✅ **精确异常**: 细化异常类型，提供详细错误上下文

## 📁 项目结构

```
rpm_auto/
├── common/                 # 公共模块
│   ├── request_util.py    # HTTP请求工具类（带重试、日志、脱敏）
│   ├── contract_api.py    # 合同管理API封装
│   ├── project_api.py     # 项目管理API封装
│   ├── assert_util.py     # 响应断言工具类
│   ├── config_manager.py  # 配置管理器（统一配置管理）
│   ├── security_util.py   # 安全工具类（敏感信息脱敏）
│   ├── exceptions.py      # 自定义异常类（精确错误处理）
│   └── logger.py          # 日志管理工具
├── config/                # 配置文件
│   ├── config.yaml        # 主配置文件
│   └── config.yaml.example # 配置文件示例
├── data/                  # 测试数据
│   └── contract_data.yaml # 合同管理测试数据
├── testcases/             # 测试用例
│   ├── test_contract.py   # 合同管理测试（创建、查询、更新等）
│   └── test_project.py    # 项目管理测试（CRUD、搜索等）
├── logs/                  # 日志文件目录（自动生成）
├── allure-results/        # Allure报告原始数据
├── conftest.py            # pytest配置和fixture
├── requirements.txt       # 依赖包列表
├── .gitignore            # Git忽略文件
└── README.md             # 项目说明文档
```

## 🛠 环境要求

- Python 3.7+
- pip
- Java 8+ (运行Allure报告需要)

## 📦 安装和配置

### 1. 克隆项目并安装依赖

```bash
# 克隆项目
git clone <your-repo-url>
cd rpm_auto

# 安装Python依赖
pip install -r requirements.txt
```

### 2. 安装Allure命令行工具

#### 方法一：通过Homebrew（推荐，如果可以访问外网）
```bash
brew install allure
```

#### 方法二：手动安装
1. 下载 [allure-commandline-2.13.2.tgz](https://github.com/allure-framework/allure2/releases)
2. 解压并配置环境变量：
```bash
tar -xzf allure-commandline-2.13.2.tgz
mv allure-2.13.2 ~/allure
echo 'export PATH=$PATH:~/allure/bin' >> ~/.zshrc
source ~/.zshrc
```

3. 验证安装：
```bash
allure --version
```

## ⚙️ 配置说明

### 基础配置

复制 `config/config.yaml.example` 为 `config/config.yaml` 并编辑：

```yaml
# 基础配置
base_url: "https://rpm-uat.pharmaronclinical.com"
username: "your_username"
password: "your_password"
captcha: "your_captcha"  # 万能验证码，请联系开发团队获取

# 请求配置
timeout: 30              # 请求超时时间（秒）
max_retries: 3           # 最大重试次数
verify_ssl: true         # 是否验证SSL证书

# 日志配置
log_level: "INFO"        # 日志级别: DEBUG, INFO, WARNING, ERROR
log_max_size: "10MB"     # 日志文件最大大小
log_backup_count: 5      # 日志文件备份数量

# Allure报告配置
allure_results_dir: "./allure-results"
allure_report_dir: "./allure-report"
allure_clean_results: true
```

### 环境变量支持

可通过环境变量覆盖配置：

```bash
export BASE_URL="https://your-api-url.com"
export USERNAME="your_username"
export PASSWORD="your_password"
export TEST_ENV="prod"  # 可指定配置文件后缀
export TIMEOUT="60"
export MAX_RETRIES="5"
```

### 多环境配置

支持环境特定配置文件：

```bash
# 开发环境
config/config_dev.yaml

# UAT环境
config/config_uat.yaml

# 生产环境
config/config_prod.yaml
```

使用方式：
```bash
# 指定环境
export TEST_ENV="uat"
pytest --alluredir=./allure-results
```

### 验证码配置

本框架支持自动获取验证码checkKey，但需要正确的验证码才能登录成功：

1. **万能验证码**：测试环境通常提供万能验证码，请联系开发团队获取
2. **验证码错误**：如果看到 `"code":"0019","message":"验证码错误"`，说明配置的验证码不正确
3. **自动识别**：可集成打码平台实现验证码自动识别（见开发指南）

## 🏃 运行测试

### 运行所有测试

```bash
pytest --alluredir=./allure-results
```

### 运行指定模块

```bash
# 运行合同管理测试
pytest testcases/test_contract.py --alluredir=./allure-results

# 运行项目管理测试
pytest testcases/test_project.py --alluredir=./allure-results
```

### 运行指定用例

```bash
# 运行创建合同测试
pytest testcases/test_contract.py::TestContract::test_create_contract -v

# 使用标记运行
pytest -m "critical" --alluredir=./allure-results
```

### 生成和查看Allure报告

```bash
# 运行测试并生成报告数据
pytest --alluredir=./allure-results

# 启动报告服务（会自动在浏览器中打开）
allure serve ./allure-results

# 或者生成静态报告
allure generate ./allure-results -o ./allure-report --clean
```

## 📊 日志和报告

### 日志系统

- **自动生成**：日志文件自动生成在 `logs/` 目录下
- **文件命名**：`test_YYYYMMDD.log`
- **详细记录**：包含请求响应、错误信息、执行时间等
- **敏感信息脱敏**：密码、token等自动脱敏显示
- **请求追踪**：每个请求都有唯一ID，便于问题排查

### Allure报告特性

- **中文支持**：测试用例、步骤、错误信息均为中文
- **详细步骤**：每个测试操作都有清晰的步骤记录
- **附件信息**：自动附加请求响应详情
- **趋势分析**：支持历史测试结果对比
- **严重级别**：用例按重要性分级（CRITICAL、NORMAL等）

## 🔧 开发指南

### 配置管理使用

框架提供了统一的配置管理器，支持多环境和环境变量覆盖：

```python
from common.config_manager import ConfigManager

# 获取配置管理器实例（单例模式）
config = ConfigManager()

# 获取API相关配置
api_config = config.get_api_config()
# 返回: {"base_url": "...", "timeout": 30, "max_retries": 3, ...}

# 获取认证相关配置
auth_config = config.get_auth_config()
# 返回: {"username": "...", "password": "...", "captcha": "..."}

# 获取日志相关配置
log_config = config.get_logging_config()

# 获取Allure相关配置
allure_config = config.get_allure_config()

# 获取单个配置项（支持嵌套键）
base_url = config.get("base_url")
db_host = config.get("database.host", "localhost")  # 支持默认值

# 设置配置项
config.set("custom.setting", "value")

# 验证必需配置
config.validate_required_config(["base_url", "username", "password"])

# 获取脱敏后的配置（用于日志记录）
safe_config = config.get_safe_config()
```

### 安全性和敏感信息处理

框架提供了全面的敏感信息脱敏功能：

```python
from common.security_util import SecurityUtil

# 自动脱敏任意数据结构
original_data = {
    "username": "testuser",
    "password": "secret123",
    "token": "abc123def456",
    "user_info": {
        "name": "张三",
        "auth_key": "sensitive_key"
    }
}

safe_data = SecurityUtil.sanitize_data(original_data)
# 结果: {
#     "username": "testuser",
#     "password": "s***3",
#     "token": "ab***56",
#     "user_info": {
#         "name": "张三",
#         "auth_key": "se***ey"
#     }
# }

# 脱敏字符串中的敏感信息
log_message = "用户登录: username=admin&password=123456&token=abc123"
safe_message = SecurityUtil.sanitize_data(log_message)
# 结果: "用户登录: username=admin&password=***&token=***"

# 验证配置安全性
security_issues = SecurityUtil.validate_config_security(config_dict)
if security_issues:
    for issue in security_issues:
        logger.warning(f"安全警告: {issue}")
```

### 异常处理和错误管理

框架提供了详细的异常分类，便于精确处理不同类型的错误：

```python
from common.exceptions import (
    APIRequestError, AuthenticationError, NetworkError, 
    ValidationError, ConfigurationError, TimeoutError
)
from common.request_util import RequestUtil

try:
    req = RequestUtil(base_url="https://api.example.com")
    response = req.send_request("POST", "/api/login", json=login_data)
    
except AuthenticationError as e:
    # 认证失败
    logger.error(f"认证失败: {e.message}")
    logger.error(f"用户名: {e.username}, 响应码: {e.response_code}")
    
except NetworkError as e:
    # 网络连接问题
    logger.error(f"网络错误: {e.message}")
    logger.error(f"URL: {e.url}, 重试次数: {e.retry_count}")
    
except TimeoutError as e:
    # 请求超时
    logger.error(f"请求超时: {e.message}")
    logger.error(f"超时时间: {e.timeout_seconds}秒, 操作: {e.operation}")
    
except APIRequestError as e:
    # API请求错误
    logger.error(f"API错误: {e.message}")
    logger.error(f"方法: {e.method}, URL: {e.url}, 状态码: {e.status_code}")
    
except ValidationError as e:
    # 数据验证错误
    logger.error(f"验证失败: {e.message}")
    logger.error(f"字段: {e.field_name}, 期望: {e.expected_value}, 实际: {e.actual_value}")
    
except ConfigurationError as e:
    # 配置错误
    logger.error(f"配置错误: {e.message}")
    logger.error(f"配置项: {e.config_key}")
```

### 接口出参数据校验

框架提供了丰富的响应数据校验方法，支持多种校验场景：

#### 1. 基础字段校验

```python
from common.assert_util import AssertUtil

# 简单字段值校验
AssertUtil.assert_response_field_value(response, "data.name", "期望的合同名称")

# 嵌套字段校验
AssertUtil.assert_nested_field_value(response, "data.user.name", "张三")

# 字段类型校验
AssertUtil.assert_field_type(response, "data.amount", int)

# 字段值范围校验
AssertUtil.assert_field_value_range(response, "data.amount", min_value=1000, max_value=100000)

# 字段包含子串校验
AssertUtil.assert_field_contains(response, "data.contract_no", "CT")
```

#### 2. 批量字段校验

```python
# 批量校验多个字段
field_expectations = {
    "code": "200",
    "data.status": "active", 
    "data.amount": 50000
}
AssertUtil.assert_multiple_fields(response, field_expectations)
```

#### 3. 使用数据校验器进行复杂校验

```python
from common.data_validator import DataValidator

# 创建校验器实例
validator = DataValidator(response)

# 校验数据结构
expected_schema = {
    "code": str,
    "data": dict,
    "total": int
}
validator.validate_schema(expected_schema)

# 校验业务规则
business_rules = [
    {"field": "data.amount", "operator": "gte", "value": 1000, "message": "金额不能小于1000"},
    {"field": "data.status", "operator": "in", "value": ["active", "pending"], "message": "状态值无效"}
]
validator.validate_business_rules(business_rules)
```

#### 4. 在YAML中定义期望值

```yaml
# data/contract_data.yaml
create_contract:
  expected_response:
    schema:
      code: str
      data: dict
    
    business_rules:
      - field: "data.id"
        operator: "gt"
        value: 0
        message: "合同ID必须大于0"
      
      - field: "data.status"
        operator: "in"
        value: ["draft", "active", "pending"]
        message: "合同状态必须在允许范围内"
```

#### 5. 支持的校验操作符

- **eq**: 等于
- **ne**: 不等于  
- **gt**: 大于
- **lt**: 小于
- **gte**: 大于等于
- **lte**: 小于等于
- **in**: 包含在列表中
- **not_in**: 不包含在列表中
- **contains**: 字符串包含
- **regex**: 正则表达式匹配
- **length**: 长度等于
- **min_length**: 最小长度
- **max_length**: 最大长度

### 添加新的API封装

1. 在 `common/` 目录下创建新的API封装类（如 `user_api.py`）：
```python
import allure
from common.logger import Logger
from common.config_manager import ConfigManager

logger = Logger().get_logger()

class UserAPI:
    def __init__(self, request_util):
        self.req = request_util
        self.config = ConfigManager()
    
    @allure.step("创建用户")
    def create_user(self, payload, headers):
        url = "/rpm-api/user/create"
        logger.info(f"创建用户请求: {payload}")
        response = self.req.send_request("POST", url, json=payload, headers=headers)
        logger.info(f"创建用户响应: {response.status_code}")
        return response
```

### 添加新的测试用例

1. 在 `testcases/` 目录下创建测试文件（如 `test_user.py`）：
```python
import allure
import pytest
from common.user_api import UserAPI
from common.assert_util import AssertUtil
from common.data_validator import DataValidator
from common.exceptions import APIRequestError, ValidationError

@allure.feature("用户管理")
class TestUser:
    
    @allure.story("创建用户")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user(self, req, headers):
        with allure.step("准备测试数据"):
            payload = {"name": "测试用户", "email": "test@example.com"}
        
        with allure.step("发送创建用户请求"):
            user_api = UserAPI(req)
            response = user_api.create_user(payload, headers)
        
        with allure.step("验证响应结果"):
            try:
                AssertUtil.assert_response_success(response)
                
                # 详细的字段校验
                AssertUtil.assert_nested_field_value(response, "data.name", "测试用户")
                AssertUtil.assert_field_type(response, "data.id", int)
                AssertUtil.assert_field_value_range(response, "data.id", min_value=1)
                
            except ValidationError as e:
                logger.error(f"数据验证失败: {e.message}")
                raise
            except APIRequestError as e:
                logger.error(f"API请求失败: {e.message}")
                raise
```

### 验证码自动识别集成

如需集成打码平台，可参考以下示例：

```python
# 在 conftest.py 中修改
@pytest.fixture(scope="session")
def captcha_and_checkkey(req):
    # 获取验证码图片
    response = req.send_request("GET", "/rpm-api/auth/generateCaptcha...")
    base64_image = response.json()["data"]["captchaBase64String"]
    
    # 调用打码平台识别
    captcha = recognize_captcha(base64_image)  # 你的识别函数
    return captcha, checkKey
```

## 🚨 常见问题

### 1. 登录失败："验证码错误"
- **原因**：config.yaml中的captcha配置错误
- **解决**：联系开发团队获取正确的万能验证码

### 2. 配置加载失败
- **原因**：配置文件格式错误或缺少必需配置项
- **解决**：检查YAML格式，确保必需配置项存在
- **日志**：查看详细的配置加载日志

### 3. 网络超时
- **原因**：网络不稳定或服务器响应慢
- **解决**：框架已内置重试机制，可调整timeout和max_retries配置

### 4. 敏感信息泄露
- **原因**：日志中包含明文密码或token
- **解决**：框架自动脱敏，如有遗漏请检查SecurityUtil配置

### 5. Allure报告打不开
- **原因**：Allure命令行工具未正确安装
- **解决**：按照安装指南重新安装Allure

### 6. 找不到模块错误
- **原因**：依赖包未安装或虚拟环境问题
- **解决**：`pip install -r requirements.txt`

## 📋 注意事项

1. **敏感信息**：请勿在代码中硬编码密码、token等敏感信息
2. **环境隔离**：不同环境使用不同的配置文件
3. **数据清理**：测试完成后及时清理测试数据
4. **并发测试**：注意并发测试时的数据冲突问题
5. **验证码有效期**：验证码checkKey有时效性，框架会自动重新获取
6. **配置安全**：定期检查配置文件安全性，避免敏感信息泄露
7. **异常处理**：使用框架提供的异常类型进行精确错误处理

## 🔒 安全特性

### 敏感信息保护
- ✅ 自动识别和脱敏敏感字段（password、token、key等）
- ✅ 支持多种数据格式的脱敏处理
- ✅ 配置文件安全性验证
- ✅ 日志输出自动脱敏

### 配置安全
- ✅ 环境变量覆盖机制，避免硬编码
- ✅ 配置文件示例模板
- ✅ 安全警告和检查机制

### 请求安全
- ✅ 请求追踪ID，便于问题排查
- ✅ 详细的异常分类和处理
- ✅ 自动重试和超时控制

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请提交 Issue 或联系项目维护者。

---

## 🏆 项目亮点

- **企业级**：完整的日志、报告、错误处理机制
- **安全性**：全面的敏感信息保护和配置安全验证
- **可维护**：清晰的代码结构和业务封装
- **可扩展**：易于添加新的API和测试场景
- **实用性**：解决了验证码、重试、环境切换等实际问题
- **专业性**：符合自动化测试最佳实践
- **稳定性**：详细的异常处理和重试机制
- **可观测**：完善的日志记录和请求追踪

## 📈 最新更新

### v2.0.0 - 企业级安全和配置管理
- ✅ 新增统一配置管理器（ConfigManager）
- ✅ 新增敏感信息脱敏工具（SecurityUtil）
- ✅ 新增详细异常分类体系
- ✅ 优化请求工具类，增强异常处理
- ✅ 改进conftest.py，集成新的配置和异常处理
- ✅ 增强安全性，自动脱敏敏感信息
- ✅ 支持多环境配置和环境变量覆盖
- ✅ 提供请求追踪ID，便于问题排查

### 升级指南
1. 复制新的配置文件示例：`cp config/config.yaml.example config/config.yaml`
2. 更新配置文件格式（参考上面的配置说明）
3. 安装新的依赖：`pip install -r requirements.txt`
4. 运行测试验证升级：`pytest --alluredir=./allure-results`
