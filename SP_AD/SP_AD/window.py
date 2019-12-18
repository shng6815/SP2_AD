from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import socket
import server

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

port = 8888


class CWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.s = server.ServerSocket(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('서버')

        # 서버 설정 부분
        ipbox = QHBoxLayout()

        gb = QGroupBox('서버 설정')
        ipbox.addWidget(gb)

        box = QHBoxLayout()

        label = QLabel('Server IP')
        self.ip = QLineEdit(socket.gethostbyname(socket.gethostname()))
        box.addWidget(label)
        box.addWidget(self.ip)

        label = QLabel('Server Port')
        self.port = QLineEdit(str(port))
        box.addWidget(label)
        box.addWidget(self.port)

        self.btn = QPushButton('서버 실행')
        self.btn.setCheckable(True)
        self.btn.toggled.connect(self.toggleButton)
        box.addWidget(self.btn)

        gb.setLayout(box)

        # 접속자 정보 부분
        infobox = QHBoxLayout()
        gb = QGroupBox('접속자 정보')
        infobox.addWidget(gb)

        box = QHBoxLayout()

        self.guest = QTableWidget()
        self.guest.setRowCount(5)
        self.guest.setColumnCount(2)
        self.guest.setHorizontalHeaderItem(0, QTableWidgetItem('ip'))
        self.guest.setHorizontalHeaderItem(1, QTableWidgetItem('port'))

        box.addWidget(self.guest)
        gb.setLayout(box)

        # 채팅창 부분
        gb = QGroupBox('메시지')
        infobox.addWidget(gb)

        box = QVBoxLayout()

        label = QLabel('받은 메시지')
        box.addWidget(label)

        self.msg = QListWidget()
        box.addWidget(self.msg)

        label = QLabel('보낼 메시지')
        box.addWidget(label)

        self.sendmsg = QLineEdit()
        box.addWidget(self.sendmsg)

        hbox = QHBoxLayout()

        self.sendbtn = QPushButton('보내기')
        self.sendbtn.clicked.connect(self.sendMsg)
        hbox.addWidget(self.sendbtn)

        self.clearbtn = QPushButton('채팅창 지움')
        self.clearbtn.clicked.connect(self.clearMsg)
        hbox.addWidget(self.clearbtn)

        box.addLayout(hbox)

        gb.setLayout(box)

        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(ipbox)
        vbox.addLayout(infobox)
        self.setLayout(vbox)

        self.show()

    def toggleButton(self, state):
        if state:
            ip = self.ip.text()
            port = self.port.text()
            if self.s.start(ip, int(port)):
                self.btn.setText('서버 종료')
        else:
            self.s.stop()
            self.msg.clear()
            self.btn.setText('서버 실행')

    def updateClient(self):
        self.guest.clearContents()
        i = 0
        for ip in self.s.ip:
            self.guest.setItem(i, 0, QTableWidgetItem(ip[0]))
            self.guest.setItem(i, 1, QTableWidgetItem(str(ip[1])))
            i += 1

    def updateMsg(self, msg):
        self.msg.addItem(QListWidgetItem(msg))
        self.msg.setCurrentRow(self.msg.count() - 1)

    def sendMsg(self):
        if not self.s.bListen:
            self.sendmsg.clear()
            return
        sendmsg = self.sendmsg.text()
        self.updateMsg(sendmsg)
        print(sendmsg)
        self.s.send(sendmsg)
        print(type(sendmsg))
        self.sendmsg.clear()

    def clearMsg(self):
        self.msg.clear()

    def closeEvent(self, e):
        self.s.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())