#!/usr/bin/env python3

"""
BORIS
Behavioral Observation Research Interactive Software
Copyright 2012-2017 Olivier Friard

This file is part of BORIS.

  BORIS is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  any later version.

  BORIS is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not see <http://www.gnu.org/licenses/>.

"""


try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

if QT_VERSION_STR[0] == "4":
    from add_modifier_ui import Ui_Dialog
else:
    from add_modifier_ui5 import Ui_Dialog

import json
import dialog
from config import *

class addModifierDialog(QDialog, Ui_Dialog):

    tabMem = -1
    itemPositionMem = -1

    def __init__(self, modifiers_str, parent=None):

        super(addModifierDialog, self).__init__(parent)
        self.setupUi(self)

        #self.modifierStr = modifiersStr

        self.pbAddModifier.clicked.connect(self.addModifier)
        self.pbAddModifier.setIcon(QIcon(":/frame_forward"))
        self.pbAddSet.clicked.connect(self.addSet)
        self.pbRemoveSet.clicked.connect(self.removeSet)
        self.pbModifyModifier.clicked.connect(self.modifyModifier)
        self.pbModifyModifier.setIcon(QIcon(":/frame_backward"))

        self.pbMoveUp.clicked.connect(self.moveModifierUp)
        self.pbMoveDown.clicked.connect(self.moveModifierDown)

        self.pbMoveSetLeft.clicked.connect(self.moveSetLeft)
        self.pbMoveSetRight.clicked.connect(self.moveSetRight)

        self.pbRemoveModifier.clicked.connect(self.removeModifier)
        self.pbOK.clicked.connect(self.accept)
        self.pbCancel.clicked.connect(self.reject)

        self.tabWidgetModifiersSets.currentChanged.connect(self.tabWidgetModifiersSets_changed)

        self.leSetName.textChanged.connect(self.set_name_changed)

        self.cbType.currentIndexChanged.connect(self.type_changed)

        # store modifiers in list

        self.modifiers_sets_dict = eval(modifiers_str)
        #d = json.loads(modifiers_str)

        # convert keys from str to int (str is due to JSON format)
        # self.modifiers_sets_dict = dict([[int(i), d[i]] for i in d])

        '''
        except:

            self.modifiers_sets_dict = {}

            if modifiers_str:
                for modifiersSet in modifiers_str.split("|"):
                    if "~" in modifiersSet:
                        modif_name, modif_values = modifiersSet.split("~")
                    else:
                        modif_name, modif_values = "", modifiersSet
                    if "," in modif_values:
                        modif_type = SINGLE_SELECTION
                    if "`" in modif_values:
                        modif_type = MULTI_SELECTION

                    self.modifiers_sets_dict[len(self.modifiers_sets_dict)] = {"name": modif_name, "type": modif_type, "values": modif_values.split(",")}
            else:
                self.modifiers_sets_dict[0]= {"name": "", "type": SINGLE_SELECTION, "values": []}
        '''





        print("self.modifiers_sets_dict", self.modifiers_sets_dict)


        # create tab
        for idx in sorted(self.modifiers_sets_dict.keys()):
            if idx:
                self.tabWidgetModifiersSets.addTab(QWidget(), "Set #{}".format(int(idx) + 1))

        # set first tab as active
        self.leSetName.setText(self.modifiers_sets_dict[0]["name"])
        self.cbType.setCurrentIndex(self.modifiers_sets_dict[0]["type"])
        self.lwModifiers.addItems(self.modifiers_sets_dict[0]["values"])
        self.tabMem = 0

    def set_name_changed(self):
        """
        set name changed
        """
        self.modifiers_sets_dict[self.tabWidgetModifiersSets.currentIndex()]["name"] = self.leSetName.text()

    def type_changed(self):
        """
        type changed
        """
        self.modifiers_sets_dict[self.tabWidgetModifiersSets.currentIndex()]["type"] = self.cbType.currentIndex()


    def moveSetLeft(self):
        """
        move selected modifiers set left
        """

        if self.tabWidgetModifiersSets.currentIndex():
            #self.modifiersSets_list[self.tabWidgetModifiersSets.currentIndex() - 1], self.modifiersSets_list[self.tabWidgetModifiersSets.currentIndex()] =  self.modifiersSets_list[ self.tabWidgetModifiersSets.currentIndex() ], self.modifiersSets_list[ self.tabWidgetModifiersSets.currentIndex() - 1]

            self.modifiers_sets_dict[self.tabWidgetModifiersSets.currentIndex() - 1], self.modifiers_sets_dict[self.tabWidgetModifiersSets.currentIndex()] = self.modifiers_sets_dict[self.tabWidgetModifiersSets.currentIndex()], self.modifiers_sets_dict[self.tabWidgetModifiersSets.currentIndex()-1]

            self.tabWidgetModifiersSets.setCurrentIndex(self.tabWidgetModifiersSets.currentIndex() - 1 )
            self.tabMem = self.tabWidgetModifiersSets.currentIndex()

    def moveSetRight(self):
        """
        move selected modifiers set right
        """

        if self.tabWidgetModifiersSets.currentIndex() < self.tabWidgetModifiersSets.count() - 1:
            #self.modifiersSets_list[self.tabWidgetModifiersSets.currentIndex() + 1],  self.modifiersSets_list[ self.tabWidgetModifiersSets.currentIndex() ] =  self.modifiersSets_list[ self.tabWidgetModifiersSets.currentIndex() ], self.modifiersSets_list[ self.tabWidgetModifiersSets.currentIndex() + 1]
            self.modifiers_sets_dict[self.tabWidgetModifiersSets.currentIndex() + 1],  self.modifiers_sets_dict[ self.tabWidgetModifiersSets.currentIndex() ] =  self.modifiers_sets_dict[ self.tabWidgetModifiersSets.currentIndex() ], self.modifiers_sets_dict[ self.tabWidgetModifiersSets.currentIndex() + 1]
            self.tabWidgetModifiersSets.setCurrentIndex(self.tabWidgetModifiersSets.currentIndex() + 1)
            self.tabMem = self.tabWidgetModifiersSets.currentIndex()


    def moveModifierUp(self):
        """
        move up the selected modifier
        """

        if self.lwModifiers.currentRow() >= 0:
            currentRow = self.lwModifiers.currentRow()
            currentItem = self.lwModifiers.takeItem(currentRow)
            self.lwModifiers.insertItem(currentRow - 1, currentItem)
            self.lwModifiers.setCurrentItem(currentItem)
            self.modifiers_sets_dict[self.tabWidgetModifiersSets.currentIndex()] = [self.lwModifiers.item(x).text() for x in range(self.lwModifiers.count())]


    def moveModifierDown(self):
        """
        move down the selected modifier
        """
        if self.lwModifiers.currentRow() >= 0:
            currentRow = self.lwModifiers.currentRow()
            currentItem = self.lwModifiers.takeItem(currentRow)
            self.lwModifiers.insertItem(currentRow + 1, currentItem)
            self.lwModifiers.setCurrentItem(currentItem)
            self.modifiers_sets_dict[self.tabWidgetModifiersSets.currentIndex()] = [self.lwModifiers.item(x).text() for x in range(self.lwModifiers.count())]

    def addSet(self):
        """
        Add a set of modifiers
        """
        if len(self.modifiers_sets_dict[self.tabWidgetModifiersSets.currentIndex()]):
            self.tabWidgetModifiersSets.addTab(QWidget(), "Set #{}".format(len(self.modifiers_sets_dict) + 1))
            self.modifiers_sets_dict[len(self.modifiers_sets_dict)] = {"name": "", "type": SINGLE_SELECTION, "values": []}
            self.tabWidgetModifiersSets.setCurrentIndex(self.tabWidgetModifiersSets.count() - 1)
            self.tabMem = self.tabWidgetModifiersSets.currentIndex()

        else:
            QMessageBox.information(self, programName, "It is not possible to add a modifiers' set while the current modifiers' set is empty.")

    def removeSet(self):
        """
        remove set of modifiers
        """
        if len(self.modifiersSets_list) > 1:
            if dialog.MessageDialog(programName, "Are you sure to remove this set of modifiers?", [YES, NO]) == YES:
                del self.modifiers_sets_dict[self.tabWidgetModifiersSets.currentIndex()]
                self.tabWidgetModifiersSets.removeTab(self.tabWidgetModifiersSets.currentIndex())
        else:
            QMessageBox.information(self, programName, "It is not possible to remove the last modifiers' set.")


    def modifyModifier(self):
        """
        modify modifier <- arrow
        """

        if self.lwModifiers.currentRow() >= 0:
            txt = self.lwModifiers.currentItem().text()
            code = ""
            if "(" in txt and ")" in txt:
                code = txt.split("(")[1].split(")")[0]

            self.leModifier.setText(txt.split("(")[0].strip())
            self.leCode.setText(code)

            self.modifiers_sets_dict[self.tabWidgetModifiersSets.currentIndex()]["values"].remove(self.lwModifiers.currentItem().text())
            self.itemPositionMem = self.lwModifiers.currentRow()
            self.lwModifiers.takeItem(self.lwModifiers.currentRow())
        else:
            QMessageBox.information(self, programName, "Select a modifier to modify from the modifiers set")


    def removeModifier(self):
        """
        remove modifier from set
        """

        if self.lwModifiers.currentIndex().row() >= 0:
            self.lwModifiers.takeItem(self.lwModifiers.currentIndex().row())
            self.modifiers_sets_dict[self.tabWidgetModifiersSets.currentIndex()]["values"] = [self.lwModifiers.item(x).text() for x in range(self.lwModifiers.count())]


    def addModifier(self):
        """
        add a modifier to set
        """

        print("add modifier")

        txt = self.leModifier.text()
        for c in "(|),`~":
            if c in txt:
                QMessageBox.critical(self, programName, "The modifier contains a character that is not allowed.<br>Check the following characters: <b>,(|)`~</b>")
                self.leModifier.setFocus()
                return

        if txt:
            if len(self.leCode.text()) > 1:
                if self.leCode.text().upper() not in ["F" + str(i) for i in range(1, 13)]:
                    QMessageBox.critical(self, programName, "The modifier key code can not exceed one key\nSelect one key of function key (F1, F2 ... F12)")
                    self.leCode.setFocus()
                    return

            if self.leCode.text():
                for c in "(|),`~":
                    if c in self.leCode.text():
                        QMessageBox.critical(self, programName, "The modifier key code is not allowed (|),`~!")
                        self.leCode.setFocus()
                        return

                # check if code already exists
                if "(" + self.leCode.text() + ")" in self.getModifiers():
                    QMessageBox.critical(self, programName, "The code {} already exists!".format(self.leCode.text()))
                    self.leCode.setFocus()
                    return
                txt += " ({})".format(self.leCode.text().upper())

            if self.itemPositionMem != -1:
                self.lwModifiers.insertItem(self.itemPositionMem, txt)
            else:
                self.lwModifiers.addItem(txt)

            self.modifiers_sets_dict[self.tabWidgetModifiersSets.currentIndex()]["values"] = [self.lwModifiers.item(x).text() for x in range(self.lwModifiers.count())]
            self.leModifier.setText("")
            self.leCode.setText("")

        else:
            QMessageBox.critical(self, programName, "No modifier to add!")
            self.leModifier.setFocus()


    def tabWidgetModifiersSets_changed(self, tabIndex):
        """
        user changed the tab widget
        """
        # check if modifier field empty
        if self.leModifier.text() and tabIndex != self.tabMem:
            if dialog.MessageDialog(programName, ("You are working on a behavior.<br>"
                                                  "If you change the modifier's set it will be lost.<br>"
                                                  "Do you want to change modifiers set"), [YES, NO ]) == NO:
                self.tabWidgetModifiersSets.setCurrentIndex(self.tabMem)
                return

        if tabIndex != self.tabMem:
            self.lwModifiers.clear()
            self.leCode.clear()
            self.leModifier.clear()

            self.tabMem = tabIndex

            self.leSetName.setText(self.modifiers_sets_dict[tabIndex]["name"])

            self.cbType.setCurrentIndex(self.modifiers_sets_dict[tabIndex]["type"])

            self.lwModifiers.addItems(self.modifiers_sets_dict[tabIndex]["values"])


    def getModifiers(self):


        txt = ""
        '''
        for idx in sorted(self.modifiers_sets_dict.keys()):
            modifiersSet = self.modifiers_sets_dict[idx]["values"]
            if modifiersSet:
                txt += ",".join(modifiersSet) + "|"
        txt = txt[:-1]
        '''

        '''
        for idx in sorted(self.modifiers_sets_dict.keys()):
            if txt:
                txt += "|"
            txt += self.modifiers_sets_dict[idx]["name"] + "~"
            if self.modifiers_sets_dict[idx]["type"] == SINGLE_SELECTION:
                txt += ",".join(self.modifiers_sets_dict[idx]["values"])
            if self.modifiers_sets_dict[idx]["type"] == MULTI_SELECTION:
                txt += "`".join(self.modifiers_sets_dict[idx]["values"])
        '''
        return str(self.modifiers_sets_dict)
        #return json.dumps(self.modifiers_sets_dict, separators=(',', ':'))
        #return txt
