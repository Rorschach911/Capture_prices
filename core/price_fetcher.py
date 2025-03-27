#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
from bs4 import BeautifulSoup
from utils.browser_handler import browser
from config import CONFIG, get_price_xpath

logger = logging.getLogger('taobao_price_checker.price_fetcher')

class PriceFetcher:
    """价格获取类"""
    
    def __init__(self):
        self.retry_times = CONFIG['task']['retry_times']
        self.retry_delay = CONFIG['task']['retry_delay']
    
    def get_price(self, url):
        """
        从淘宝页面获取价格
        
        Args:
            url: 商品页面URL
            
        Returns:
            float: 商品价格，如果获取失败返回0.0
        """
        try:
            # 打开页面
            if not browser.get_page(url):
                logger.error(f"无法打开页面: {url}")
                return 0.0
            
            # 获取价格面板ID
            panel_id = self._get_panel_id()
            if not panel_id:
                logger.error("无法获取价格面板ID")
                return 0.0
            
            # 使用XPath获取价格
            xpath = get_price_xpath(panel_id)
            price_element = browser.find_element_by_xpath(xpath)
            
            if price_element is None:
                logger.error("无法找到价格元素")
                return 0.0
            
            # 获取价格文本并处理
            price_text = browser.get_element_text(price_element)
            return self._parse_price(price_text)
            
        except Exception as e:
            logger.error(f"获取价格时出错: {str(e)}")
            return 0.0
    
    def _get_panel_id(self):
        """
        获取价格面板的ID
        
        Returns:
            str: 面板ID，如果获取失败返回None
        """
        try:
            # 查找具有特定class的元素
            panel_class = CONFIG['price']['panel_class']
            panel = browser.find_element_by_class(panel_class.replace('class=', '').strip('"'))
            
            if panel:
                # 从元素的id属性中提取ID
                panel_id = panel.get_attribute('id')
                if panel_id:
                    return panel_id
            
            # 如果上面的方法失败，尝试从页面源码中提取
            page_source = browser.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            panel = soup.find('div', {'class': panel_class.replace('class=', '').strip('"')})
            
            if panel and 'id' in panel.attrs:
                return panel['id']
            
            return None
            
        except Exception as e:
            logger.error(f"获取价格面板ID时出错: {str(e)}")
            return None
    
    def _parse_price(self, price_text):
        """
        解析价格文本
        
        Args:
            price_text: 价格文本
            
        Returns:
            float: 解析后的价格，如果解析失败返回0.0
        """
        try:
            if not price_text:
                return 0.0
            
            # 移除非数字字符（保留小数点）
            price_text = re.sub(r'[^\d.]', '', price_text)
            
            # 转换为浮点数
            price = float(price_text)
            
            # 根据配置的精度处理小数位数
            precision = CONFIG['compare']['price_precision']
            return round(price, precision)
            
        except (ValueError, TypeError) as e:
            logger.error(f"解析价格文本时出错: {str(e)}")
            return 0.0
