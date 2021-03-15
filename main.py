# coding=utf-8
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QInputDialog, QLineEdit
from PyQt5.QtGui import QTextCursor
import subprocess
import test
from PyQt5 import QtCore
import json
import os
import time
import pyperclip
from _ctypes import *

VirtualKey = [
'CTRL+G键-----将窗口大小调整为1:1（完美像素）',

'CTRL+H键-----点击主页菜单',

'CTRL+B键-----CTRL+backspace键-----右键单击-----点击返回键',

'CTRL+M键-----点击菜单',

'CTRL+向上-----点击音量增大',

'CTRL+向下-----点击音量',

'CTRL+P键-----点击电源（打开/关闭屏幕）',

'右键单击-----（屏幕关闭时）开机',

'CTRL+O键-----关闭设备屏幕（保持镜像）',

'CTRL+N键-----展开通知面板',

'ctrl+shift+n-----折叠通知面板',

'从计算机安装apk-----将拖放apk文件拖放至窗口即可'
]
global screen_state
screen_state=0
#进程
global process
process=None
#下拉框的下标
global list_index
list_index=0
#模拟点击初始值
global tap_times
tap_times=0
global lp_state
lp_state=0
def button_False():
    ui.pushButton_7.setEnabled(False)
    ui.pushButton_8.setEnabled(False)
    ui.pushButton_9.setEnabled(False)
    ui.pushButton_11.setEnabled(False)
    ui.pushButton_6.setEnabled(False)
    ui.pushButton_13.setEnabled(False)
    ui.pushButton_14.setEnabled(False)
    ui.pushButton_10.setEnabled(False)
def button_True():
    ui.pushButton_7.setEnabled(True)
    ui.pushButton_8.setEnabled(True)
    ui.pushButton_9.setEnabled(True)
    ui.pushButton_11.setEnabled(True)
    ui.pushButton_6.setEnabled(True)
    ui.pushButton_14.setEnabled(True)
    ui.pushButton_13.setEnabled(True)
    ui.pushButton_10.setEnabled(True)

class Thread_1(QThread):
    _signal = pyqtSignal()
    def __init__(self):
        super().__init__()

    def run(self):
        tap_phone(tap_times)
        self._signal.emit()

def tap_start():
    button_False()
    ui.thread_1 = Thread_1()  # 创建线程
    ui.thread_1._signal.connect(set_btn1)      # 脚本运行过程中，启动按钮状态变为不可点击状态
    ui.thread_1.start()  # 开始线程

def set_btn1():
    button_True()

class Thread_2(QThread):
    _signal = pyqtSignal()
    def __init__(self):
        super().__init__()

    def run(self):
        while screen_state>0:
            time.sleep(1)
        self._signal.emit()

def lp_th():
    button_False()
    ui.thread_2 = Thread_2()  # 创建线程
    ui.thread_2._signal.connect(set_btn2)  # 脚本运行过程中，启动按钮状态变为不可点击状态
    ui.thread_2.start()  # 开始线程

def set_btn2():
    button_True()

