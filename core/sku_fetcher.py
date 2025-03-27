#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
from utils.browser_handler import browser
from config import CONFIG, get_sku_selector

logger = logging.getLogger('taobao_price_checker.sku_fetcher')

class SkuFetcher:
    """SKU获取类"""
    
    def __init__(self):
        self.retry_times = CONFIG['task']['retry_times']
        self.retry_delay = CONFIG['task']['retry_delay']
    
    def get_sku(self, url):
        """
        从淘宝页面获取SKU
        
        Args:
            url: 商品页面URL
            
        Returns:
            str: 商品SKU，如果获取失败返回空字符串
        """
        try:
            # 打开页面
            if not browser.get_page(url):
                logger.error(f"无法打开页面: {url}")
                return ""
            
            # 获取SKU元素
            selector = get_sku_selector()
            sku_element = browser.find_element_by_selector(selector)
            
            if sku_element is None:
                logger.error("无法找到SKU元素")
                return ""
            
            # 获取SKU文本
            sku_text = browser.get_element_text(sku_element)
            return self._clean_sku(sku_text)
            
        except Exception as e:
            logger.error(f"获取SKU时出错: {str(e)}")
            return ""
    
    def _clean_sku(self, sku_text):
        """
        清理SKU文本
        
        Args:
            sku_text: SKU文本
            
        Returns:
            str: 清理后的SKU文本
        """
        try:
            if not sku_text:
                return ""
            
            # 移除空白字符
            sku = sku_text.strip()
            
            # 移除可能的前缀（如"SKU："）
            if ':' in sku:
                sku = sku.split(':')[-1].strip()
            elif '：' in sku:
                sku = sku.split('：')[-1].strip()
            
            return sku
            
        except Exception as e:
            logger.error(f"清理SKU文本时出错: {str(e)}")
            return ""
    
    def get_sku_with_retry(self, url):
        """
        带重试机制的SKU获取
        
        Args:
            url: 商品页面URL
            
        Returns:
            str: 商品SKU，如果所有重试都失败则返回空字符串
        """
        for attempt in range(self.retry_times):
            try:
                sku = self.get_sku(url)
                if sku:
                    return sku
                
                # 如果获取失败且不是最后一次尝试，等待后重试
                if attempt < self.retry_times - 1:
                    logger.warning(f"获取SKU失败，{self.retry_delay}秒后进行第{attempt + 2}次尝试")
                    time.sleep(self.retry_delay)
                
            except Exception as e:
                logger.error(f"第{attempt + 1}次获取SKU时出错: {str(e)}")
                if attempt < self.retry_times - 1:
                    time.sleep(self.retry_delay)
        
        logger.error(f"在{self.retry_times}次尝试后仍无法获取SKU")
        return ""
