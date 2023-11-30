# -*- coding: utf-8 -*-

import sys
import struct

from ui_form1 import Ui_MainWindow1
from ui_form2 import Ui_MainWindow2
from ui_form3 import Ui_MainWindow3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtCore
from time import sleep
import serial
import serial.tools.list_ports
import threading
import time


def UiInit():
    MainWindow1.pushButton.clicked.connect(MainWindow1.openSerial)
    MainWindow1.pushButton_2.clicked.connect(
        lambda: MainWindow2.move(MainWindow1.pos())
    )
    MainWindow1.pushButton_2.clicked.connect(MainWindow2.show)
    MainWindow1.pushButton_2.clicked.connect(MainWindow1.hide)
    MainWindow1.pushButton_3.clicked.connect(
        lambda: MainWindow3.move(
            MainWindow1.pos().x() + 300,
            MainWindow1.pos().y(),
        )
    )
    MainWindow1.pushButton_3.clicked.connect(MainWindow3.PushButtonPressEvent)
    MainWindow1.pushButton_5.clicked.connect(MainWindow1.refresh)

    MainWindow2.pushButton_3.clicked.connect(
        lambda: MainWindow3.move(
            MainWindow2.pos().x() + 300,
            MainWindow2.pos().y(),
        )
    )
    MainWindow2.pushButton_3.clicked.connect(MainWindow3.PushButtonPressEvent)
    MainWindow2.pushButton_4.clicked.connect(
        lambda: MainWindow1.move(MainWindow2.pos())
    )
    MainWindow2.pushButton_4.clicked.connect(MainWindow1.show)
    MainWindow2.pushButton_4.clicked.connect(MainWindow2.hide)
    MainWindow2.pushButton_2.clicked.connect(
        lambda: MainWindow1.send(
            [
                MainWindow2.doubleSpinBox.value(),
                MainWindow2.doubleSpinBox_2.value(),
                MainWindow2.doubleSpinBox_3.value(),
                MainWindow2.doubleSpinBox_4.value(),
            ]
        )
    )

    MainWindow2.checkBox.stateChanged.connect(
        lambda: MainWindow2.checkBox_stateChanged(MainWindow2.checkBox),
    )
    MainWindow2.checkBox_2.stateChanged.connect(
        lambda: MainWindow2.checkBox_stateChanged(MainWindow2.checkBox_2),
    )
    MainWindow2.doubleSpinBox.valueChanged.connect(
        lambda: MainWindow2.doubleSpinBox_valueChanged(
            MainWindow2.doubleSpinBox
        ),
    )
    MainWindow2.doubleSpinBox_2.valueChanged.connect(
        lambda: MainWindow2.doubleSpinBox_valueChanged(
            MainWindow2.doubleSpinBox_2
        ),
    )
    MainWindow2.doubleSpinBox_3.valueChanged.connect(
        lambda: MainWindow2.doubleSpinBox_valueChanged(
            MainWindow2.doubleSpinBox_3
        ),
    )
    MainWindow2.doubleSpinBox_4.valueChanged.connect(
        lambda: MainWindow2.doubleSpinBox_valueChanged(
            MainWindow2.doubleSpinBox_4
        ),
    )

    MainWindow2.verticalSlider_3.valueChanged.connect(
        lambda: MainWindow2.target_valueChanged(MainWindow2.verticalSlider_3),
    )
    MainWindow2.verticalSlider_2.valueChanged.connect(
        lambda: MainWindow2.target_valueChanged(MainWindow2.verticalSlider_2),
    )
    MainWindow2.verticalSlider.valueChanged.connect(
        lambda: MainWindow2.target_valueChanged(MainWindow2.verticalSlider),
    )

    MainWindow2.dial.valueChanged.connect(
        lambda: MainWindow2.target_valueChanged(MainWindow2.dial),
    )


