# -*- coding: utf-8 -*-
# 注意：本文件不能命名为 inspect.py，会与 Python 标准库 inspect 冲突导致报错
import re
from excel_io import load_devices
from ssh_client import HuaweiSSH

# 匹配华为接口名开头的行
IF_PATTERN = re.compile(r'^(GigabitEthernet|Ethernet|Eth-Trunk|Serial|Vlanif)', re.I)

def parse_vrrp(text):
    if re.search(r'master', text, re.I):
        return '正常', '检测到 VRRP Master 网关'
    return '异常', '未检测到 VRRP Master 状态'

def parse_interface(text):
    downs = []
    for line in text.splitlines():
        s = line.strip()
        if IF_PATTERN.match(s) and re.search(r'\bdown\b', s, re.I):
            downs.append(s)
    if downs:
        return '异常', '; '.join(downs)[:300]
    return '正常', '所有接口状态 UP'

def inspect_all(log=print):
    """巡检所有设备，返回报告行：(名称, IP, 巡检项, 状态, 明细)"""
    devices = load_devices()
    if not devices:
        log('设备清单为空，请先在菜单选 1 生成模板')
        return []
    rows = []
    for dev in devices:
        log(f'[巡检] {dev["name"]} ({dev["ip"]}) ...')
        try:
            with HuaweiSSH(dev) as cli:
                text = cli.exec_cmds(['display vrrp brief', 'display interface brief'])
            checks = (
                ('VRRP 状态', *parse_vrrp(text)),
                ('接口状态', *parse_interface(text)),
            )
            for item, status, detail in checks:
                rows.append((dev['name'], dev['ip'], item, status, detail))
                mark = 'OK ' if status == '正常' else '!! '
                log(f'  {mark}{item}: {status}')
        except Exception as e:
            rows.append((dev['name'], dev['ip'], '连接', '异常', str(e)))
            log('  失败: ' + str(e))
    return rows
