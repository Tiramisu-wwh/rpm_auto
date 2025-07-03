"""
响应断言工具类
"""
import allure
from common.logger import Logger

logger = Logger().get_logger()

class AssertUtil:
    """API响应断言工具类"""
    
    @staticmethod
    @allure.step("断言响应状态码为200")
    def assert_status_code_200(response):
        """断言响应状态码为200"""
        assert response.status_code == 200, f"期望状态码200，实际状态码{response.status_code}"
        logger.info(f"状态码断言成功: {response.status_code}")
    
    @staticmethod
    @allure.step("断言响应成功")
    def assert_response_success(response):
        """断言响应成功（状态码200且code为200）"""
        AssertUtil.assert_status_code_200(response)
        response_json = response.json()
        assert response_json.get("code") == "200", f"期望code为200，实际为{response_json.get('code')}"
        logger.info(f"响应成功断言通过: code={response_json.get('code')}")
    
    @staticmethod
    @allure.step("断言响应包含指定字段")
    def assert_response_contains_field(response, field_name):
        """断言响应包含指定字段"""
        response_json = response.json()
        assert field_name in response_json, f"响应中缺少字段: {field_name}"
        logger.info(f"字段存在断言通过: {field_name}")
    
    @staticmethod
    @allure.step("断言响应字段值")
    def assert_response_field_value(response, field_name, expected_value):
        """断言响应字段值"""
        response_json = response.json()
        actual_value = response_json.get(field_name)
        assert actual_value == expected_value, f"字段{field_name}期望值为{expected_value}，实际值为{actual_value}"
        logger.info(f"字段值断言通过: {field_name}={actual_value}")
    
    @staticmethod
    @allure.step("断言响应数据不为空")
    def assert_response_data_not_empty(response):
        """断言响应数据不为空"""
        response_json = response.json()
        data = response_json.get("data")
        assert data is not None, "响应data字段为空"
        if isinstance(data, list):
            assert len(data) > 0, "响应data列表为空"
        logger.info("响应数据非空断言通过")
    
    @staticmethod
    @allure.step("断言响应错误")
    def assert_response_error(response, expected_code=None, expected_message=None):
        """断言响应为错误状态"""
        response_json = response.json()
        code = response_json.get("code")
        
        # 断言不是成功状态
        assert code != "200", f"期望错误响应，但得到成功响应: code={code}"
        
        if expected_code:
            assert code == expected_code, f"期望错误码{expected_code}，实际错误码{code}"
        
        if expected_message:
            message = response_json.get("message", "")
            assert expected_message in message, f"期望错误信息包含'{expected_message}'，实际信息'{message}'"
        
        logger.info(f"错误响应断言通过: code={code}")
    
    @staticmethod
    def assert_list_length(actual_list, expected_length):
        """断言列表长度"""
        assert len(actual_list) == expected_length, f"期望列表长度{expected_length}，实际长度{len(actual_list)}"
        logger.info(f"列表长度断言通过: {len(actual_list)}")
    
    @staticmethod
    def assert_dict_contains_keys(actual_dict, expected_keys):
        """断言字典包含指定键"""
        for key in expected_keys:
            assert key in actual_dict, f"字典中缺少键: {key}"
        logger.info(f"字典键存在断言通过: {expected_keys}") 