# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_modifier.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(638, 510)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbModifier = QtWidgets.QLabel(Dialog)
        self.lbModifier.setObjectName("lbModifier")
        self.verticalLayout_2.addWidget(self.lbModifier)
        self.leModifier = QtWidgets.QLineEdit(Dialog)
        self.leModifier.setObjectName("leModifier")
        self.verticalLayout_2.addWidget(self.leModifier)
        self.lbCode = QtWidgets.QLabel(Dialog)
        self.lbCode.setObjectName("lbCode")
        self.verticalLayout_2.addWidget(self.lbCode)
        self.leCode = QtWidgets.QLineEdit(Dialog)
        self.leCode.setObjectName("leCode")
        self.verticalLayout_2.addWidget(self.leCode)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pbAddModifier = QtWidgets.QPushButton(Dialog)
        self.pbAddModifier.setText("")
        self.pbAddModifier.setObjectName("pbAddModifier")
        self.verticalLayout_3.addWidget(self.pbAddModifier)
        self.pbModifyModifier = QtWidgets.QPushButton(Dialog)
        self.pbModifyModifier.setText("")
        self.pbModifyModifier.setObjectName("pbModifyModifier")
        self.verticalLayout_3.addWidget(self.pbModifyModifier)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidgetModifiersSets = QtWidgets.QTabWidget(Dialog)
        self.tabWidgetModifiersSets.setMaximumSize(QtCore.QSize(16777215, 30))
        self.tabWidgetModifiersSets.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidgetModifiersSets.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidgetModifiersSets.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidgetModifiersSets.setDocumentMode(True)
        self.tabWidgetModifiersSets.setObjectName("tabWidgetModifiersSets")
        self.set1 = QtWidgets.QWidget()
        self.set1.setObjectName("set1")
        self.tabWidgetModifiersSets.addTab(self.set1, "")
        self.verticalLayout.addWidget(self.tabWidgetModifiersSets)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.leSetName = QtWidgets.QLineEdit(Dialog)
        self.leSetName.setObjectName("leSetName")
        self.verticalLayout.addWidget(self.leSetName)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.cbType = QtWidgets.QComboBox(Dialog)
        self.cbType.setObjectName("cbType")
        self.cbType.addItem("")
        self.cbType.addItem("")
        self.verticalLayout.addWidget(self.cbType)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.lwModifiers = QtWidgets.QListWidget(Dialog)
        self.lwModifiers.setObjectName("lwModifiers")
        self.verticalLayout.addWidget(self.lwModifiers)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pbMoveUp = QtWidgets.QPushButton(Dialog)
        self.pbMoveUp.setObjectName("pbMoveUp")
        self.horizontalLayout.addWidget(self.pbMoveUp)
        self.pbMoveDown = QtWidgets.QPushButton(Dialog)
        self.pbMoveDown.setObjectName("pbMoveDown")
        self.horizontalLayout.addWidget(self.pbMoveDown)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pbRemoveModifier = QtWidgets.QPushButton(Dialog)
        self.pbRemoveModifier.setObjectName("pbRemoveModifier")
        self.verticalLayout.addWidget(self.pbRemoveModifier)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pbAddSet = QtWidgets.QPushButton(Dialog)
        self.pbAddSet.setObjectName("pbAddSet")
        self.horizontalLayout_3.addWidget(self.pbAddSet)
        self.pbRemoveSet = QtWidgets.QPushButton(Dialog)
        self.pbRemoveSet.setObjectName("pbRemoveSet")
        self.horizontalLayout_3.addWidget(self.pbRemoveSet)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pbMoveSetLeft = QtWidgets.QPushButton(Dialog)
        self.pbMoveSetLeft.setObjectName("pbMoveSetLeft")
        self.horizontalLayout_4.addWidget(self.pbMoveSetLeft)
        self.pbMoveSetRight = QtWidgets.QPushButton(Dialog)
        self.pbMoveSetRight.setObjectName("pbMoveSetRight")
        self.horizontalLayout_4.addWidget(self.pbMoveSetRight)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.pbCancel = QtWidgets.QPushButton(Dialog)
        self.pbCancel.setObjectName("pbCancel")
        self.horizontalLayout_2.addWidget(self.pbCancel)
        self.pbOK = QtWidgets.QPushButton(Dialog)
        self.pbOK.setObjectName("pbOK")
        self.horizontalLayout_2.addWidget(self.pbOK)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.retranslateUi(Dialog)
        self.tabWidgetModifiersSets.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Set modifiers"))
        self.lbModifier.setText(_translate("Dialog", "Modifier"))
        self.lbCode.setText(_translate("Dialog", "Key code"))
        self.label.setText(_translate("Dialog", "Key code is case insensitive. Type one character or a function key (F1, F2... F12)"))
        self.tabWidgetModifiersSets.setTabText(self.tabWidgetModifiersSets.indexOf(self.set1), _translate("Dialog", "Set #1"))
        self.label_3.setText(_translate("Dialog", "Set name"))
        self.label_4.setText(_translate("Dialog", "Modifier type"))
        self.cbType.setItemText(0, _translate("Dialog", "Single selection"))
        self.cbType.setItemText(1, _translate("Dialog", "Multiple selection"))
        self.label_2.setText(_translate("Dialog", "Values"))
        self.pbMoveUp.setText(_translate("Dialog", "Move modifier up"))
        self.pbMoveDown.setText(_translate("Dialog", "Move modifier down"))
        self.pbRemoveModifier.setText(_translate("Dialog", "Remove modifier"))
        self.pbAddSet.setText(_translate("Dialog", "Add set of modifiers"))
        self.pbRemoveSet.setText(_translate("Dialog", "Remove set of modifiers"))
        self.pbMoveSetLeft.setText(_translate("Dialog", "Move set left"))
        self.pbMoveSetRight.setText(_translate("Dialog", "Move set right"))
        self.pbCancel.setText(_translate("Dialog", "Cancel"))
        self.pbOK.setText(_translate("Dialog", "OK"))

