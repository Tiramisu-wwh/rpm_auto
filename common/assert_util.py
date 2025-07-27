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
    @allure.step("断言响应字段值")
    def assert_response_field_value(response, field_name, expected_value):
        """断言响应字段值"""
        response_json = response.json()
        actual_value = response_json.get(field_name)
        assert actual_value == expected_value, f"字段{field_name}期望值为{expected_value}，实际值为{actual_value}"
        logger.info(f"字段值断言通过: {field_name}={actual_value}")

    @staticmethod
    @allure.step("断言嵌套字段值")
    def assert_nested_field_value(response, field_path, expected_value):
        """断言嵌套字段值，支持 data.user.name 格式"""
        response_json = response.json()
        actual_value = response_json

        # 按路径逐层获取值
        for field in field_path.split('.'):
            if isinstance(actual_value, dict) and field in actual_value:
                actual_value = actual_value[field]
            else:
                assert False, f"字段路径 {field_path} 不存在"

        assert actual_value == expected_value, f"字段{field_path}期望值为{expected_value}，实际值为{actual_value}"
        logger.info(f"嵌套字段值断言通过: {field_path}={actual_value}")

    @staticmethod
    @allure.step("断言字段值类型")
    def assert_field_type(response, field_name, expected_type):
        """断言字段值类型"""
        response_json = response.json()
        actual_value = response_json.get(field_name)
        assert isinstance(actual_value, expected_type), f"字段{field_name}期望类型{expected_type.__name__}，实际类型{type(actual_value).__name__}"
        logger.info(f"字段类型断言通过: {field_name} 类型为 {type(actual_value).__name__}")

    @staticmethod
    @allure.step("断言字段值范围")
    def assert_field_value_range(response, field_name, min_value=None, max_value=None):
        """断言字段值在指定范围内"""
        response_json = response.json()
        actual_value = response_json.get(field_name)

        if min_value is not None:
            assert actual_value >= min_value, f"字段{field_name}值{actual_value}小于最小值{min_value}"

        if max_value is not None:
            assert actual_value <= max_value, f"字段{field_name}值{actual_value}大于最大值{max_value}"

        logger.info(f"字段范围断言通过: {field_name}={actual_value}")

    @staticmethod
    @allure.step("断言字段值包含子串")
    def assert_field_contains(response, field_name, expected_substring):
        """断言字段值包含指定子串"""
        response_json = response.json()
        actual_value = str(response_json.get(field_name, ""))
        assert expected_substring in actual_value, f"字段{field_name}值'{actual_value}'不包含'{expected_substring}'"
        logger.info(f"字段包含断言通过: {field_name} 包含 '{expected_substring}'")

    @staticmethod
    @allure.step("批量断言字段值")
    def assert_multiple_fields(response, field_expectations):
        """批量断言多个字段值

        Args:
            response: HTTP响应对象
            field_expectations: 字段期望值字典，格式：{"field_name": expected_value}
        """
        response_json = response.json()
        failed_assertions = []

        for field_name, expected_value in field_expectations.items():
            actual_value = response_json.get(field_name)
            if actual_value != expected_value:
                failed_assertions.append(f"字段{field_name}期望值{expected_value}，实际值{actual_value}")

        if failed_assertions:
            assert False, f"批量断言失败: {'; '.join(failed_assertions)}"

        logger.info(f"批量字段断言通过: {list(field_expectations.keys())}")

    @staticmethod
    @allure.step("断言响应包含字段")
    def assert_response_contains_field(response, field_name):
        """断言响应包含指定字段"""
        response_json = response.json()
        assert field_name in response_json, f"响应中缺少字段: {field_name}"
        logger.info(f"字段存在断言通过: {field_name}")