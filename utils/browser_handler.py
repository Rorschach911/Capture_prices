#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import CONFIG

logger = logging.getLogger('taobao_price_checker.browser_handler')

class BrowserHandler:
    """浏览器操作处理类"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BrowserHandler, cls).__new__(cls)
            cls._instance.driver = None
            cls._instance.wait = None
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
    
    def setup_browser(self):
        """初始化浏览器"""
        if self.driver is not None:
            return
            
        try:
            # 设置Chrome选项
            options = webdriver.ChromeOptions()
            
            # 设置User-Agent
            options.add_argument(f'user-agent={CONFIG["browser"]["user_agent"]}')
            
            # 设置窗口大小
            options.add_argument(f'window-size={CONFIG["browser"]["window_size"]["width"]},'
                               f'{CONFIG["browser"]["window_size"]["height"]}')
            
            # 无头模式设置
            if CONFIG["browser"]["headless"]:
                options.add_argument('--headless')
            
            # 其他常用设置
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-infobars')
            
            # 创建浏览器实例
            self.driver = webdriver.Chrome(options=options)
            
            # 设置等待对象
            self.wait = WebDriverWait(
                self.driver, 
                CONFIG["browser"]["timeout"]
            )
            
            logger.info("浏览器初始化成功")
            
        except Exception as e:
            logger.error(f"浏览器初始化失败: {str(e)}")
            raise
    
    def get_page(self, url):
        """
        打开指定URL的页面
        
        Args:
            url: 要打开的网页URL
            
        Returns:
            bool: 是否成功打开页面
        """
        try:
            self.driver.get(url)
            return True
        except Exception as e:
            logger.error(f"打开页面失败 {url}: {str(e)}")
            return False
    
    def find_element_by_xpath(self, xpath, timeout=None):
        """
        通过XPath查找元素
        
        Args:
            xpath: XPath表达式
            timeout: 超时时间（秒），None则使用默认值
            
        Returns:
            WebElement: 找到的元素，如果未找到返回None
        """
        try:
            if timeout is None:
                timeout = CONFIG["browser"]["timeout"]
            
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element
        except TimeoutException:
            logger.warning(f"等待元素超时 (XPath: {xpath})")
            return None
        except Exception as e:
            logger.error(f"查找元素失败 (XPath: {xpath}): {str(e)}")
            return None
    
    def find_element_by_class(self, class_name, timeout=None):
        """
        通过class名称查找元素
        
        Args:
            class_name: 类名
            timeout: 超时时间（秒），None则使用默认值
            
        Returns:
            WebElement: 找到的元素，如果未找到返回None
        """
        try:
            if timeout is None:
                timeout = CONFIG["browser"]["timeout"]
            
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
            return element
        except TimeoutException:
            logger.warning(f"等待元素超时 (class: {class_name})")
            return None
        except Exception as e:
            logger.error(f"查找元素失败 (class: {class_name}): {str(e)}")
            return None
    
    def find_element_by_selector(self, selector, timeout=None):
        """
        通过CSS选择器查找元素
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（秒），None则使用默认值
            
        Returns:
            WebElement: 找到的元素，如果未找到返回None
        """
        try:
            if timeout is None:
                timeout = CONFIG["browser"]["timeout"]
            
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element
        except TimeoutException:
            logger.warning(f"等待元素超时 (selector: {selector})")
            return None
        except Exception as e:
            logger.error(f"查找元素失败 (selector: {selector}): {str(e)}")
            return None
    
    def get_element_text(self, element):
        """
        获取元素的文本内容
        
        Args:
            element: WebElement对象
            
        Returns:
            str: 元素的文本内容，如果失败返回空字符串
        """
        try:
            if element is None:
                return ""
            return element.text.strip()
        except Exception as e:
            logger.error(f"获取元素文本失败: {str(e)}")
            return ""
    
    def wait_for_element(self, by, value, timeout=None):
        """
        等待元素出现
        
        Args:
            by: 定位方式（By.ID, By.CLASS_NAME等）
            value: 定位值
            timeout: 超时时间（秒），None则使用默认值
            
        Returns:
            WebElement: 找到的元素，如果未找到返回None
        """
        try:
            if timeout is None:
                timeout = CONFIG["browser"]["timeout"]
            
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.warning(f"等待元素超时 ({by}: {value})")
            return None
        except Exception as e:
            logger.error(f"等待元素失败 ({by}: {value}): {str(e)}")
            return None
    
    def close(self):
        """关闭浏览器"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("浏览器已关闭")
        except Exception as e:
            logger.error(f"关闭浏览器失败: {str(e)}")
    
    def __del__(self):
        """析构函数，确保浏览器被关闭"""
        self.close()

# 创建单例实例，但不初始化浏览器
browser = BrowserHandler()
