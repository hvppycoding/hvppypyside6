import sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.createIconGroupBox()
        self.createMessageGroupBox()
        self.iconLabel.setMinimumWidth(self.durationLabel.sizeHint().width())
        self.createActions()
        self.createTrayIcon()
        self.showMessageButton.clicked.connect(self.showMessage)
        self.showIconCheckBox.toggled.connect(self.trayIcon.setVisible)
        self.iconComboBox.currentIndexChanged.connect(self.setIcon)
        self.trayIcon.messageClicked.connect(self.messageClicked)
        self.trayIcon.activated.connect(self.iconActivated)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.iconGroupBox)
        self.mainLayout.addWidget(self.messageGroupBox)
        self.setLayout(self.mainLayout)
        self.iconComboBox.setCurrentIndex(1)
        self.trayIcon.show()
        self.setWindowTitle("Systray")
        self.resize(400, 300)
        
    def setVisible(self, visible):
        self.minimizeAction.setEnabled(visible)
        self.maximizeAction.setEnabled(not self.isMaximized())
        self.restoreAction.setEnabled(self.isMaximized() or not visible)
        super().setVisible(visible)
        
    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            QMessageBox.information(self, self.tr("Systray"),
                                    self.tr("The program will keep running in the "
                                        "system tray. To terminate the program, "
                                        "choose <b>Quit</b> in the context menu "
                                        "of the system tray entry."))
            self.hide()
            event.ignore()

    def setIcon(self, index):
        icon = self.iconComboBox.itemIcon(index)
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)
        self.trayIcon.setToolTip(self.iconComboBox.itemText(index))
        
    def iconActivated(self, reason):
        if reason == QSystemTrayIcon.Trigger or reason == QSystemTrayIcon.DoubleClick:
            self.iconComboBox.setCurrentIndex((self.iconComboBox.currentIndex() + 1) % self.iconComboBox.count())
        elif reason == QSystemTrayIcon.MiddleClick:
            self.showMessage()
            
    def showMessage(self):
        self.showIconCheckBox.setChecked(True)
        selectedIndex = self.typeComboBox.currentIndex()
        msgIcon = self.typeComboBox.itemData(selectedIndex)

        if selectedIndex == -1:
            icon = QIcon(self.iconComboBox.itemIcon(self.iconComboBox.currentIndex()))
            self.trayIcon.showMessage(self.titleEdit.text(), self.bodyEdit.toPlainText(), icon,
                                      self.durationSpinBox.value() * 1000)
        else:
            self.trayIcon.showMessage(self.titleEdit.text(), self.bodyEdit.toPlainText(), msgIcon,
                                      self.durationSpinBox.value() * 1000)
            
    def messageClicked(self):
        QMessageBox.information(None, self.tr("Systray"),
                            self.tr("Sorry, I already gave what help I could.\n"
                            "Maybe you should try asking a human?"))
        
    def createIconGroupBox(self):
        self.iconGroupBox = QGroupBox(self.tr("Tray Icon"))
        self.iconLabel = QLabel("Icon:")
        self.iconComboBox = QComboBox()
        qtIcon = self.style().standardIcon(QStyle.SP_TitleBarMenuButton)
        self.iconComboBox.addItem(qtIcon, "Qt")
        hdIcon = self.style().standardIcon(QStyle.SP_DriveHDIcon)
        self.iconComboBox.addItem(hdIcon, "Hard disk")
        volumeIcon = self.style().standardIcon(QStyle.SP_MediaVolume)
        self.iconComboBox.addItem(volumeIcon, "Volume")

        self.showIconCheckBox = QCheckBox(self.tr("Show icon"))
        self.showIconCheckBox.setChecked(True)

        self.iconLayout = QHBoxLayout()
        self.iconLayout.addWidget(self.iconLabel)
        self.iconLayout.addWidget(self.iconComboBox)
        self.iconLayout.addStretch();
        self.iconLayout.addWidget(self.showIconCheckBox)
        self.iconGroupBox.setLayout(self.iconLayout)
        
    def createMessageGroupBox(self):
        self.messageGroupBox = QGroupBox(self.tr("Balloon Message"))
        self.typeLabel = QLabel(self.tr("Type:"))
        self.typeComboBox = QComboBox()
        self.typeComboBox.addItem("None", QSystemTrayIcon.NoIcon)
        infoIcon = self.style().standardIcon(QStyle.SP_MessageBoxInformation)
        self.typeComboBox.addItem(infoIcon, "Information", QSystemTrayIcon.Information)
        warnIcon = self.style().standardIcon(QStyle.SP_MessageBoxWarning)
        self.typeComboBox.addItem(warnIcon, "Warning", QSystemTrayIcon.Warning)
        criticalIcon = self.style().standardIcon(QStyle.SP_MessageBoxCritical)
        self.typeComboBox.addItem(criticalIcon, "Critical", QSystemTrayIcon.Critical)
        self.typeComboBox.addItem(QIcon(), "Custom icon", -1)
        self.typeComboBox.setCurrentIndex(1)

        self.durationLabel = QLabel("Duration:")

        self.durationSpinBox = QSpinBox()
        self.durationSpinBox.setRange(5, 60);
        self.durationSpinBox.setSuffix(" s");
        self.durationSpinBox.setValue(15);

        self.durationWarningLabel = QLabel("(some systems might ignore this hint)")
        self.durationWarningLabel.setIndent(10);

        self.titleLabel = QLabel("Title:")

        self.titleEdit = QLineEdit("Cannot connect to network")

        self.bodyLabel = QLabel("Body:")

        self.bodyEdit = QTextEdit()
        self.bodyEdit.setPlainText("Don't believe me. Honestly, I don't have a "
                                "clue.\nClick this balloon for details.")

        self.showMessageButton = QPushButton("Show Message")
        self.showMessageButton.setDefault(True);

        self.messageLayout = QGridLayout()
        self.messageLayout.addWidget(self.typeLabel, 0, 0);
        self.messageLayout.addWidget(self.typeComboBox, 0, 1, 1, 2);
        self.messageLayout.addWidget(self.durationLabel, 1, 0);
        self.messageLayout.addWidget(self.durationSpinBox, 1, 1);
        self.messageLayout.addWidget(self.durationWarningLabel, 1, 2, 1, 3);
        self.messageLayout.addWidget(self.titleLabel, 2, 0);
        self.messageLayout.addWidget(self.titleEdit, 2, 1, 1, 4);
        self.messageLayout.addWidget(self.bodyLabel, 3, 0);
        self.messageLayout.addWidget(self.bodyEdit, 3, 1, 2, 4);
        self.messageLayout.addWidget(self.showMessageButton, 5, 4);
        self.messageLayout.setColumnStretch(3, 1);
        self.messageLayout.setRowStretch(4, 1);
        self.messageGroupBox.setLayout(self.messageLayout);
    
    def createActions(self):
        self.minimizeAction = QAction("Mi&nimize", self)
        self.minimizeAction.triggered.connect(self.hide)

        self.maximizeAction = QAction("Ma&ximize", self)
        self.maximizeAction.triggered.connect(self.showMaximized)

        self.restoreAction = QAction("&Restore", self)
        self.restoreAction.triggered.connect(self.showNormal)

        self.quitAction = QAction("&Quit", self)
        self.quitAction.triggered.connect(QCoreApplication.quit)

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.minimizeAction)
        self.trayIconMenu.addAction(self.maximizeAction)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)

def main():
    print("START")
    app = QApplication(sys.argv)
    
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Systray",
            "I couldn't detect any system tray on this system.")
        sys.exit(1)
    QApplication.setQuitOnLastWindowClosed(False)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
