#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
from datetime import datetime
import threading
import time

from PyQt5.QtWidgets import (QApplication, QMessageBox, QTableWidgetItem)
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, Qt

from ui import (MainWindow, PriceDifferentAlert, SkuDifferentAlert, 
               LocalSkuDifferentAlert, CompetitorSkuDifferentAlert)
from utils.excel_handler import ExcelHandler
from core.price_fetcher import PriceFetcher
from core.sku_fetcher import SkuFetcher
from core.data_comparator import DataComparator
from config import CONFIG
from utils.browser_handler import browser

# 确保应用程序只有一个实例
app = None

# 配置日志
def setup_logging():
    """设置日志"""
    try:
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, 'app.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('taobao_price_checker')
    except Exception as e:
        print(f"设置日志时出错: {str(e)}")
        sys.exit(1)


class SignalBridge(QObject):
    """信号桥接器，用于在线程间传递信号"""
    update_progress = pyqtSignal(int)
    task_completed = pyqtSignal()
    show_price_alert = pyqtSignal()
    show_sku_alert = pyqtSignal()
    show_local_sku_alert = pyqtSignal()
    show_competitor_sku_alert = pyqtSignal()
    update_table = pyqtSignal(list)


class PriceCheckerApp:
    """淘宝价格检查应用程序主类"""
    def __init__(self):
        global app
        self.logger = setup_logging()
        
        # 确保只创建一个QApplication实例
        if app is None:
            app = QApplication(sys.argv)
        self.app = app
        
        try:
            self.main_window = MainWindow()
            self.signals = SignalBridge()
            
            # 连接信号到槽
            self.setup_signals()
            
            # 工作线程
            self.worker_thread = None
            self.is_running = False
            self.selected_file = None
            self.run_count = 0  # 初始化运行次数
            
            # 数据处理器
            self.excel_handler = ExcelHandler()
            self.price_fetcher = PriceFetcher()
            self.sku_fetcher = SkuFetcher()
            self.data_comparator = DataComparator()
            
            # 记录任务时间
            self.first_run_time = None
            self.last_run_time = None
            
            self.logger.info("应用程序初始化完成")
            
        except Exception as e:
            self.logger.error(f"初始化应用程序时出错: {str(e)}")
            raise
    
    def setup_signals(self):
        """设置信号连接"""
        try:
            # 主窗口信号
            self.main_window.execute_button.clicked.connect(self.start_task)
            
            # 桥接信号
            self.signals.update_progress.connect(self.main_window.update_progress)
            self.signals.task_completed.connect(self.main_window.task_completed)
            self.signals.show_price_alert.connect(self.show_price_alert)
            self.signals.show_sku_alert.connect(self.show_sku_alert)
            self.signals.show_local_sku_alert.connect(self.show_local_sku_alert)
            self.signals.show_competitor_sku_alert.connect(self.show_competitor_sku_alert)
            self.signals.update_table.connect(self.main_window.update_table)
                
        except Exception as e:
            self.logger.error(f"设置信号连接时出错: {str(e)}")
            raise
    
    def start_task(self):
        """启动任务"""
        try:
            if not self.main_window.selected_file:
                self.logger.warning("未选择Excel文件")
                QMessageBox.warning(self.main_window, "警告", "请先选择Excel文件！")
                return
            
            if self.is_running:
                self.logger.warning("任务已在运行中")
                return
            
            self.is_running = True
            self.selected_file = self.main_window.selected_file
            self.run_count += 1
            
            # 更新运行次数显示
            self.main_window.current_run_label.setText(f"本次是第{self.run_count}次任务执行")
            
            # 更新时间显示
            current_time = datetime.now()
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M")
            
            if self.run_count == 1:
                self.first_run_time = current_time
                self.main_window.first_time_label.setText(f"任务第一次执行时间:    {current_time_str}")
            
            self.last_run_time = current_time
            self.main_window.last_time_label.setText(f"任务上一次执行时间:    {current_time_str}")
            
            # 重置进度条
            self.main_window.progress_bar.setValue(0)
            
            # 清空表格
            self.main_window.table.setRowCount(0)
            
            # 创建并启动工作线程
            self.worker_thread = threading.Thread(target=self.run_task)
            self.worker_thread.daemon = True
            self.worker_thread.start()
            
            # 设置下一次任务的定时器
            try:
                interval_minutes = int(self.main_window.interval_input.text())
                if interval_minutes > 0:
                    QTimer.singleShot(interval_minutes * 60 * 1000, self.start_task)
            except ValueError:
                pass
            
            self.logger.info("任务已启动")
            
        except Exception as e:
            self.logger.error(f"启动任务时出错: {str(e)}")
            self.is_running = False
            raise
    
    def run_task(self):
        """执行任务的主要逻辑"""
        try:
            # 读取Excel文件
            data = self.excel_handler.read_excel(self.selected_file)
            if not data:
                self.logger.error("无法读取Excel文件")
                return
            
            # 初始化浏览器
            browser.setup_browser()
            
            total_items = len(data)
            results = []
            
            for i, item in enumerate(data, 1):
                # 更新进度
                progress = int((i / total_items) * 100)
                self.signals.update_progress.emit(progress)
                
                # 获取价格和SKU信息
                a_price = self.price_fetcher.get_price(item['link_a'])
                b_price = self.price_fetcher.get_price(item['link_b'])
                a_sku = self.sku_fetcher.get_sku(item['link_a'])
                b_sku = self.sku_fetcher.get_sku(item['link_b'])
                
                # 比较数据
                result = {
                    'sequence': i,
                    'a_price': a_price,
                    'b_price': b_price,
                    'a_sku': a_sku,
                    'b_sku': b_sku
                }
                
                # 检查价格差异
                if self.data_comparator.check_price_difference(a_price, b_price):
                    self.signals.show_price_alert.emit()
                
                # 检查SKU差异
                if self.data_comparator.check_sku_difference(a_sku, b_sku):
                    self.signals.show_sku_alert.emit()
                    
                    # 检查具体的SKU差异类型
                    if self.data_comparator.check_local_sku_difference(a_sku):
                        self.signals.show_local_sku_alert.emit()
                    if self.data_comparator.check_competitor_sku_difference(b_sku):
                        self.signals.show_competitor_sku_alert.emit()
                
                results.append(result)
                
                # 每处理一项后更新表格
                self.signals.update_table.emit(results)
                
                # 添加延时避免请求过快
                time.sleep(CONFIG['request_delay'])
            
            self.signals.task_completed.emit()
            self.logger.info("任务执行完成")
            
        except Exception as e:
            self.logger.error(f"执行任务时出错: {str(e)}")
        finally:
            self.is_running = False
            # 关闭浏览器
            try:
                browser.close()
            except Exception as e:
                self.logger.error(f"关闭浏览器时出错: {str(e)}")
    
    def update_table(self, results):
        """更新表格数据"""
        try:
            if not hasattr(self.main_window, 'table'):
                self.logger.error("主窗口缺少table组件")
                return
            
            table = self.main_window.table
            for row, result in enumerate(results):
                table.setItem(row, 0, QTableWidgetItem(str(result['sequence'])))
                table.setItem(row, 1, QTableWidgetItem(str(result['a_price'])))
                table.setItem(row, 2, QTableWidgetItem(str(result['a_sku'])))
                table.setItem(row, 3, QTableWidgetItem(str(result['b_price'])))
                table.setItem(row, 4, QTableWidgetItem(str(result['b_sku'])))
                
            table.resizeColumnsToContents()
            
        except Exception as e:
            self.logger.error(f"更新表格时出错: {str(e)}")
    
    def show_price_alert(self):
        """显示价格差异警告"""
        try:
            alert = PriceDifferentAlert()
            alert.exec_()
        except Exception as e:
            self.logger.error(f"显示价格差异警告时出错: {str(e)}")
    
    def show_sku_alert(self):
        """显示SKU差异警告"""
        try:
            alert = SkuDifferentAlert()
            alert.exec_()
        except Exception as e:
            self.logger.error(f"显示SKU差异警告时出错: {str(e)}")
    
    def show_local_sku_alert(self):
        """显示本地SKU差异警告"""
        try:
            alert = LocalSkuDifferentAlert()
            alert.exec_()
        except Exception as e:
            self.logger.error(f"显示本地SKU差异警告时出错: {str(e)}")
    
    def show_competitor_sku_alert(self):
        """显示竞争对手SKU差异警告"""
        try:
            alert = CompetitorSkuDifferentAlert()
            alert.exec_()
        except Exception as e:
            self.logger.error(f"显示竞争对手SKU差异警告时出错: {str(e)}")
    
    def on_task_completed(self):
        """任务完成时的处理"""
        try:
            self.is_running = False
            self.main_window.progress_bar.setValue(100)
            QMessageBox.information(self.main_window, "完成", "价格检查任务已完成！")
        except Exception as e:
            self.logger.error(f"处理任务完成事件时出错: {str(e)}")
    
    def run(self):
        """运行应用程序"""
        try:
            self.main_window.show()
            return self.app.exec_()
        except Exception as e:
            self.logger.error(f"运行应用程序时出错: {str(e)}")
            return 1

if __name__ == '__main__':
    try:
        app = PriceCheckerApp()
        sys.exit(app.run())
    except Exception as e:
        logging.error(f"程序启动失败: {str(e)}")
        sys.exit(1)
