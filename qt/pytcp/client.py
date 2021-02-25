#!/usr/bin/env python
# https://stackoverrun.com/ja/q/11331946
#
from PyQt5.QtCore import QDataStream, QIODevice
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket

class Client(QDialog):
       def __init__(self, parent=None):
              super(Client, self).__init__(parent)
              self.tcpSocket = QTcpSocket(self)
              self.blockSize = 0
              self.makeRequest()
              self.tcpSocket.waitForConnected(1000)
              # send any message you like it could come from a widget text.
              self.tcpSocket.write(b'hello')
              self.tcpSocket.readyRead.connect(self.dealCommunication)
              self.tcpSocket.error.connect(self.displayError)

       def makeRequest(self):
              HOST = '127.0.0.1'
              PORT = 8000
              self.tcpSocket.connectToHost(HOST, PORT, QIODevice.ReadWrite)

       def dealCommunication(self):
              instr = QDataStream(self.tcpSocket)
              instr.setVersion(QDataStream.Qt_5_0)
              if self.blockSize == 0:
                     if self.tcpSocket.bytesAvailable() < 2:
                            return
                     self.blockSize = instr.readUInt16()
              if self.tcpSocket.bytesAvailable() < self.blockSize:
                     return
              # Print response to terminal, we could use it anywhere else we wanted.
#              print(str(instr.readString(), encoding='ascii'))
              print(str(instr.readString()))

       def displayError(self, socketError):
              if socketError == QAbstractSocket.RemoteHostClosedError:
                     pass
              else:
                     print(self, "The following error occurred: %s." % self.tcpSocket.errorString())


if __name__ == '__main__':
       import sys

       app = QApplication(sys.argv)
       client = Client()
       sys.exit(client.exec_())
