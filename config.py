# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEVICE_FILE = os.path.join(BASE_DIR, 'devices.xlsx')   # 设备清单
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')         # 配置备份目录
REPORT_DIR = os.path.join(BASE_DIR, 'reports')         # 巡检报告目录
SSH_PORT = 22
TIMEOUT = 10

# 重要：True=模拟模式（不连真机，自动生成演示数据，先把项目跑通）
#       连真机验证成功后，改成 False
MOCK = True

for d in (BACKUP_DIR, REPORT_DIR):
    os.makedirs(d, exist_ok=True)
