from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex, QSortFilterProxyModel
from PySide2.QtGui import QColor
from pydantic import BaseModel
import typing


class Message(BaseModel):
    login: str
    proxie: str
    text: str
    status: int = 0


class MessagesModel(QAbstractTableModel):
    def __init__(self):
        QAbstractTableModel.__init__(self)
        self.messages : typing.List[Message] = []
        self.columns = ("Логин", "Прокси", "Сообщение")

    def rowCount(self, parent=QModelIndex()):
        return len(self.messages)

    def columnCount(self, parent=QModelIndex()):
        return len(self.columns)

    def insertRow(self, message: Message, row=1, parent=QModelIndex()) -> bool:
        row = self.rowCount()
        self.beginInsertRows(QModelIndex(), row, row)
        self.messages.append(message)
        self.endInsertRows()
        return True

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.columns[section]
        else:
            return "{}".format(section)

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            if column == 0:
                return self.messages[row].login
            elif column == 1:
                return self.messages[row].proxie
            elif column == 2:
                return self.messages[row].text
        elif role == Qt.BackgroundRole:
            message: Message = self.messages[row]
            return {
                0: QColor(Qt.yellow),
                1: QColor(Qt.green),
                2: QColor(Qt.red),
                3: QColor(Qt.cyan)
            }.get(message.status, QColor(Qt.white))
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight
        return None


class MessageFilterSortProxy(QSortFilterProxyModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.filterFlags = []

    def setFilterFlags(self, flags):
        if flags != self.filterFlags:
            self.filterFlags = flags
            self.invalidateFilter()

    def filterAcceptsRow(self, sourceRow, sourceParent):
        model = self.sourceModel()
        return model.messages[sourceRow].status + 1 in self.filterFlags