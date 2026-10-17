# 网络设备配置批量备份与巡检工具

基于 Python + Paramiko 开发的企业网络运维自动化工具：用 Excel 维护设备清单，一键批量 SSH 登录华为交换机/路由器，自动完成配置备份与 VRRP / 接口状态巡检，并生成带异常标红的 Excel 报告。内置模拟模式（MOCK），无需真机即可完整演示全流程；将 `config.py` 中 `MOCK` 改为 `False` 即可连接真实设备。

## 技术栈

Python 3、Paramiko、openpyxl、SSH（华为 VRP）

## 功能

- 读取 Excel 设备清单，批量执行 `display current-configuration` 备份配置，按「设备名 + 时间戳」归档到 backups 目录
- 自动采集 VRRP / 接口状态，用正则解析异常 DOWN 接口
- 生成 Excel 备份报告与巡检报告，**异常项整行自动标红**
- 命令行数字菜单操作，支持一键「备份 + 巡检」
- 使用上下文管理器（with）封装 SSH 连接，确保连接自动释放；MOCK 模式便于无设备环境开发与测试

## 项目结构

```
network-config-tool/
├── main.py          # 程序入口（数字菜单）
├── config.py        # 配置项（MOCK 开关、路径、超时）
├── excel_io.py      # 读写 Excel 设备清单
├── ssh_client.py    # Paramiko 封装华为 VRP 的 SSH 连接
├── backup.py        # 批量配置备份
├── health_check.py  # VRRP / 接口状态巡检与解析
├── report.py        # 生成 Excel 报告（异常标红）
├── devices.xlsx     # 设备清单（程序自动生成模板）
├── backups/         # 备份的配置文件
└── reports/         # 巡检报告
```

## 快速开始

```bash
git clone <仓库地址>
cd network-config-tool
python -m venv .venv
# Windows 激活虚拟环境
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

运行后按菜单：先输入 `1` 生成设备清单模板，再输入 `4` 一键执行备份与巡检，报告生成在 reports 目录。

## 连接真机

在华为设备（eNSP 或真机）开启 SSH（stelnet server enable、AAA 用户授权 ssh、VTY 配置 protocol inbound ssh），将真实 IP / 账号填入 devices.xlsx，把 config.py 中 `MOCK` 改为 `False` 后重新运行即可。
