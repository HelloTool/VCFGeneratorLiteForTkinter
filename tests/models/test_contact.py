import pytest
from vcf_generator_lite.models.contact import parse_contact, Contact


class TestParseContact:
    # 正常情况测试
    def test_valid_contact_with_note(self):
        """测试包含备注的联系人信息"""
        result = parse_contact("张三 13800138000 同事")
        assert result == Contact("张三", "13800138000", "同事")

    def test_valid_contact_without_note(self):
        """测试无备注的联系人信息"""
        result = parse_contact("李四 13912345678")
        assert result == Contact("李四", "13912345678", None)

    def test_name_with_spaces(self):
        """测试姓名包含空格的情况"""
        result = parse_contact("张 三 丰 15011223344 武术大师")
        assert result == Contact("张 三 丰", "15011223344", "武术大师")

    # 异常情况测试
    def test_missing_phone(self):
        """测试缺少有效手机号的情况"""
        with pytest.raises(ValueError):
            parse_contact("王五 123456 工程师")

    def test_insufficient_parts(self):
        """测试输入少于两个部分的情况"""
        with pytest.raises(ValueError):
            parse_contact("赵六")

    def test_multiple_phones(self):
        """测试包含多个手机号的情况（应使用第一个有效手机号）"""
        result = parse_contact("钱七 13111111111 13222222222 备用号码")
        assert result == Contact("钱七", "13111111111", "13222222222 备用号码")
