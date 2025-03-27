#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
配置文件，包含应用程序的各种参数设置
"""

# 淘宝价格爬取相关配置
CONFIG = {
    # 浏览器配置
    "browser": {
        "headless": False,  # 是否启用无头模式 (True为不显示浏览器界面)
        "timeout": 30,      # 页面加载超时时间(秒)
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "window_size": {
            "width": 1366,
            "height": 768
        }
    },
    
    # 价格获取配置
    "price": {
        # 价格XPath模板，其中{panel_id}将被替换为实际面板ID
        "panel_class": "class=\"purchasePanel--cG3DU6bX normalPanel--tH79cfP4 normalPanel  \"",
        "xpath_template": "//*[@id=\"{panel_id}\"]/div[2]/div[3]/div/div/div[1]/span[3]"
    },
    
    # SKU获取配置
    "sku": {
        "class_name": "valueItemText--HiKnUqGa f-els-1"
    },
    
    # Excel配置
    "excel": {
        "sheet_name": "Sheet1",
        "columns": {
            "link_a": "链接A",
            "sku_a": "A店SKU",
            "link_b": "链接B",
            "sku_b": "B店SKU"
        }
    },
    
    # 任务配置
    "task": {
        "default_interval": 60,  # 默认任务间隔(分钟)
        "retry_times": 3,        # 失败重试次数
        "retry_delay": 5         # 重试间隔(秒)
    },
    
    # 比较配置
    "compare": {
        "price_precision": 2     # 价格比较精度(小数位数)
    },
    
    # 日志配置
    "log": {
        "level": "INFO",
        "file": "logs/app.log",
        "max_size": 10 * 1024 * 1024,  # 10MB
        "backup_count": 5
    }
}

# XPath解析辅助函数
def get_price_xpath(panel_id):
    """生成价格的XPath"""
    return CONFIG["price"]["xpath_template"].format(panel_id=panel_id)

# SKU元素选择器
def get_sku_selector():
    """获取SKU元素选择器"""
    return f"[class='{CONFIG['sku']['class_name']}']"