class main_ui1(QMainWindow, Ui_MainWindow1):
    def __init__(self):
        super(main_ui1, self).__init__()
        self.setupUi(self)

    def closeSerial(self):
        self.ser.close()
        print(self.ser.name + " closed\r\n")
        self.pushButton.setStyleSheet("background-color: white")
        self.pushButton.setText("打开串口")
        self.pushButton.clicked.disconnect(self.closeSerial)
        self.pushButton.clicked.connect(self.openSerial)

    def openSerial(self):
        self.stopbits_dicts = {
            1: serial.STOPBITS_ONE,
            1.5: serial.STOPBITS_ONE_POINT_FIVE,
            2: serial.STOPBITS_TWO,
        }
        self.databits_dicts = {
            8: serial.EIGHTBITS,
            7: serial.SEVENBITS,
            6: serial.SIXBITS,
            5: serial.FIVEBITS,
        }
        self.parity_dicts = {
            "无": serial.PARITY_NONE,
            "奇校验": serial.PARITY_ODD,
            "偶校验": serial.PARITY_EVEN,
        }
        try:
            self.port = self.comboBox.currentText()
            self.baudrate = self.comboBox_2.currentText()
            self.stopbits = self.stopbits_dicts[
                int(self.comboBox_3.currentText())
            ]
            self.databits = self.databits_dicts[
                int(self.comboBox_4.currentText())
            ]
            self.parity = self.parity_dicts[self.comboBox_5.currentText()]
            self.ser = serial.Serial(
                self.port,
                baudrate=self.baudrate,
                stopbits=self.stopbits,
                bytesize=self.databits,
                parity=self.parity,
                timeout=0.5,
            )
            self.ser.flush()
            print(self.port.encode("utf-8") + b" opened\r\n")
            thread1 = threading.Thread(target=self.readSerial)
            thread1.start()
            self.pushButton.setStyleSheet("background-color: green")
            self.pushButton.setText("关闭串口")
            self.pushButton.clicked.disconnect(self.openSerial)
            self.pushButton.clicked.connect(self.closeSerial)
        except ValueError:
            print("[ERROR]未选定波特率!")
            self.comboBox_2.setStyleSheet("background-color: red")
            QMessageBox.warning(
                self,
                "警告",
                "你还未选定波特率!"
            )
            time.sleep(0.5)
            self.comboBox_2.setStyleSheet("background-color: white")
            return
        except serial.serialutil.SerialException:
            QMessageBox.critical(
                self,
                "超时",
                "未能正常打开串口!"
            )
            print("[ERROR]未能正常打开串口!")
            return

    def readSerial(self):
        while (True):
            try:
                headFrame1 = ord(self.ser.read())
                if headFrame1 == 0xF5:
                    headFrame2 = ord(self.ser.read())
                    if headFrame2 == 0xF5:
                        toolFrame = ord(self.ser.read())
                        dataLenFrame = int(self.ser.read())
                        dataFrame = int(self.ser.read(dataLenFrame))
                        lastFrame = ord(self.ser.read())
                    if lastFrame == 0x5F:
                        print(toolFrame, dataFrame)
            except Exception:
                break

    def refresh(self):
        _translate = QtCore.QCoreApplication.translate
        port_list = list(serial.tools.list_ports.comports())
        self.comboBox.clear()
        if len(port_list) != 0:
            for i in range(len(port_list)):
                self.comboBox.addItem("")
                self.comboBox.setItemText(
                    i,
                    _translate("MainWindow", port_list[i][0]),
                )
                print(port_list[i][0])

    def window2_checkBox_stateChanged(self, flag):
        if not self.serial_test():
            return False
        if flag[0]:
            if flag[1]:
                self.ser.write(b"[stateChanged:pid:on]\r\n")
                print("[INFO]发送[stateChanged:pid:on]\r\n")
                return True
            self.ser.write(b"[stateChanged:pid:off]\r\n")
            print("[INFO]发送[stateChanged:pid:off]\r\n")
            return True
        if flag[1]:
            self.ser.write(b"[stateChanged:velocity:on]\r\n")
            print("[INFO]发送[stateChanged:velocity:on]\r\n")
            return True
        self.ser.write(b"[stateChanged:velocity:off]\r\n")
        print("[INFO]发送[stateChanged:velocity:off]\r\n")
        return True

    def window2_doubleSpinBox_valueChanged(self, flag, value):
        if not self.serial_test():
            return False
        if flag == 0:
            self.ser.write(
                b"[pid:set:kp:"
                + str("{:.2f}".format(value)).encode("utf-8")
                + b"]\r\n"
            )
            print("[INFO]发送[pid:set:kp:{:.2f}".format(value), "]\r\n")
            return True
        elif flag == 1:
            self.ser.write(
                    b"[pid:set:ki:"
                    + str("{:.2f}".format(value)).encode("utf-8")
                    + b"]\r\n"
                )
            print("[INFO]发送[pid:set:ki:{:.2f}".format(value), "]\r\n")
            return True
        elif flag == 2:
            self.ser.write(
                b"[pid:set:kd:"
                + str("{:.2f}".format(value)).encode("utf-8")
                + b"]\r\n"
            )
            print("[INFO]发送[pid:set:kd:{:.2f}".format(value), "]\r\n")
            return True
        elif flag == 3:
            self.ser.write(
                b"[pid:set:v:"
                + str(value).encode("utf-8")
                + b"]\r\n"
            )
            print("[INFO]发送[pid:set:v:{:.2f}".format(value), "]\r\n")
            return True

    def window2_keyPressEvent(self, key):
        self.keyBoard_dicts = {
                QtCore.Qt.Key_W: b"[keyBoard:W]\r\n",
                QtCore.Qt.Key_A: b"[keyBoard:A]\r\n",
                QtCore.Qt.Key_S: b"[keyBoard:S]\r\n",
                QtCore.Qt.Key_D: b"[keyBoard:D]\r\n",
                QtCore.Qt.Key_Q: b"[keyBoard:Q]\r\n",
                QtCore.Qt.Key_E: b"[keyBoard:E]\r\n",
            }
        if not self.serial_test():
            return False
        if self.keyBoard_dicts.get(key) is None:
            return
        print("[INFO]发送", self.keyBoard_dicts.get(key))

    def send(self, info):
        if not self.serial_test():
            return False
        self.ser.write(
            b"[pid:set:kp:"
            + str("{:.2f}".format(info[0])).encode("utf-8")
            + b"]\r\n"
        )
        print("[INFO]发送[pid:set:kp:{:.2f}".format(info[0]), "]\r\n")
        self.ser.write(
            b"[pid:set:ki:"
            + str("{:.2f}".format(info[1])).encode("utf-8")
            + b"]\r\n"
        )
        print("[INFO]发送[pid:set:ki:{:.2f}".format(info[1]), "]\r\n")
        self.ser.write(
            b"[pid:set:kd:"
            + str("{:.2f}".format(info[2])).encode("utf-8")
            + b"]\r\n"
        )
        print("[INFO]发送[pid:set:kd:{:.2f}".format(info[2]), "]\r\n")
        self.ser.write(
            b"[pid:set:v:"
            + str("{:.2f}".format(info[3])).encode("utf-8")
            + b"]\r\n"
        )
        print("[INFO]发送[pid:set:v:{:.2f}".format(info[3]), "]\r\n")

    def serial_test(self):
        try:
            if not self.ser.isOpen():
                raise AttributeError("串口未开启!")
            return True
        except AttributeError:
            QMessageBox.warning(
                self,
                "警告",
                "你还未打开串口!"
            )
            print("[ERROR]串口未开启!\r\n")
            return False


