#!/usr/bin/env python

import sys
from PyQt5.QtCore import QByteArray, QDataStream, QIODevice
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtNetwork import QHostAddress, QTcpServer

class Server(QDialog):
       def __init__(self, parent=None):
              super(Server, self).__init__(parent)
              self.tcpServer = None

       def sessionOpened(self):
              self.tcpServer = QTcpServer(self)
              PORT = 8000
              address = QHostAddress('127.0.0.1')
              if not self.tcpServer.listen(address, PORT):
                     print("cant listen!")
                     self.close()
                     return
              self.tcpServer.newConnection.connect(self.dealCommunication)
              
       def dealCommunication(self):
              # Get a QTcpSocket from the QTcpServer
              clientConnection = self.tcpServer.nextPendingConnection()
              # instantiate a QByteArray
              block = QByteArray()
              # QDataStream class provides serialization of binary data to a QIODevice
              out = QDataStream(block, QIODevice.ReadWrite)
              # We are using PyQt5 so set the QDataStream version accordingly.
              out.setVersion(QDataStream.Qt_5_0)
              out.writeUInt16(0)
              # this is the message we will send it could come from a widget.
              message = "Goodbye!"
              # get a byte array of the message encoded appropriately.
#              message = bytes(message, encoding='ascii')
              message = bytes(message)
              # now use the QDataStream and write the byte array to it.
              out.writeString(message)
              out.device().seek(0)
              out.writeUInt16(block.size() - 2)
              # wait until the connection is ready to read
              clientConnection.waitForReadyRead()
              # read incomming data
              instr = clientConnection.readAll()
              # in this case we print to the terminal could update text of a widget if we wanted.
#              print(str(instr, encoding='ascii'))
              print(str(instr))
              # get the connection ready for clean up
              clientConnection.disconnected.connect(clientConnection.deleteLater)
              # now send the QByteArray.
              clientConnection.write(block)
              # now disconnect connection.
              clientConnection.disconnectFromHost()
              
if __name__ == '__main__':
       app = QApplication(sys.argv)
       server = Server()
       server.sessionOpened()
       sys.exit(server.exec_())
                     
