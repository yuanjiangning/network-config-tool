# -*- coding: utf-8 -*-
import os
from datetime import datetime
from config import BACKUP_DIR
from excel_io import load_devices
from ssh_client import HuaweiSSH

def backup_all(log=print):
    """备份清单中所有设备，返回报告行：(名称, IP, 状态, 文件名)"""
    devices = load_devices()
    if not devices:
        log('设备清单为空，请先在菜单选 1 生成模板')
        return []
    rows = []
    for dev in devices:
        log(f'[备份] {dev["name"]} ({dev["ip"]}) ...')
        try:
            with HuaweiSSH(dev) as cli:
                config = cli.exec_cmds(['display current-configuration'])
            fname = f'{dev["name"]}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.cfg'
            with open(os.path.join(BACKUP_DIR, fname), 'w', encoding='utf-8') as f:
                f.write(config)
            log('  成功 -> ' + fname)
            rows.append((dev['name'], dev['ip'], '成功', fname))
        except Exception as e:
            log('  失败: ' + str(e))
            rows.append((dev['name'], dev['ip'], '失败: ' + str(e), ''))
    return rows
