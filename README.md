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

## 📁 项目结构

```
rpm_auto/
├── common/                 # 公共模块
│   ├── request_util.py    # HTTP请求工具类（带重试、日志、脱敏）
│   ├── contract_api.py    # 合同管理API封装
│   ├── project_api.py     # 项目管理API封装
│   ├── assert_util.py     # 响应断言工具类
│   └── logger.py          # 日志管理工具
├── config/                # 配置文件
│   └── config.yaml        # 主配置文件
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

编辑 `config/config.yaml` 文件：

```yaml
base_url: "https://rpm-uat.pharmaronclinical.com"
username: "your_username"
password: "your_password"
captcha: "your_captcha"  # 万能验证码，请联系开发团队获取
```

### 环境变量支持

可通过环境变量覆盖配置：

```bash
export BASE_URL="https://your-api-url.com"
export USERNAME="your_username"
export PASSWORD="your_password"
export TEST_ENV="prod"  # 可指定配置文件后缀
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

### Allure报告特性

- **中文支持**：测试用例、步骤、错误信息均为中文
- **详细步骤**：每个测试操作都有清晰的步骤记录
- **附件信息**：自动附加请求响应详情
- **趋势分析**：支持历史测试结果对比
- **严重级别**：用例按重要性分级（CRITICAL、NORMAL等）

## 🔧 开发指南

### 添加新的API封装

1. 在 `common/` 目录下创建新的API封装类（如 `user_api.py`）：
```python
import allure
from common.logger import Logger

logger = Logger().get_logger()

class UserAPI:
    def __init__(self, request_util):
        self.req = request_util
    
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
            AssertUtil.assert_response_success(response)
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

### 2. 网络超时
- **原因**：网络不稳定或服务器响应慢
- **解决**：框架已内置重试机制，可在request_util.py中调整重试次数

### 3. Allure报告打不开
- **原因**：Allure命令行工具未正确安装
- **解决**：按照安装指南重新安装Allure

### 4. 找不到模块错误
- **原因**：依赖包未安装或虚拟环境问题
- **解决**：`pip install -r requirements.txt`

## 📋 注意事项

1. **敏感信息**：请勿在代码中硬编码密码、token等敏感信息
2. **环境隔离**：不同环境使用不同的配置文件
3. **数据清理**：测试完成后及时清理测试数据
4. **并发测试**：注意并发测试时的数据冲突问题
5. **验证码有效期**：验证码checkKey有时效性，框架会自动重新获取

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
- **可维护**：清晰的代码结构和业务封装
- **可扩展**：易于添加新的API和测试场景
- **实用性**：解决了验证码、重试、环境切换等实际问题
- **专业性**：符合自动化测试最佳实践
