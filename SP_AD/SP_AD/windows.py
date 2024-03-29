from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import client
import speech2text
import record

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

port = 8888

class CWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 200, 338, 600)

        self.c = client.ClientSocket(self)

        self.initUI()

    def __del__(self):
        self.c.stop()

    def initUI(self):

        self.setWindowTitle('클라이언트')


        # 클라이언트 설정 부분
        ipbox = QHBoxLayout()


        gb = QGroupBox('서버 설정')
        ipbox.addWidget(gb)

        box = QHBoxLayout()

        label = QLabel('Server IP')
        self.ip = QLineEdit()
        self.ip.setStyleSheet("QLineEdit{background: white; color: black;}")

        opacity_effect = QGraphicsOpacityEffect(self.ip)
        opacity_effect.setOpacity(0.9)
        self.ip.setGraphicsEffect(opacity_effect)

        box.addWidget(label)
        box.addWidget(self.ip)

        label = QLabel('Server Port')
        self.port = QLineEdit(str(port))
        self.port.setStyleSheet("QLineEdit{background: white; color: black;}")

        opacity_effect = QGraphicsOpacityEffect(self.port)
        opacity_effect.setOpacity(0.9)
        self.port.setGraphicsEffect(opacity_effect)
        box.addWidget(label)
        box.addWidget(self.port)

        label = QLabel('닉네임')
        self.nickname = QLineEdit()
        self.nickname.setStyleSheet("QLineEdit{background: white; color: black;}")
        opacity_effect = QGraphicsOpacityEffect(self.nickname)
        opacity_effect.setOpacity(0.9)
        self.nickname.setGraphicsEffect(opacity_effect)
        box.addWidget(label)
        box.addWidget(self.nickname)



        self.btn = QPushButton('접속')
        self.btn.clicked.connect(self.connectClicked)
        box.addWidget(self.btn)

        gb.setLayout(box)

        # 채팅창 부분
        infobox = QHBoxLayout()
        gb = QGroupBox('메시지')
        infobox.addWidget(gb)

        box = QVBoxLayout()

        label = QLabel('받은 메시지')
        box.addWidget(label)

        self.recvmsg = QListWidget()

        opacity_effect = QGraphicsOpacityEffect(self.recvmsg)
        opacity_effect.setOpacity(0.9)
        self.recvmsg.setGraphicsEffect(opacity_effect)
        self.recvmsg.setStyleSheet("QListWidget{background: white; color: black;}")
        box.addWidget(self.recvmsg)


        label = QLabel('보낼 메시지')
        box.addWidget(label)

        self.sendmsg = QTextEdit()
        self.sendmsg.setStyleSheet("QTextEdit{background: white; color: black;}")
        self.sendmsg.setFixedHeight(50)
        opacity_effect = QGraphicsOpacityEffect(self.sendmsg)
        opacity_effect.setOpacity(0.9)
        self.sendmsg.setGraphicsEffect(opacity_effect)
        box.addWidget(self.sendmsg)



        hbox = QHBoxLayout()

        box.addLayout(hbox)
        self.sendbtn = QPushButton('보내기')
        self.sendbtn.setAutoDefault(True)
        self.sendbtn.clicked.connect(self.sendMsg)

        self.clearbtn = QPushButton('채팅창 지움')
        self.clearbtn.clicked.connect(self.clearMsg)

        self.speech2text = QPushButton('음성으로 말하기')
        self.speech2text.clicked.connect(self.speech_text)

        hbox.addWidget(self.sendbtn)
        hbox.addWidget(self.clearbtn)
        hbox.addWidget(self.speech2text)
        gb.setLayout(box)

        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(ipbox)
        vbox.addLayout(infobox)
        self.setLayout(vbox)

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap('145.jpg')))
        self.setPalette(palette)

        self.show()

    def connectClicked(self):
        if self.c.bConnect == False:
            ip = self.ip.text()
            port = self.port.text()
            if self.c.connectServer(ip, int(port)):
                self.btn.setText('접속 종료')
            else:
                self.c.stop()
                self.sendmsg.clear()
                self.recvmsg.clear()
                self.btn.setText('접속')
        else:
            self.c.stop()
            self.sendmsg.clear()
            self.recvmsg.clear()
            self.btn.setText('접속')

    def updateMsg(self, msg):
        self.recvmsg.addItem(QListWidgetItem(msg))

    def updateDisconnect(self):
        self.btn.setText('접속')

    def sendMsg(self):
        sendmsg = self.sendmsg.toPlainText()
        self.c.send(self.nickname.text()+' : ' + sendmsg)
        self.sendmsg.clear()

    def clearMsg(self):
        self.recvmsg.clear()
    def speech_text(self):
        record.reco(10)
        self.sendmsg.setText(speech2text.sp2te())



    def closeEvent(self, e):
        self.c.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())