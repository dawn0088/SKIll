# Embedded Debug Agent Matrix Skill

面向 STM32、ESP32、传感器、运动控制、PID 调参、Datasheet 长文本检索、硬件原理图解析、C/C++ 底层驱动生成、自动化编译修复与闭环故障诊断的 Codex Skill 库。

本仓库用于沉淀一个已经落地使用的“嵌入式软硬件联调与自动化闭环调试 Agent 矩阵系统”。它既可以作为 Codex Skill 被复用，也可以作为申请更高 Token 额度时的项目材料，说明该系统为什么需要稳定的大上下文、多 Agent 协作与高频推理调用。

## 项目背景

传统嵌入式开发中，工程师需要频繁在硬件原理图、芯片 Datasheet、引脚配置工具、寄存器手册、C 语言代码、编译日志、串口日志、示波器波形之间切换。由于信息源分散，常见问题包括：

- 引脚复用冲突、启动引脚误用、SWD/JTAG 调试引脚占用。
- 总线时序、传感器转换延迟、PWM/编码器采样周期不匹配。
- PID 参数震荡、积分饱和、采样周期抖动、计数器溢出。
- I2C/SPI/UART 偶发死锁、DMA/中断优先级冲突、看门狗复位。
- 编译报错与硬件配置之间缺乏自动化反思闭环。

本项目通过长上下文推理、状态机建模和多 Agent 协作，把“硬件约束 -> 架构推理 -> 代码生成 -> 自动编译 -> 日志分析 -> 反思修复”串成一个可迭代闭环。

## Agent 矩阵

### 1. 硬件规格感知 Agent

负责解析原理图、引脚连接图、Datasheet、时序表、CubeMX/ESP-IDF 配置等资料，并抽取结构化硬件约束：

```text
signal | mcu_pin | peripheral | direction | voltage | timing | source | risk
```

它重点识别引脚复用、启动引脚、电平兼容、外设时钟、总线时序、传感器转换时间、PWM/编码器资源占用等风险。

### 2. 架构推理与代码生成 Agent

负责基于硬件约束生成固件架构、状态机、控制周期、寄存器/外设配置和 C/C++ 代码。典型推理链包括：

```text
电机减速比 -> 编码器脉冲数 -> 计数器溢出时间 -> 采样周期 -> 离散 PID 方程 -> PWM 输出限幅
```

该 Agent 优先遵循项目已有 HAL、LL、ESP-IDF、FreeRTOS 或裸机代码风格，避免引入与项目不一致的抽象。

### 3. 自动化编译与虚拟执行 Agent

负责调用本地交叉编译工具链，捕获 Error/Warning/Linker diagnostics，并将诊断信息反向喂给生成 Agent：

- 定位第一处真实错误。
- 识别 HAL/LL/ESP-IDF API 签名不匹配。
- 修复 include、宏、类型、链接符号、弱函数覆盖等问题。
- 迭代直到编译通过或明确阻塞原因。

### 4. 闭环调试与故障诊断 Agent

负责分析串口日志、SWD/JTAG Dump、异常堆栈、PID 曲线、总线抓包和运行时状态机日志，判断故障属于：

- 电气问题：电源跌落、电平不匹配、上拉缺失、地弹、噪声。
- 时序问题：ISR 抖动、计数器溢出、总线 setup/hold 违规。
- 软件问题：竞态、缓冲区溢出、寄存器掩码错误、错误处理缺失。
- 配置问题：复用功能错误、DMA 通道冲突、中断优先级不当。

然后给出代码修正、配置修正或下一步测量建议。

## 仓库结构

```text
embedded-debug-agent-matrix/
  SKILL.md
  agents/
    openai.yaml
  references/
    hardware-ingestion.md
    state-machine-patterns.md
    compile-reflection.md
    closed-loop-debug.md
  scripts/
    pin_conflict_checker.py
docs/
  token-quota-application.md
```

## Skill 能力范围

- STM32/ESP32 工程 Bring-up。
- 原理图、Datasheet、寄存器表、引脚表解析。
- CubeMX、ESP-IDF、HAL、LL、FreeRTOS、裸机 C 工程辅助开发。
- 传感器、编码器、电机驱动、PID 控制、PWM、ADC、UART、SPI、I2C 调试。
- 编译日志反思修复与代码生成迭代。
- 串口日志、SWD Dump、异常堆栈、控制曲线的闭环诊断。

## 引脚冲突检查工具

仓库内置一个轻量脚本，可对归一化后的 pin map CSV 做基础风险检查：

```bash
python embedded-debug-agent-matrix/scripts/pin_conflict_checker.py pinmap.csv
```

CSV 字段格式：

```text
signal,mcu_pin,peripheral,direction,voltage,timing,source
```

脚本会检查：

- MCU 引脚重复占用。
- BOOT、NRST、SWD、JTAG、OSC、ESP32 strapping pin 等特殊引脚风险。
- 5V 电平兼容风险。
- I2C 开漏/上拉检查提示。
- 缺失资料来源的硬件约束。

## Token 额度申请说明

该系统不是简单的短问答场景，而是高频、长上下文、多轮闭环的工程推理任务。一次完整调试可能同时包含：

- 多页硬件原理图与 PCB 引脚映射。
- 上百页 Datasheet、寄存器表和时序表。
- 生成代码、手写驱动、HAL/LL/ESP-IDF 配置。
- 编译错误、链接错误、Warning、AST 级修复上下文。
- 串口日志、SWD Dump、PID 曲线、总线抓包与历史迭代记录。

目前目标落地场景为 15 人核心嵌入式团队，每日稳定 Token 消耗约 380 万至 450 万，并已将软硬件联调周期缩短约 65%。更高 Token 额度可以保证长链路调试状态不被截断，支持多 Agent 并行分析与更稳定的自动化修复闭环。

更完整的申请材料见：

[docs/token-quota-application.md](docs/token-quota-application.md)

## 适用场景示例

- “帮我根据 STM32 原理图和 Datasheet 检查 I2C/SPI/UART 引脚复用是否冲突。”
- “根据电机减速比、编码器线数和目标控制频率生成 PID 控制状态机。”
- “编译失败了，帮我根据 GCC 报错修复 HAL 驱动代码。”
- “串口日志显示 I2C 偶发卡死，帮我分析可能的硬件和软件原因。”
- “ESP32 上电偶发无法启动，帮我检查 strapping pin 和外围电路风险。”