class main_ui2(QMainWindow, Ui_MainWindow2):
    def __init__(self):
        super(main_ui2, self).__init__()
        self.setupUi(self)
        self.lastTime = 0

    def checkBox_stateChanged(self, checkBox):
        self.flag = False
        if checkBox == self.checkBox:
            self.flag = True
        if not MainWindow1.window2_checkBox_stateChanged(
            [self.flag, checkBox.isChecked()]
        ):
            checkBox.blockSignals(True)
            checkBox.setCheckState(False)
            checkBox.blockSignals(False)

    def doubleSpinBox_valueChanged(self, doubleSpinBox):
        self.switcher = {
            self.doubleSpinBox: 0,
            self.doubleSpinBox_2: 1,
            self.doubleSpinBox_3: 2,
            self.doubleSpinBox_4: 3,
        }
        self.switcher2 = {
            self.doubleSpinBox: self.verticalSlider_3,
            self.doubleSpinBox_2: self.verticalSlider_2,
            self.doubleSpinBox_3: self.verticalSlider,
            self.doubleSpinBox_4: self.dial,
        }
        self.target = self.switcher2.get(doubleSpinBox)
        self.flag = self.switcher.get(doubleSpinBox)
        if not MainWindow1.window2_doubleSpinBox_valueChanged(
            self.flag, doubleSpinBox.value()
        ):
            doubleSpinBox.blockSignals(True)
            doubleSpinBox.setValue(0)
            sleep(0.5)
            doubleSpinBox.blockSignals(False)
            return
        self.target.blockSignals(True)
        self.target.setValue(int(doubleSpinBox.value() * 100))
        self.target.blockSignals(False)

    def target_valueChanged(self, target):
        self.switcher = {
            self.verticalSlider_3: 0,
            self.verticalSlider_2: 1,
            self.verticalSlider: 2,
            self.dial: 3,
        }
        self.switcher2 = {
            self.verticalSlider: self.doubleSpinBox_3,
            self.verticalSlider_2: self.doubleSpinBox_2,
            self.verticalSlider_3: self.doubleSpinBox,
            self.dial: self.doubleSpinBox_4,
        }
        self.flag = self.switcher.get(target)
        self.doubleSpinBox = self.switcher2.get(target)
        if not MainWindow1.window2_doubleSpinBox_valueChanged(
            self.flag, target.value() / 100
        ):
            target.blockSignals(True)
            target.setValue(0)
            sleep(0.5)
            target.blockSignals(False)
            return
        self.doubleSpinBox.blockSignals(True)
        self.doubleSpinBox.setValue(target.value() / 100)
        self.doubleSpinBox.blockSignals(False)

    def keyPressEvent(self, event):
        self.dTime = time.time() - self.lastTime
        if (self.dTime >= 0.05):
            print(self.dTime)
            MainWindow1.window2_keyPressEvent(event.key())
            self.lastTime = time.time()


class main_ui3(QMainWindow, Ui_MainWindow3):
    def __init__(self):
        super(main_ui3, self).__init__()
        self.setupUi(self)

    def PushButtonPressEvent(self):
        if self.isVisible():
            self.hide()
            return
        self.show()


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(
        QtCore.Qt.AA_EnableHighDpiScaling
    )
    app = QApplication(sys.argv)
    MainWindow1 = main_ui1()
    MainWindow2 = main_ui2()
    MainWindow3 = main_ui3()
    MainWindow1.show()
    UiInit()
    sys.exit(app.exec_())