def tap_phone(times):
    updata_number()
    dev = Phone_ID()
    list_index = ui.comboBox_2.currentIndex()
    if len(dev)>0:
        color_handle('-' * 60)
        color_handle('模拟点击执行中...')
        for i in range(times):
            if len(Phone_ID())>0:
                subprocess.Popen(f"adb -s {dev[list_index]} shell input tap 650 550", shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            else:
                return
        color_handle('模拟点击执行完毕')
        global tap_times
        tap_times=0
    else:
        color_handle('-' * 60)
        color_handle('设备未连接')

def  tap_number():
    global tap_times
    global lp_state
    if lp_state==0:
        tap_times = QInputDialog.getInt(ui.pushButton_10, "模拟点击", "请输入点击次数:")[0]
    else:
        color_handle('-' * 60)
        color_handle('等待录屏完成')
        return
    if tap_times>0:
        tap_start()
    else:
        color_handle('-' * 60)
        color_handle('请输入正确参数！')


def Phone_ID():
    cc=subprocess.Popen("adb devices",shell=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
    aa = cc.stdout.read().decode('GBK')
    devices=aa.splitlines()
    androidevices_list=[]
    for device in devices:
        if 'device' in device and 'devices' not in device:
            device = device.split('\t')[0]
            androidevices_list.append(device)

    return androidevices_list


def devices_name():
    with open('devices_name.json','r',encoding='utf-8') as fp:
        dev_name=json.load(fp)
        dev=Phone_ID()
        a = []
        for dd in dev:
            for dev in dev_name:
                if dd == dev_name[dev]:
                    a.append(dev)
        return a

def phone_ch_name():
    devices=devices_name()
    return devices[list_index]
def phone_all_name():
    devices=comboBoxAdd()
    return devices[list_index]

def devices_name1():
    with open('devices_name.json','r',encoding='utf-8') as fp:
        dev_name=json.load(fp)
        return dev_name

# def comboBoxAdd():
#     device_list = []
#     global list_index
#     devices=devices_name()
#     list_index = 0
#     if not devices:
#         # device_id = ''
#         # device_list = []
#         ui.comboBox_2.clear()
#         return
#     if ui.comboBox_2.currentText() and ui.comboBox_2.currentText() in devices:
#         try:
#             list_index = devices.index(ui.comboBox_2.currentText())
#         except Exception as E:
#             ui.textBrowser.append("命令执行失败，当前没有连接设备，请点击'获取设备'按钮，尝试获取设备。")
#     if device_list != devices:
#         ui.comboBox_2.clear()
#         ui.comboBox_2.addItems(devices)
#         ui.comboBox_2.setCurrentIndex(list_index)
#         device_list = devices

def comboBoxAdd():
    device_list = []
    global list_index
    list_index = 0
    dev = Phone_ID()
    # adr_ch_name是配置文件中的所有键值对
    adr_ch_name = devices_name1()
    # all_device[]是下拉列表的所有设备
    all_device = []
    # b是配置文件中的值
    json_device = []
    ui.label_2.setText(f"当前连接：{len(Phone_ID())}")
    for key_chName in adr_ch_name:
        # 获取配置文件所有的值 添加到数组b中
        json_device.append(adr_ch_name[key_chName])
    for devID in dev:
        # 判断adb获取的所有设备是否有没有在配置文件中，如果没有则添加到数组a中
        if devID not in json_device:
            all_device.append(devID)
        # 判断adb获取的设备如果在配置文件中，在的话就获取该值的键，添加在数组a中
        elif devID in json_device:
            for adr in adr_ch_name:
                if devID == adr_ch_name[adr]:
                    all_device.append(adr)
    if not all_device:
        ui.comboBox_2.clear()
        return
    if ui.comboBox_2.currentText() in all_device:
        try:
            list_index = all_device.index(ui.comboBox_2.currentText())
        except Exception as E:
            ui.textBrowser.append("命令执行失败，当前没有连接设备，请点击'获取设备'按钮，尝试获取设备。")
    if device_list != all_device:
        ui.comboBox_2.clear()
        ui.comboBox_2.addItems(all_device)
        ui.comboBox_2.setCurrentIndex(list_index)
        device_list = all_device
        return all_device


def clean():
    ui.textBrowser.clear()


def config_color():
    stus = {'背景颜色': '#MainWindow{background-color: white}'}
    res2 = json.dumps(stus, ensure_ascii=False)
    with open("config.json", "w", encoding="utf-8")as f:
        f.write(res2)
    # for i in ll:
    #     if i =="背景颜色":
    #         MainWindow.setStyleSheet(ll[i])
    MainWindow.setStyleSheet('#MainWindow{background-color: white}')

def config_color1():
    stus = {'背景颜色': '#MainWindow{background-color: #e8e8e8}'}
    res2 = json.dumps(stus, ensure_ascii=False)
    with open("config.json", "w", encoding="utf-8")as f:
        f.write(res2)
    MainWindow.setStyleSheet('#MainWindow{background-color: #e8e8e8}')

def load_config():
    with open('config.json', 'r', encoding='utf-8') as fp:
        ll = json.load(fp)
    for i in ll:
        if i == "背景颜色":
            MainWindow.setStyleSheet(ll[i])

def data():
    #执行中返回选中数据
    dev=Phone_ID()
    buff=stop_refresh()
    if buff!=False and len(dev)>0:
        number=ui.comboBox.itemText(ui.comboBox.currentIndex())
        BrushPhoto(number)
    else:
        color_handle('-'*60)
        color_handle("未连接设备")

def color_handle(aa):
    arr = aa.split('\r\n')
    for i in arr:
        if len(i) > 0:
            #ff557f  #ABBABA 米白色
            ui.textBrowser.append('<font color="#ff557f">' +i + ' </font> ')

    # ui.textBrowser.append("<font color=\"#ABBABA\">" + aa + " </font> ")
    # ui.textBrowser.append('<color=#FFFFFF>' + aa + '</c>')
def BrushPhoto(text):
    try:
        list_index = ui.comboBox_2.currentIndex()
        dev=Phone_ID()
        if text == "第三方软件包名":
            cc=subprocess.Popen(f"adb -s {dev[list_index]} shell pm list packages -3",shell=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
            aa = cc.stdout.read().decode('GBK')
            color_handle('-'*60)
            color_handle(aa)
        elif text == "系统应用包名":
            cc = subprocess.Popen(f"adb -s {dev[list_index]} shell pm list packages -s", shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
            aa = cc.stdout.read().decode('GBK')
            color_handle('-'*60)
            color_handle(aa)
        elif text == "":
            pass
    except:
        color_handle('-' * 60)
        color_handle('设备连接异常,刷新重试')

def about():
    QMessageBox.about(MainWindow, "关于", "\n版本号：1.0.0")

def dev_all_adb(adb_grammar):
    deves = Phone_ID()
    buff = stop_refresh()
    list_index = ui.comboBox_2.currentIndex()
    dev_data=[]
    if len(deves) > 0 and buff != False:
        color_handle('-' * 60)
        for i in adb_grammar:
            cc = subprocess.Popen(f"adb -s {deves[list_index]} shell {i}", shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
            dev_data.append(cc.stdout.read().decode('GBK'))
    elif buff == False:
        color_handle("继续执行")
    else:
        color_handle('-' * 60)
        color_handle("未连接设备")
    return dev_data

def active_package():
    comboBoxAdd()
    try:
        adb_grammar=['dumpsys window | findstr mCurrentFocus']
        all_data=dev_all_adb(adb_grammar)
        package_name=all_data[0].split('u0')[1].split('/')[0].strip()
        pyperclip.copy(package_name)
        for i in all_data:
            if i=='':
                color_handle("信息未知")
            else:
                color_handle('包名已复制')
                color_handle(package_name)
    except:
        color_handle('-'*60)
        color_handle('获取包名异常')
def cpu_data():
    comboBoxAdd()
    try:
        adb_grammar=['cat /proc/cpuinfo']
        all_data=dev_all_adb(adb_grammar)
        for i in all_data:
            if i=='':
                color_handle("信息未知")
            else:
                color_handle(i)
    except:
        color_handle('-' * 60)
        color_handle('设备连接异常,请刷新重试！')

def all_phone_data():
    comboBoxAdd()
    try:
        adb_grammar=['getprop ro.build.version.release','getprop ro.product.brand','getprop ro.product.model'
            ,'cat /proc/meminfo |findstr MemTotal','getprop ro.serialno','wm size']
        adb_meaning=['安卓:','厂商:','手机型号:','','设备序列号:','']
        all_data=dev_all_adb(adb_grammar)
        j=0
        for i in all_data:
            if i=='':
                color_handle('-'*60)
                color_handle("信息未知")
            else:
                color_handle(adb_meaning[j]+i)
                j+=1
    except:
        color_handle('-'*60)
        color_handle('设备连接异常,请刷新重试！')

def data_ready_process():
    try:
        # process.waitForFinished(1000)
        data = str(process.readAll(),encoding='utf-8')
        # ui.textBrowser.append(data)
        color_handle(data)
    except:
        return

def data_ready_process1(ss):
    # process.waitForFinished(1000)
    data = str(ss.readAll(),encoding='utf-8')
    # ui.textBrowser.append(data)
    color_handle(data)

def stop_refresh():
    """ 清理所有进程
    """
    list_index = ui.comboBox_2.currentIndex()
    global process
    if process:
        reply = QMessageBox.warning(MainWindow,
                                    "提示",
                                    "当前有任务正在执行，是否停止操作",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            process.close()
            process = None
            dev = Phone_ID()
            path = 'log'
            if not os.path.exists(path):  # 判断地址是否有效，如果不存在就创建一个地址
                os.mkdir(path)
            NowTime = time.strftime(f"{dev[list_index]}-%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))  # 用时间戳定义截图名称
            logName = f'{NowTime}.txt'
            try:
                StrText = ui.textBrowser.toPlainText()
                qS = str(StrText)
                f = open(f'log/{logName}', 'w', encoding='UTF-8')
                f.write('{}'.format(qS))
                f.close()
                color_handle('日志打印完成，请至根目录下的log文件夹内查看')
                # 打开log文件夹
                os.startfile('log')
            except Exception as e:
                color_handle(e)
        elif reply == QMessageBox.No:
            return False
    return True

def get_log():
    try:
        list_index = ui.comboBox_2.currentIndex()
        dev=Phone_ID()
        buff = stop_refresh()
        if len(dev)>0 and buff!=False:
            global process
            process = QtCore.QProcess()
            # process.start("D:\\adb\\adb.exe",['-s', '65f8a4bd', 'logcat'])
            process.start("D:\\adb\\adb.exe", ['-s',dev[list_index],'logcat'])
            process.readyRead.connect(data_ready_process)
        elif buff == False:
            color_handle('-'*60)
            color_handle("继续执行")
        else:
            color_handle('-'*60)
            color_handle("未连接设备")
    except:
        color_handle('-'*60)
        color_handle('设备连接异常,刷新重试')

def text_backgroubd_config():
    with open('text_config.json', 'r', encoding='utf-8') as fp:
        ll = json.load(fp)
    for i in ll:
        if i == "背景颜色":
            ui.textBrowser.setStyleSheet(ll[i])

def text_backgroubd():
    stus = {'背景颜色': 'background-color: white'}
    res2 = json.dumps(stus, ensure_ascii=False)
    with open("text_config.json", "w", encoding="utf-8")as f:
        f.write(res2)
    ui.textBrowser.setStyleSheet('background-color: white')

def text_backgroubd_1():
    stus = {'背景颜色': 'background-color: black'}
    res2 = json.dumps(stus, ensure_ascii=False)
    with open("text_config.json", "w", encoding="utf-8")as f:
        f.write(res2)
    ui.textBrowser.setStyleSheet('background-color: black')


def android_control():
    """ 开启画面投屏
    """
    comboBoxAdd()
    dev=Phone_ID()
    if len(dev)>0:
        if len(dev)==1:
            for i in VirtualKey:
                color_handle(i)
            process1 = QtCore.QProcess()
            # process.start("D:\\adb\\adb.exe",['-s', '65f8a4bd', 'logcat'])
            # process.start("D:\\PyCharm 2020.1.1\\ui\\scrcpy\\scrcpy.exe", ['-s','450bfe2a'])
            process1.start(".\\scrcpy\\scrcpy.exe", [])
            process1.readyRead.connect(lambda :data_ready_process1(process1))
        else:
            color_handle(VirtualKey)
            # global process
            process1 = QtCore.QProcess()
            # process.start("D:\\adb\\adb.exe",['-s', '65f8a4bd', 'logcat'])
            # process.start("D:\\PyCharm 2020.1.1\\ui\\scrcpy\\scrcpy.exe", ['-s','450bfe2a'])
            process1.start(".\\scrcpy\\scrcpy.exe", ['-s',dev[list_index]])
            process1.readyRead.connect(lambda: data_ready_process1(process1))
    else:
        color_handle('-'*60)
        color_handle("设备未连接")

#----------------------------------------------------
global search_content
global search_key
global search_count
global search_current
search_key = None
search_content = None
search_count = 0
search_current = 0
def Qstring2Str(qStr):
    """转换Qstring类型为str类型"""
    return qStr



def select(start, length):
    """选中文字,高亮显示"""
    cur = QTextCursor(ui.textBrowser.textCursor())
    cur.setPosition(start)
    cur.setPosition(start + length, QTextCursor.KeepAnchor)
    ui.textBrowser.setTextCursor(cur)


def reset_search_content():
    global search_content
    global search_count
    global search_current
    """改变待搜索内容"""
    search_content = None
    search_count = 0
    search_current = 0



def search():
    """搜索"""
    global search_content
    global search_key
    global search_count
    global search_current

    key_word = Qstring2Str(ui.lineEdit.text().strip())
    if len(key_word) == 0:
        return
    if key_word != search_key:
        search_key = key_word
        search_count = 0
        search_current = 0
    if not search_content:
        search_content = Qstring2Str(ui.textBrowser.toPlainText())
    if not search_count:
        search_count = search_content.count(key_word)
        if search_count != 0:
            start = search_content.index(key_word)
            select(start, len(key_word))
            search_current += 1
    else:
        if search_current < search_count:
            start = search_content.find(key_word, ui.textBrowser.textCursor().position())
            if start != -1:
                select(start, len(key_word))
                search_current += 1
        else:
            search_count = 0
            search_current = 0
            search()
    ui.textBrowser.setFocus()
    ui.label.setText("{}/{}".format(search_current, search_count))

#----------------------------------------
def clean_log():
    list_devices=Phone_ID()
    dev_ch_name=comboBoxAdd()
    global process
    if len(list_devices)>0:
        if process:
            reply = QMessageBox.warning(MainWindow,
                                        "提示",
                                        "当前有任务正在执行，是否停止操作",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                process.close()
                process = None
            elif reply == QMessageBox.No:
                return False
        else:
            reply = QMessageBox.warning(MainWindow,
                                        "提示",
                                        "是否清空日志缓存，清除后信息不可找回！！！",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                if len(list_devices):
                    cc = subprocess.Popen(f"adb -s {list_devices[list_index]} logcat -c", shell=True,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
                    color_handle('-'*60)
                    color_handle(f"{dev_ch_name[list_index]}清理完成")
                else:
                    color_handle('-'*60)
                    color_handle("设备未连接")
            elif reply == QMessageBox.No:
                return False

def Help():
    color_handle('-' * 60)
    color_handle('(1).设备中文显示,请在main文件夹下找到devices_name.json文件进行添加设备ID')
    color_handle('(2).检查是否装有adb调试工具')
    color_handle('(3).获取手机日志时应用程序出现闪退，请先清空日志缓存后再次尝试')

#------------单个设备apk安装------------------
def install_one():
    list_index = ui.comboBox_2.currentIndex()
    dev = Phone_ID()
    if len(dev) > 0:
        apk_path = QFileDialog.getOpenFileName()
        if apk_path[0]!= '':
            process2(dev[list_index], apk_path[0])
        else:
            color_handle('-'*60)
            color_handle("未选择安装包")
    else:
        color_handle('-'*60)
        color_handle("设备未连接")

#------------批量安装apk------------------
def install_all():
    apk_path = QFileDialog.getOpenFileName()
    if apk_path[0]!= '':
        return apk_path[0]
    else:
        color_handle('-'*60)
        color_handle('未选择安装包')

# 多进程安装
def process2(device,a):
    process3 = QtCore.QProcess()
    process3.start("adb.exe", ['-s', device, 'install', '-r', a])
    process3.readyRead.connect(lambda: data_ready_process1(process3))

def main_install():
    dev=Phone_ID()
    if len(dev)>0:
        a = install_all()
        if a != None:
            for device in dev:
                process2(device,a)
    else:
        color_handle('-'*60)
        color_handle("设备未连接")

#--------------------------------
def updata_number():
    ui.label_2.setText(f"当前连接：{len(Phone_ID())}")
    comboBoxAdd()

def screenshot():
    try:
        list_index = ui.comboBox_2.currentIndex()
        dev = Phone_ID()
        if len(dev) > 0:
            Picture_name = time.strftime(f"%Y-%m-%d-%H-{dev[list_index]}", time.localtime(time.time()))  # 用时间戳定义截图名称
            os.system(f"adb -s {dev[list_index]} shell screencap -p /sdcard/{Picture_name}.png")
            # 同步到电脑相应文件夹
            # path = 'D:\\截图'
            path = '截图'
            if not os.path.exists(path):  # 判断地址是否有效，如果不存在就创建一个地址
                os.mkdir(path)
            os.system(f"adb -s {dev[list_index]} pull /sdcard/{Picture_name}.png {path}")
            # print(dev[list_index] + "截图完毕！")
            # 删除手机临时截图
            os.popen(f"adb -s {dev[list_index]} shell rm /sdcard/{Picture_name}.png")
            # 打开截图文件夹
            # os.popen('explorer.exe /n, D:\截图')
            os.popen('explorer.exe /n, 截图')
        else:
            color_handle('-'*60)
            color_handle("设备未连接")
    except:
        color_handle('-'*60)
        color_handle('设备连接异常,刷新重试')

# 单个设备卸载apk——进程写法
def uninstall_one_input():
    copy_name=pyperclip.paste()
    input_page_name = QInputDialog.getText(ui.pushButton_9,"卸载apk","请输入正确的包名:" ,QLineEdit.Normal, copy_name)[0]
    if input_page_name!= '':
        color_handle('卸载包名：'+input_page_name)
        return input_page_name
    else:
        color_handle('-'*60)
        color_handle('未输入包名')

def process_uninstall(device,a):
    process = QtCore.QProcess()
    process.start("adb.exe", ['-s', device, 'uninstall', a])
    process.readyRead.connect(lambda: data_ready_process1(process))


def uninstall_one():
    list_index = ui.comboBox_2.currentIndex()
    dev=Phone_ID()
    a = uninstall_one_input()
    if len(dev)>0:
        if a != None:
            process_uninstall(dev[list_index],a)
    else:
        color_handle('-'*60)
        color_handle("设备未连接")
#


#------------多进程批量卸载apk------------------
def uninstall_all_input():
    copy_name = pyperclip.paste()
    input_page_name = QInputDialog.getText(ui.pushButton_9,"卸载apk","请输入正确的包名:",QLineEdit.Normal, copy_name)[0]
    if input_page_name!= '':
        return input_page_name
    else:
        color_handle('-'*60)
        color_handle('未输入包名')



def uninstall_all():
    dev=Phone_ID()
    a = uninstall_all_input()
    if len(dev)>0:
        if a != None:
            for device in dev:
                process_uninstall(device,a)
    else:
        color_handle('-'*60)
        color_handle("设备未连接")

# 投屏所有设备
def Control1(device):
    process_android_control_all = QtCore.QProcess()
    process_android_control_all.start(".\\scrcpy\\scrcpy.exe", ['-s',device])
    process_android_control_all.readyRead.connect(lambda: data_ready_process1(process_android_control_all))

def android_control_all():
    dev=Phone_ID()
    dev_length = len(dev)
    if dev_length>0:
        # ui.textBrowser.append(VirtualKey)
        for d in dev:
            Control1(d)
    else:
        color_handle('-'*60)
        color_handle("设备未连接")

#------------多进程清理应用数据缓存------------------
def clear_all():
    copy_name = pyperclip.paste()
    input_page_name = QInputDialog.getText(ui.pushButton_11,"清理应用缓存","请输入正确的包名:",QLineEdit.Normal, copy_name)[0]
    dev = Phone_ID()
    dev_ch=comboBoxAdd()
    list_index = ui.comboBox_2.currentIndex()
    if input_page_name!= '':
        cc = subprocess.Popen(f"adb -s {dev[list_index]} shell pm list packages -3", shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        s = cc.stdout.read().decode('GBK')
        if input_page_name in s:
            return input_page_name
        else:
            color_handle('-'*60)
            color_handle(f'设备 {dev_ch[list_index]} 不存在此包名或该应用无法清理')
    else:
        color_handle('-'*60)
        color_handle('未输入包名')

def process_clear(device,a):
    process = QtCore.QProcess()
    process.start("adb.exe", ['-s', device, 'shell','pm','clear', a])
    process.readyRead.connect(lambda: data_ready_process1(process))

def main_clear():
    ff=stop_refresh()
    if ff==True:
        try:
            dev = Phone_ID()
            list_index = ui.comboBox_2.currentIndex()
            a = clear_all()
            if len(dev)>0:
                if a != None:
                    process_clear(dev[list_index], a)
            else:
                color_handle('-'*60)
                color_handle("设备未连接")
        except:
            color_handle('-'*60)
            color_handle("请检查设备连接")


def ScreenCAP():
    global lp_state
    comboBoxAdd()
    ff=stop_refresh()
    if ff==True:
        dev=Phone_ID()
        try:
            if len(dev)>0:
                if lp_state==0:
                    list_index = ui.comboBox_2.currentIndex()
                    video_name = time.strftime(f"%m-%d-%H_%M_%S_{dev[list_index]}",
                                               time.localtime(time.time()))  # 用时间戳定义截图名称
                    cc_time = input_ScreenCAP_time()
                    # ------------------
                    try:
                        inputData = int(cc_time)
                        if isinstance(inputData,int):
                            if inputData <= 180 and inputData > 0:
                                global screen_state
                                screen_state = 1
                                lp_th()
                                lp_state = 1
                                lp(dev[list_index],cc_time,video_name)
                            else:
                                color_handle('-'*60)
                                color_handle('请输入 1——180 以内的数字')
                    except:
                        color_handle('-'*60)
                        color_handle('请输入数字')
                    # -------------------
                else:
                    color_handle('当前录屏未执行完,请等待')
            else:
                color_handle('-'*60)
                color_handle("设备未连接")
        except:
            color_handle('-'*60)
            color_handle("请检查设备连接")

def input_ScreenCAP_time():
    input_time = QInputDialog.getText(ui.pushButton_14, "手机录屏", "请输入时间（＜180）")[0]
    return input_time

def data_ready_process1_lp(ss):
    data = str(ss.readAll(),encoding='utf-8')
    color_handle(data)

def started_lp():
    color_handle('-'*60)
    color_handle('正在录屏中')

def finished_lp(devies,video_name):
    global screen_state
    global lp_state
    # 同步到电脑相应文件夹
    path = '录屏'
    if not os.path.exists(path):  # 判断地址是否有效，如果不存在就创建一个地址
        os.mkdir(path)
    os.system(f"adb -s {devies} pull /sdcard/{video_name}.mp4 {path}")
    # # 打开录屏文件夹
    os.startfile('录屏')
    color_handle('-'*60)
    color_handle('录屏结束')
    lp_state=0
    screen_state=0


def lp(devies,time,video_name):
    try:
        process = QtCore.QProcess()
        process.started.connect(started_lp)
        process.start("adb.exe", ['-s',devies, 'shell','screenrecord', '--time-limit',time,f'//sdcard//{video_name}.mp4'])
        process.readyRead.connect(lambda: data_ready_process1_lp(process))
        process.finished.connect(lambda:finished_lp(devies,video_name))
    except:
        color_handle('-'*60)
        color_handle('请检查设备连接')

# def touch_phone():
#         for i in range(50):
#             time.sleep(0.2)
#             subprocess.Popen("adb shell input tap 550 550", shell=True,
#                                   stdout=subprocess.PIPE,
#                                   stderr=subprocess.PIPE)
#
# def proscess_tap():
#     p=Process(target=touch_phone,)
#     p.start()
def off_renwu():
    try:
        global process
        for i in range(2):
            time.sleep(0.2)
            subprocess.Popen("TASKKILL /F /IM adb.exe", shell=True)
            process = None
        color_handle('-' * 60)
        color_handle('任务已终止')
    except Exception as e:
        color_handle(e)

def py_test():
    color_handle('-' * 60)
    color_handle('这是一个测试按钮！')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    #去掉窗口边框
    # MainWindow.setWindowFlags(Qt.FramelessWindowHint)
    ui = test.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    updata_number()
    comboBoxAdd()
    load_config()
    text_backgroubd_config()
    #pushButton是按钮ID
    #获取设备ID
    ui.pushButton_2.clicked.connect(comboBoxAdd)
    #清除文本消息
    ui.pushButton_4.clicked.connect(clean)
    #背景颜色
    ui.actionh.triggered.connect(config_color)
    ui.actionb.triggered.connect(config_color1)
    #adb功能选择
    ui.pushButton_3.clicked.connect(data)
    #清除缓存
    ui.pushButton_7.clicked.connect(main_clear)
    #当前包名
    ui.pushButton_8.clicked.connect(active_package)
    #获取手机CPU
    ui.pushButton_9.clicked.connect(cpu_data)
    #录屏
    ui.pushButton_14.clicked.connect(ScreenCAP)
    # 一键显示
    ui.pushButton_11.clicked.connect(all_phone_data)
    #获取日志
    ui.pushButton_6.clicked.connect(get_log)
    #判断进程是否在执行
    ui.pushButton_12.clicked.connect(stop_refresh)
    #更改颜色
    ui.actionb_2.triggered.connect(text_backgroubd)
    ui.actionh_3.triggered.connect(text_backgroubd_1)

    #投屏
    ui.pushButton.clicked.connect(android_control)

    #信息搜索
    ui.textBrowser.textChanged.connect(reset_search_content)
    ui.pushButton_5.clicked.connect(search)

    #清空日志缓存
    ui.pushButton_13.clicked.connect(clean_log)
    #关于
    ui.actionhss.triggered.connect(about)
    #帮助
    ui.actionhelp.triggered.connect(Help)
    #装包
    ui.pushButton_15.clicked.connect(install_one)
    ui.pushButton_16.clicked.connect(main_install)
    #连接数量
    # ui.label_2.setText(f"当前连接：{len(Phone_ID())}")
    ui.pushButton_17.clicked.connect(updata_number)
    #截图
    ui.pushButton_18.clicked.connect(screenshot)
    #卸载
    ui.pushButton_19.clicked.connect(uninstall_one)
    ui.pushButton_20.clicked.connect(uninstall_all)
    #模拟点击
    ui.pushButton_10.clicked.connect(tap_number)
    ui.pushButton_21.clicked.connect(off_renwu)
    #测试按钮
    ui.pushButton_22.clicked.connect(py_test)
    sys.exit(app.exec_())
