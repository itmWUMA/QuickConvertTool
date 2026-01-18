# QuickConvertTool

一个可扩展的桌面单位换算工具，使用 Python + Tkinter 开发。

## 功能特点

- **多种单位转换**：支持长度、温度、重量、电量单位转换
- **实时转换**：输入即转换，无需点击按钮
- **参数化转换**：支持需要额外参数的转换（如电量转换需要电压）
- **易于扩展**：基于插件架构，轻松添加新的转换类型
- **简洁界面**：清晰直观的用户界面

## 支持的转换类型

### 长度 (Length)
- 米 (m)、千米 (km)、厘米 (cm)、毫米 (mm)
- 英里 (mile)、码 (yard)、英尺 (ft)、英寸 (inch)

### 温度 (Temperature)
- 摄氏度 (°C)
- 华氏度 (°F)
- 开尔文 (K)

### 重量 (Weight)
- 千克 (kg)、克 (g)、毫克 (mg)、吨 (ton)
- 磅 (lb)、盎司 (oz)

### 电量 (Battery)
- 电荷单位：毫安时 (mAh)、安时 (Ah)
- 能量单位：瓦时 (Wh)、千瓦时 (kWh)
- 支持电压参数输入，默认3.7V（锂电池常用电压）

## 安装和运行

### 环境要求
- Python 3.8 或更高版本
- Tkinter (通常随 Python 一起安装)

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
# 方式 1: 使用启动脚本（推荐）
python run.py

# 方式 2: 作为模块运行
python -m src.main
```

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行单个测试文件
pytest tests/test_length.py -v

# 运行测试并查看覆盖率
pytest tests/ --cov=src --cov-report=html
```

## 项目结构

```
QuickConvertTool/
├── run.py                         # 应用程序启动脚本（推荐）
├── src/
│   ├── __init__.py
│   ├── main.py                    # 应用程序入口
│   ├── core/
│   │   ├── __init__.py
│   │   ├── converter.py           # 转换器抽象基类
│   │   ├── parameterized_converter.py  # 参数化转换器基类
│   │   └── registry.py            # 转换器注册和管理系统
│   ├── converters/
│   │   ├── __init__.py
│   │   ├── length.py              # 长度单位转换器
│   │   ├── temperature.py         # 温度转换器
│   │   ├── weight.py              # 重量转换器
│   │   └── battery.py             # 电量转换器
│   └── ui/
│       ├── __init__.py
│       └── main_window.py         # Tkinter主窗口UI
├── tests/
│   ├── __init__.py
│   ├── test_length.py             # 长度转换器测试
│   ├── test_temperature.py        # 温度转换器测试
│   ├── test_weight.py             # 重量转换器测试
│   └── test_battery.py            # 电量转换器测试
├── requirements.txt               # 项目依赖
├── README.md                      # 项目文档
└── CLAUDE.md                      # Claude AI 指导文档
```

## 如何添加新的转换器

1. **创建转换器类**

在 `src/converters/` 目录下创建新的 Python 文件，例如 `currency.py`：

```python
from typing import List
from ..core.converter import Converter

class CurrencyConverter(Converter):
    @property
    def name(self) -> str:
        return "Currency"

    @property
    def units(self) -> List[str]:
        return ["USD", "EUR", "CNY", "JPY"]

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        # 实现转换逻辑
        pass
```

2. **注册转换器**

在 `src/converters/__init__.py` 中导出新转换器：

```python
from .currency import CurrencyConverter
__all__ = [..., "CurrencyConverter"]
```

3. **在主程序中注册**

在 `src/main.py` 中注册新转换器：

```python
from converters import ..., CurrencyConverter
registry.register(CurrencyConverter())
```

4. **编写测试**

在 `tests/` 目录下创建 `test_currency.py` 并编写单元测试。

5. **参数化转换器（可选）**

如果转换器需要额外参数（如电量转换需要电压），继承 `ParameterizedConverter` 而不是 `Converter`：

```python
from typing import List, Dict
from ..core.parameterized_converter import ParameterizedConverter

class BatteryConverter(ParameterizedConverter):
    @property
    def name(self) -> str:
        return "Battery"

    @property
    def units(self) -> List[str]:
        return ["mAh", "Ah", "Wh", "kWh"]

    @property
    def parameters(self) -> Dict:
        return {
            "voltage": {
                "label": "Voltage (V)",
                "default": "3.7",
                "required": True
            }
        }

    def _convert_with_params(self, value: float, from_unit: str, to_unit: str, **kwargs) -> float:
        voltage = kwargs.get("voltage", 3.7)
        return value * voltage
```

UI 会自动显示参数输入框，窗口高度自动调整为 380px。

## 架构设计

### 核心组件

- **Converter (抽象基类)**：定义所有转换器必须实现的接口
- **ConverterRegistry**：管理所有已注册的转换器
- **MainWindow**：提供用户界面

### 设计原则

- **开闭原则**：对扩展开放，对修改关闭
- **依赖倒置**：UI 依赖于抽象接口，而非具体实现
- **单一职责**：每个转换器只负责一种类型的转换
- **模块化**：转换器相互独立，可独立测试

## 技术栈

- **语言**: Python 3.8+
- **GUI框架**: Tkinter
- **测试框架**: pytest
- **架构模式**: 插件/注册表模式

## 开发者

此项目专为游戏程序员设计，代码结构清晰，易于理解和扩展。

## 许可证

MIT License

## 贡献

欢迎提交问题和拉取请求！

## 更新日志

### v0.2.0
- 新增电量转换器（mAh、Ah、Wh、kWh）
- 实现参数化转换器架构，支持需要额外参数的转换
- UI自动显示参数输入区域
- 窗口高度动态调整以容纳参数输入
- 完整的电量转换器单元测试（30个测试用例）

### v0.1.0 (Initial Release)
- 实现长度、温度、重量转换器
- 基于 Tkinter 的图形界面
- 完整的单元测试
- 可扩展的架构设计
