import sys
import os
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QTableWidget, QTableWidgetItem, QHeaderView, 
                            QProgressBar, QFileDialog)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtCore import pyqtSignal

class MainWindow(QMainWindow):
    # 定义信号
    task_started = pyqtSignal(str)
    task_completed = pyqtSignal()
    progress_updated = pyqtSignal(int)
    table_updated = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("淘宝产品价格对比工具")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #e6ffe6;")  # 浅绿色背景
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 顶部区域 - 输入区域
        top_layout = QVBoxLayout()
        
        # 文件输入区域
        file_input_layout = QHBoxLayout()
        file_label = QLabel("导入表格:")
        self.file_name_label = QLabel("")  # 初始为空
        self.open_button = QPushButton("打开")
        self.open_button.setFixedSize(80, 30)
        self.open_button.clicked.connect(self.open_file_dialog)
        
        # 添加执行按钮
        self.execute_button = QPushButton("执行")
        self.execute_button.setFixedSize(80, 30)
        self.execute_button.clicked.connect(self.start_task)
        self.execute_button.setEnabled(False)  # 初始禁用
        
        file_input_layout.addWidget(file_label)
        file_input_layout.addWidget(self.file_name_label)
        file_input_layout.addStretch()
        file_input_layout.addWidget(self.open_button)
        file_input_layout.addWidget(self.execute_button)
        
        # 任务重复间隔
        interval_layout = QHBoxLayout()
        interval_label = QLabel("任务重复间隔:")
        self.interval_input = QLineEdit()  # 初始为空
        self.interval_input.setFixedWidth(80)
        interval_unit = QLabel("分钟")
        
        interval_layout.addWidget(interval_label)
        interval_layout.addWidget(self.interval_input)
        interval_layout.addWidget(interval_unit)
        interval_layout.addStretch()
        
        # 任务时间信息
        time_info_layout = QVBoxLayout()
        
        # 初始化时间标签为空
        self.first_time_label = QLabel("任务第一次执行时间:    ")
        self.last_time_label = QLabel("任务上一次执行时间:    ")
        self.current_run_label = QLabel("本次是第0次任务执行")  # 初始为0次
        
        time_info_layout.addWidget(self.first_time_label)
        time_info_layout.addWidget(self.last_time_label)
        time_info_layout.addWidget(self.current_run_label)
        
        # 进度条
        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid grey;
                border-radius: 2px;
                text-align: center;
            }
            
            QProgressBar::chunk {
                background-color: #88c0d0;
                width: 10px;
            }
        """)
        self.progress_bar.setValue(0)  # 初始进度为0
        self.progress_label = QLabel("0%")
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        
        # 添加所有顶部布局
        top_layout.addLayout(file_input_layout)
        top_layout.addLayout(interval_layout)
        top_layout.addLayout(time_info_layout)
        top_layout.addLayout(progress_layout)
        
        # 表格区域
        self.table = QTableWidget(0, 5)  # 初始只有表头，没有数据行
        self.table.setHorizontalHeaderLabels(["序号", "本店价格", "本店SKU", "竞店价格", "竞店SKU"])
        
        # 设置表格样式
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d3d3d3;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 4px;
                border: 1px solid #d3d3d3;
                font-weight: bold;
            }
        """)
        
        # 将所有组件添加到主布局
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.table)
        
        # 初始化任务相关变量
        self.run_count = 0
        self.first_run_time = None
        self.last_run_time = None
        self.is_running = False
        self.selected_file = None
        
    def open_file_dialog(self):
        """打开文件对话框选择Excel文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择Excel文件", "", "Excel文件 (*.xlsx *.xls)"
        )
        if file_path:
            self.selected_file = file_path
            file_name = os.path.basename(file_path)
            self.file_name_label.setText(file_name)
            self.execute_button.setEnabled(True)  # 启用执行按钮
    
    def start_task(self):
        """开始执行任务"""
        if not self.selected_file:
            return
        
        if self.is_running:
            return
            
        try:
            self.is_running = True
            self.run_count += 1
            
            # 更新运行次数显示
            self.current_run_label.setText(f"本次是第{self.run_count}次任务执行")
            
            # 更新时间显示
            current_time = datetime.now()
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M")
            
            if self.run_count == 1:
                self.first_run_time = current_time
                self.first_time_label.setText(f"任务第一次执行时间:    {current_time_str}")
            
            self.last_run_time = current_time
            self.last_time_label.setText(f"任务上一次执行时间:    {current_time_str}")
            
            # 重置进度条
            self.progress_bar.setValue(0)
            self.progress_label.setText("0%")
            
            # 清空表格
            self.table.setRowCount(0)
            
            # 发出任务开始信号，并传递文件路径
            self.task_started.emit(self.selected_file)
            
            # 设置下一次任务的定时器
            try:
                interval_minutes = int(self.interval_input.text())
                if interval_minutes > 0:
                    QTimer.singleShot(interval_minutes * 60 * 1000, self.start_task)
            except ValueError:
                pass
                
        except Exception as e:
            self.is_running = False
            print(f"启动任务时出错: {str(e)}")
    
    def update_progress(self, value):
        """更新进度条和进度标签"""
        try:
            self.progress_bar.setValue(value)
            self.progress_label.setText(f"{value}%")
        except Exception as e:
            print(f"更新进度时出错: {str(e)}")
    
    def update_table(self, data):
        """更新表格数据"""
        try:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row, col, item)
                
        except Exception as e:
            print(f"更新表格时出错: {str(e)}")
            
    def task_completed(self):
        """任务完成时的处理"""
        self.is_running = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
