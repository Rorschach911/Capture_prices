# 淘宝商品价格对比工具

一个用于自动比较淘宝商品价格和SKU的桌面应用程序。

## 功能特点

- 自动读取Excel表格中的商品链接
- 实时抓取淘宝商品价格和SKU信息
- 自动比较本店和竞店商品价格差异
- 自动比较本店和竞店SKU差异
- 支持定时任务，可设置重复执行间隔
- 直观的图形用户界面
- 实时进度显示
- 差异警告弹窗提示
- 完整的日志记录

## 安装说明

### 系统要求

- Python 3.7+
- Windows 10/11
- Chrome浏览器

### 依赖安装

1. 克隆项目到本地：
```bash
git clone https://github.com/yourusername/taobao-price-checker.git
cd taobao-price-checker
```

2. 安装依赖包：
```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python main.py
```

## 使用说明

1. 准备Excel文件
   - 创建名为"对比表.xlsx"的Excel文件
   - 文件需包含以下列：
     - 链接A（本店商品链接）
     - A店SKU（本店商品SKU）
     - 链接B（竞店商品链接）
     - B店SKU（竞店商品SKU）

2. 启动程序
   - 点击"打开"按钮选择Excel文件
   - 设置任务重复间隔（分钟）
   - 程序会自动开始执行比较任务

3. 查看结果
   - 表格中显示实时比较结果
   - 如有差异会弹出相应警告窗口：
     - 红色窗口：价格不同
     - 黄色窗口：SKU不同
     - 蓝色窗口：本店SKU与链接中不同
     - 橙色窗口：竞店SKU与链接中不同

## 开发文档

### 项目结构

```
price_compare_app/
│
├── main.py                 # 主程序入口
├── config.py               # 配置文件
├── requirements.txt        # 依赖包列表
│
├── utils/                  # 工具模块
│   ├── __init__.py
│   ├── excel_handler.py    # Excel处理
│   └── browser_handler.py  # 浏览器操作
│
├── core/                   # 核心功能模块
│   ├── __init__.py
│   ├── price_fetcher.py    # 价格获取
│   ├── sku_fetcher.py      # SKU获取
│   └── data_comparator.py  # 数据比较
│
├── ui/                     # 用户界面模块
│   ├── __init__.py
│   ├── main_window.py      # 主窗口
│   ├── alert_dialog.py     # 警告弹窗
│   └── resources/          # 资源文件
│
├── logs/                   # 日志文件夹
└── data/                   # 数据文件夹
```

### 核心模块说明

#### 1. 价格获取模块 (core.price_fetcher)

主要类：`PriceFetcher`

```python
class PriceFetcher:
    def get_price(self, url: str) -> float:
        """获取商品价格"""
        pass
```

#### 2. SKU获取模块 (core.sku_fetcher)

主要类：`SkuFetcher`

```python
class SkuFetcher:
    def get_sku(self, url: str) -> str:
        """获取商品SKU"""
        pass
    
    def get_sku_with_retry(self, url: str) -> str:
        """带重试机制的SKU获取"""
        pass
```

#### 3. 数据比较模块 (core.data_comparator)

主要类：`DataComparator`

```python
class DataComparator:
    def compare_prices(self, price1: float, price2: float) -> bool:
        """比较价格"""
        pass
    
    def compare_skus(self, sku1: str, sku2: str) -> bool:
        """比较SKU"""
        pass
```

### 工具模块说明

#### 1. Excel处理模块 (utils.excel_handler)

主要类：`ExcelHandler`

```python
class ExcelHandler:
    def read_excel(self, file_path: str) -> list:
        """读取Excel文件"""
        pass
    
    def save_results(self, file_path: str, results: list) -> None:
        """保存结果"""
        pass
```

#### 2. 浏览器处理模块 (utils.browser_handler)

主要类：`BrowserHandler`

```python
class BrowserHandler:
    def get_page(self, url: str) -> bool:
        """打开页面"""
        pass
    
    def find_element_by_xpath(self, xpath: str) -> WebElement:
        """通过XPath查找元素"""
        pass
```

### UI模块说明

#### 1. 主窗口 (ui.main_window)

主要类：`MainWindow`
- 继承自`QMainWindow`
- 实现主界面布局和交互逻辑

#### 2. 警告对话框 (ui.alert_dialog)

主要类：
- `PriceDifferentAlert`
- `SkuDifferentAlert`
- `LocalSkuDifferentAlert`
- `CompetitorSkuDifferentAlert`

## 接口文档

### 1. Excel文件格式

要求的Excel文件格式：

| 列名 | 说明 | 类型 | 必填 |
|------|------|------|------|
| 链接A | 本店商品链接 | string | 是 |
| A店SKU | 本店商品SKU | string | 是 |
| 链接B | 竞店商品链接 | string | 是 |
| B店SKU | 竞店商品SKU | string | 是 |

### 2. 配置文件参数

config.py中的配置项：

```python
CONFIG = {
    "browser": {
        "headless": False,      # 是否启用无头模式
        "timeout": 30,          # 超时时间(秒)
        "user_agent": "...",    # 用户代理
        "window_size": {
            "width": 1366,
            "height": 768
        }
    },
    "price": {
        "panel_class": "...",   # 价格面板class
        "xpath_template": "..." # 价格XPath模板
    },
    "sku": {
        "class_name": "..."    # SKU元素class
    },
    "task": {
        "default_interval": 60, # 默认任务间隔(分钟)
        "retry_times": 3,       # 重试次数
        "retry_delay": 5        # 重试间隔(秒)
    }
}
```

### 3. 日志格式

日志文件位置：`logs/app.log`

日志格式：
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

## 常见问题

1. **Q: 为什么无法打开淘宝页面？**
   A: 请确保：
   - Chrome浏览器已安装
   - 网络连接正常
   - 淘宝链接有效且可访问

2. **Q: 为什么获取不到价格？**
   A: 可能原因：
   - 页面结构发生变化
   - 网页加载不完整
   - XPath配置不正确

3. **Q: 为什么程序运行很慢？**
   A: 建议：
   - 减少同时比较的商品数量
   - 增加任务执行间隔
   - 检查网络连接速度

## 更新日志

### v1.0.0 (2024-03-05)
- 初始版本发布
- 实现基本的价格和SKU比较功能
- 支持定时任务
- 添加图形用户界面

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 联系方式

- 项目维护者：[Rorschach]
- 邮箱：[your.email@example.com]
- GitHub：[your-github-profile]
