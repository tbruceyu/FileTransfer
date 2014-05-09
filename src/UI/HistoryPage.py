#!/usr/bin/env python
# -*- coding: utf-8 -*-
# View the file transfer history
from PyQt4 import QtGui
from core.transferPC import HistoryThread
import os

class HistoryPageWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(HistoryPageWindow, self).__init__(parent)
        self.resize(400, 300)
        self.createGUI()
        self.thread = HistoryThread()
        self.thread.signalCallback.connect(self.addRow)
        self.thread.start()
    def createGUI(self):
        self.table = QtGui.QTableWidget(0, 4)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setHorizontalHeaderLabels(["id", "Name", "Time", "Comment"])
        self.table.verticalHeader().setVisible(False)
        self.table.resize(400, 300)
        self.table.cellDoubleClicked.connect(self.cellDoubleClicked)
        self.table.resizeColumnToContents(0)
        self.table.horizontalHeader().setStretchLastSection(True)

        layout = QtGui.QGridLayout()
        layout.addWidget(self.table, 0, 0)
        self.setLayout(layout)

        self.setWindowTitle("File history")
    def addRow(self, data):
        index = self.table.rowCount()
        self.table.insertRow(index)
        self.table.setItem(index, 0, QtGui.QTableWidgetItem(str(data['id'])))
        self.table.setItem(index, 1, QtGui.QTableWidgetItem(data['name']))
        self.table.setItem(index, 2, QtGui.QTableWidgetItem(data['date']))
        self.table.setItem(index, 3, QtGui.QTableWidgetItem(data['comment']))
    def cellDoubleClicked (self, x, y):
        os.startfile(self.thread.data[x]['path'])
