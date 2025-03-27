#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from decimal import Decimal, ROUND_HALF_UP
from config import CONFIG

logger = logging.getLogger('taobao_price_checker.data_comparator')

class DataComparator:
    """数据比较类"""
    
    def __init__(self):
        self.price_precision = CONFIG['compare']['price_precision']
    
    def compare_prices(self, price1, price2):
        """
        比较两个价格是否相同
        
        Args:
            price1: 第一个价格
            price2: 第二个价格
            
        Returns:
            bool: 价格是否相同
        """
        try:
            # 转换为Decimal以确保精确比较
            p1 = self._to_decimal(price1)
            p2 = self._to_decimal(price2)
            
            if p1 is None or p2 is None:
                return False
            
            # 根据配置的精度进行比较
            p1 = p1.quantize(Decimal(f'0.{"0" * self.price_precision}'), 
                            rounding=ROUND_HALF_UP)
            p2 = p2.quantize(Decimal(f'0.{"0" * self.price_precision}'), 
                            rounding=ROUND_HALF_UP)
            
            return p1 == p2
            
        except Exception as e:
            logger.error(f"比较价格时出错: {str(e)}")
            return False
    
    def compare_skus(self, sku1, sku2):
        """
        比较两个SKU是否相同
        
        Args:
            sku1: 第一个SKU
            sku2: 第二个SKU
            
        Returns:
            bool: SKU是否相同
        """
        try:
            # 确保输入是字符串
            s1 = str(sku1).strip().upper()
            s2 = str(sku2).strip().upper()
            
            # 空字符串视为不相同
            if not s1 or not s2:
                return False
            
            return s1 == s2
            
        except Exception as e:
            logger.error(f"比较SKU时出错: {str(e)}")
            return False
    
    def _to_decimal(self, value):
        """
        将输入值转换为Decimal类型
        
        Args:
            value: 要转换的值（可以是字符串、整数或浮点数）
            
        Returns:
            Decimal: 转换后的Decimal对象，如果转换失败返回None
        """
        try:
            if isinstance(value, (int, float)):
                return Decimal(str(value))
            elif isinstance(value, str):
                # 移除可能的货币符号和空白字符
                value = value.strip().replace('¥', '').replace('￥', '')
                return Decimal(value)
            elif isinstance(value, Decimal):
                return value
            else:
                logger.warning(f"无法转换的价格类型: {type(value)}")
                return None
        except Exception as e:
            logger.error(f"转换价格时出错: {str(e)}")
            return None
    
    def format_price(self, price):
        """
        格式化价格为指定精度的字符串
        
        Args:
            price: 要格式化的价格
            
        Returns:
            str: 格式化后的价格字符串
        """
        try:
            decimal_price = self._to_decimal(price)
            if decimal_price is None:
                return "0.00"
            
            # 格式化为指定精度的字符串
            format_str = f"0.{'0' * self.price_precision}"
            return str(decimal_price.quantize(Decimal(format_str), 
                                           rounding=ROUND_HALF_UP))
            
        except Exception as e:
            logger.error(f"格式化价格时出错: {str(e)}")
            return "0.00"
