#!/bin/python
# -*- coding: utf-8 -*-

import os, os.path
import time
import traceback
import jxpj
import sys
import subprocess

reload(sys)
sys.setdefaultencoding('utf-8')


def create_lnk(lnkpath, targetpath):
    """ 创建或设置快捷方式
    """
    print u'\n\n\t正在设置开机自启动，请选择允许运行！\n\n'
    # time.sleep(3)
    vbspath = os.path.join(sys.path[0], 'shortcut.vbs')
    command = 'cmd /c ""%s" "%s" "%s""' % (vbspath, lnkpath, targetpath)
    code = subprocess.call(command)
    # 由于vbs不论是否正常退出，都返回0，所以手动返回1表示成功
    return code == 1
    

def check_start_at_login():
    if sys.platform != 'win32':
        print u'目前仅支持windows开机自启动！'
        return

    lnkpath = os.environ['USERPROFILE']
    lnkpath = os.path.join(lnkpath, r'AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup')
    lnkpath = os.path.join(lnkpath, 'startup.py.lnk')
    lnkpath = os.path.abspath(lnkpath)
    targetpath = os.path.join(sys.path[0], 'startup.py')
    targetpath = os.path.abspath(targetpath)

    while not create_lnk(lnkpath, targetpath):
        pass


# -------------- main --------------
if __name__ == '__main__':
    endTime = time.time() + 10

    try:
        jxpj.check_username_password()
    except:
        traceback.print_exc()
        print u'程序出问题，请联系QQ：735486078'
        os.system('pause')
        exit(0)

    check_start_at_login()

    now = time.time()
    old = 0
    status = None
    while now <= endTime:
        now = time.time()
        if now - old > 1:
            old = now
            t = int(endTime - now)
            status = u'\t为了避免刚启动时网络还未正常连接，请等待%d秒' % (t)
            # win10上一个中文字符需要多个退格键清楚
            status += chr(8) * (len(status) *3)
            print status,
            sys.stdout.flush()

    # 清理status
    if status is not None:
        l = len(status) + 1
        status = ' ' * l + chr(8) * l
        print status,
    print u'\t正在评分，请稍后。。。'

    try:
        jxpj.dojxpj()
    except:
        traceback.print_exc()
        print u'程序出问题，请联系QQ：735486078'
        os.system('pause')

