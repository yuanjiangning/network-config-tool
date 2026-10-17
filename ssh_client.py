# -*- coding: utf-8 -*-
import time
import paramiko
from config import MOCK, SSH_PORT, TIMEOUT

def mock_output(cmd, dev):
    """模拟设备返回数据：没有真机时用它把流程跑通"""
    if 'current-configuration' in cmd:
        return (
            '#\n'
            f' sysname {dev["name"]}\n'
            'vlan batch 10 20 30\n'
            'interface Vlanif10\n'
            ' ip address 192.168.10.254 255.255.255.0\n'
            ' vrrp vrid 1 virtual-ip 192.168.10.1\n'
            'ospf 1 router-id 1.1.1.1\n#\n'
        )
    if 'vrrp brief' in cmd:
        return 'VRID  State   Virtual IP\n1     Master  192.168.10.1\n'
    if 'interface brief' in cmd:
        # 固定让 SW2 有一个 DOWN 口，演示巡检报告的异常标红
        phy = 'down' if 'SW2' in dev['name'] else 'up'
        return (
            'Interface                   PHY   PROTOCOL\n'
            'GigabitEthernet0/0/1        up    up\n'
            f'GigabitEthernet0/0/2        {phy}   {phy}\n'
        )
    return 'MOCK: ' + cmd + '\n'

class HuaweiSSH:
    """华为 VRP 设备 SSH 连接，用 with 语法自动关闭"""

    def __init__(self, dev):
        self.dev = dev
        self.client = None
        self.shell = None

    def __enter__(self):
        if MOCK:
            return self
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(
            self.dev['ip'], port=SSH_PORT,
            username=self.dev['username'],
            password=self.dev['password'],
            timeout=TIMEOUT
        )
        self.shell = self.client.invoke_shell()
        self.shell.settimeout(TIMEOUT)
        time.sleep(1)
        if self.shell.recv_ready():
            self.shell.recv(65535)
        self._send('screen-length 0 temporary')  # 关闭分屏暂停
        return self

    def _send(self, cmd, wait=1.5):
        self.shell.send(cmd + '\n')
        time.sleep(wait)
        data = b''
        while self.shell.recv_ready():
            data += self.shell.recv(65535)
            time.sleep(0.2)
        return data.decode('utf-8', errors='ignore')

    def exec_cmds(self, cmds):
        """执行多条 display 命令，返回拼接输出"""
        if MOCK:
            return '\n'.join(mock_output(c, self.dev) for c in cmds)
        out = ''
        for cmd in cmds:
            out += self._send(cmd)
        return out

    def __exit__(self, *exc):
        if self.client:
            self.client.close()
