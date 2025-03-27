import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, 
                            QLabel, QPushButton, QHBoxLayout)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

class AlertDialog(QDialog):
    """
    警告对话框基类，可以根据不同类型的错误显示不同的对话框
    """
    def __init__(self, message="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("警告")
        self.setFixedSize(400, 150)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        # 主布局
        main_layout = QHBoxLayout(self)
        
        # 图标标签
        self.icon_label = QLabel()
        self.icon_pixmap = QPixmap()  # 将在子类中设置
        self.icon_label.setFixedSize(32, 32)
        
        # 消息标签
        self.message_label = QLabel(message)
        self.message_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.message_label.setAlignment(Qt.AlignCenter)
        
        # 确认按钮
        self.ok_button = QPushButton("确定")
        self.ok_button.setFixedSize(80, 30)
        self.ok_button.clicked.connect(self.accept)
        
        # 设置布局
        content_layout = QVBoxLayout()
        content_layout.addWidget(self.message_label)
        content_layout.addWidget(self.ok_button, 0, Qt.AlignCenter)
        
        main_layout.addWidget(self.icon_label)
        main_layout.addLayout(content_layout)
        
    def set_style(self, bg_color, text_color):
        """设置对话框样式"""
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_color};
                border: 1px solid #666666;
                border-radius: 5px;
            }}
            QLabel {{
                color: {text_color};
                background-color: transparent;
            }}
            QPushButton {{
                background-color: white;
                border: 1px solid #666666;
                border-radius: 3px;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #e0e0e0;
            }}
        """)


class PriceDifferentAlert(AlertDialog):
    """价格不同警告对话框"""
    def __init__(self, parent=None):
        super().__init__("本店和竞店价格不同", parent)
        
        # 设置红色背景和白色文本
        self.set_style("#ff0000", "white")
        
        # 设置警告图标
        warning_icon = QPixmap("ui/resources/价格报错图.png")
        if warning_icon.isNull():
            # 如果找不到图标，创建一个替代图标
            warning_icon = self.create_warning_icon()
        
        self.icon_label.setPixmap(warning_icon.scaled(32, 32, Qt.KeepAspectRatio))

    def create_warning_icon(self):
        """创建默认警告图标"""
        from PyQt5.QtGui import QPainter, QColor, QPen
        from PyQt5.QtCore import QRect
        
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor("yellow"), 2))
        painter.setBrush(QColor("yellow"))
        painter.drawPolygon([
            pixmap.rect().topLeft() + QPoint(16, 0),
            pixmap.rect().bottomLeft() + QPoint(0, 0),
            pixmap.rect().bottomRight() + QPoint(0, 0)
        ])
        
        painter.setPen(QPen(QColor("black"), 2))
        painter.drawText(QRect(12, 8, 8, 16), Qt.AlignCenter, "!")
        painter.end()
        
        return pixmap


class SkuDifferentAlert(AlertDialog):
    """SKU不同警告对话框"""
    def __init__(self, parent=None):
        super().__init__("本店和竞店SKU不同", parent)
        
        # 设置黄色背景和黑色文本
        self.set_style("#ffff00", "black")
        
        # 设置警告图标
        warning_icon = QPixmap("ui/resources/SKU报错图.png")
        if warning_icon.isNull():
            # 如果找不到图标，创建一个替代图标
            warning_icon = self.create_warning_icon()
        
        self.icon_label.setPixmap(warning_icon.scaled(32, 32, Qt.KeepAspectRatio))

    def create_warning_icon(self):
        """创建默认警告图标"""
        from PyQt5.QtGui import QPainter, QColor, QPen
        from PyQt5.QtCore import QRect
        
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor("yellow"), 2))
        painter.setBrush(QColor("yellow"))
        painter.drawPolygon([
            pixmap.rect().topLeft() + QPoint(16, 0),
            pixmap.rect().bottomLeft() + QPoint(0, 0),
            pixmap.rect().bottomRight() + QPoint(0, 0)
        ])
        
        painter.setPen(QPen(QColor("black"), 2))
        painter.drawText(QRect(12, 8, 8, 16), Qt.AlignCenter, "!")
        painter.end()
        
        return pixmap


class LocalSkuDifferentAlert(AlertDialog):
    """本店SKU与链接中不同警告对话框"""
    def __init__(self, parent=None):
        super().__init__("本店SKU和链接中本店的SKU不同", parent)
        
        # 设置蓝色背景和白色文本
        self.set_style("#0080ff", "white")
        
        # 设置警告图标
        warning_icon = QPixmap("ui/resources/本店SKU报错.png")
        if warning_icon.isNull():
            # 如果找不到图标，创建一个替代图标
            warning_icon = self.create_warning_icon()
        
        self.icon_label.setPixmap(warning_icon.scaled(32, 32, Qt.KeepAspectRatio))

    def create_warning_icon(self):
        """创建默认警告图标"""
        from PyQt5.QtGui import QPainter, QColor, QPen
        from PyQt5.QtCore import QRect
        
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor("blue"), 2))
        painter.setBrush(QColor("blue"))
        painter.drawPolygon([
            pixmap.rect().topLeft() + QPoint(16, 0),
            pixmap.rect().bottomLeft() + QPoint(0, 0),
            pixmap.rect().bottomRight() + QPoint(0, 0)
        ])
        
        painter.setPen(QPen(QColor("white"), 2))
        painter.drawText(QRect(12, 8, 8, 16), Qt.AlignCenter, "!")
        painter.end()
        
        return pixmap


class CompetitorSkuDifferentAlert(AlertDialog):
    """竞店SKU与链接中不同警告对话框"""
    def __init__(self, parent=None):
        super().__init__("竞店SKU和链接中竞店的SKU不同", parent)
        
        # 设置橙色背景和黑色文本
        self.set_style("#ffa500", "black")
        
        # 设置警告图标
        warning_icon = QPixmap("ui/resources/竞店SKU报错.png")
        if warning_icon.isNull():
            # 如果找不到图标，创建一个替代图标
            warning_icon = self.create_warning_icon()
        
        self.icon_label.setPixmap(warning_icon.scaled(32, 32, Qt.KeepAspectRatio))

    def create_warning_icon(self):
        """创建默认警告图标"""
        from PyQt5.QtGui import QPainter, QColor, QPen
        from PyQt5.QtCore import QRect
        
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor("orange"), 2))
        painter.setBrush(QColor("orange"))
        painter.drawPolygon([
            pixmap.rect().topLeft() + QPoint(16, 0),
            pixmap.rect().bottomLeft() + QPoint(0, 0),
            pixmap.rect().bottomRight() + QPoint(0, 0)
        ])
        
        painter.setPen(QPen(QColor("black"), 2))
        painter.drawText(QRect(12, 8, 8, 16), Qt.AlignCenter, "!")
        painter.end()
        
        return pixmap


# 测试代码
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 测试各种对话框
    price_alert = PriceDifferentAlert()
    price_alert.exec_()
    
    sku_alert = SkuDifferentAlert()
    sku_alert.exec_()
    
    local_sku_alert = LocalSkuDifferentAlert()
    local_sku_alert.exec_()
    
    competitor_sku_alert = CompetitorSkuDifferentAlert()
    competitor_sku_alert.exec_()
