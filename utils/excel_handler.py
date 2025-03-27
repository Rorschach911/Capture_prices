#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import pandas as pd
from config import CONFIG

logger = logging.getLogger('taobao_price_checker.excel_handler')

class ExcelHandler:
    """Excel文件处理类"""
    
    def __init__(self):
        self.sheet_name = CONFIG['excel']['sheet_name']
        self.columns = CONFIG['excel']['columns']
    
    def read_excel(self, file_path):
        """
        读取Excel文件数据
        
        Args:
            file_path: Excel文件路径
            
        Returns:
            list: 包含每行数据的字典列表，如果出错返回空列表
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"Excel文件不存在: {file_path}")
                return []
            
            # 读取Excel文件
            df = pd.read_excel(file_path, sheet_name=self.sheet_name)
            
            # 检查必要的列是否存在
            required_columns = list(self.columns.values())
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                logger.error(f"Excel文件缺少必要的列: {', '.join(missing_columns)}")
                return []
            
            # 转换为字典列表
            data = []
            for _, row in df.iterrows():
                row_dict = {}
                for key, col_name in self.columns.items():
                    row_dict[col_name] = str(row[col_name]).strip()
                data.append(row_dict)
            
            logger.info(f"成功读取Excel文件，共{len(data)}行数据")
            return data
            
        except Exception as e:
            logger.error(f"读取Excel文件出错: {str(e)}")
            return []
    
    def save_results(self, file_path, results):
        """
        保存比较结果到Excel文件
        
        Args:
            file_path: 保存的Excel文件路径
            results: 比较结果数据列表
        """
        try:
            # 创建DataFrame
            df = pd.DataFrame(results)
            
            # 重命名列
            column_mapping = {
                'sequence': '序号',
                'a_price': '本店价格',
                'a_sku': '本店SKU',
                'b_price': '竞店价格',
                'b_sku': '竞店SKU'
            }
            df = df.rename(columns=column_mapping)
            
            # 保存到Excel
            df.to_excel(file_path, sheet_name='比较结果', index=False)
            logger.info(f"结果已保存到: {file_path}")
            
        except Exception as e:
            logger.error(f"保存结果到Excel文件出错: {str(e)}")
    
    def validate_excel(self, file_path):
        """
        验证Excel文件格式是否正确
        
        Args:
            file_path: Excel文件路径
            
        Returns:
            bool: 验证是否通过
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"Excel文件不存在: {file_path}")
                return False
            
            # 读取Excel文件
            df = pd.read_excel(file_path, sheet_name=self.sheet_name)
            
            # 检查必要的列
            required_columns = list(self.columns.values())
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                logger.error(f"Excel文件缺少必要的列: {', '.join(missing_columns)}")
                return False
            
            # 检查是否有空值
            for col in required_columns:
                if df[col].isnull().any():
                    logger.warning(f"列 '{col}' 存在空值")
            
            return True
            
        except Exception as e:
            logger.error(f"验证Excel文件出错: {str(e)}")
            return False
