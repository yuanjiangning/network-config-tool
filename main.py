# -*- coding: utf-8 -*-
from excel_io import create_template
from backup import backup_all
from health_check import inspect_all
from report import save_report

MENU = '''
======== 网络设备配置批量备份与巡检工具 ========
1. 生成设备清单模板（devices.xlsx）
2. 批量备份设备配置
3. 执行状态巡检并生成报告
4. 一键执行：备份 + 巡检
0. 退出
请输入序号：'''

def main():
    while True:
        cmd = input(MENU).strip()
        if cmd == '1':
            create_template()
        elif cmd == '2':
            rows = backup_all()
            if rows:
                print('报告已生成：', save_report('配置备份报告',
                      ['设备名称', '管理IP', '状态', '备份文件'], rows))
        elif cmd == '3':
            rows = inspect_all()
            if rows:
                print('报告已生成：', save_report('巡检报告',
                      ['设备名称', '管理IP', '巡检项', '状态', '明细'], rows))
        elif cmd == '4':
            rows = backup_all()
            if rows:
                print('报告已生成：', save_report('配置备份报告',
                      ['设备名称', '管理IP', '状态', '备份文件'], rows))
            rows = inspect_all()
            if rows:
                print('报告已生成：', save_report('巡检报告',
                      ['设备名称', '管理IP', '巡检项', '状态', '明细'], rows))
        elif cmd == '0':
            print('再见')
            break
        else:
            print('输入有误，请重新选择')

if __name__ == '__main__':
    main()
