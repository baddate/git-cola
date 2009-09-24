"""This module creates simple wrapper classes around the auto-generated
.ui classes.
"""


import sys
import time

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import qApp
from PyQt4.QtCore import SIGNAL

from cola import core
from cola.views.standard import create_standard_view
from cola.views.syntax import DiffSyntaxHighlighter

try:
    from cola.gui.bookmark import Ui_bookmark
    from cola.gui.branchview import Ui_branchview
    from cola.gui.combo import Ui_combo
    from cola.gui.compare import Ui_compare
    from cola.gui.createbranch import Ui_createbranch
    from cola.gui.items import Ui_items
    from cola.gui.options import Ui_options
    from cola.gui.remote import Ui_remote
    from cola.gui.stash import Ui_stash
except ImportError:
    sys.stderr.write('\nThe cola gui modules have not been built.\n'
                     'Try running "make" in the cola source tree.\n')
    sys.exit(-1)

OptionsView = create_standard_view(Ui_options, QDialog)
BranchCompareView = create_standard_view(Ui_branchview, QDialog)
CreateBranchView = create_standard_view(Ui_createbranch, QDialog)
BookmarkView = create_standard_view(Ui_bookmark, QDialog)
StashView = create_standard_view(Ui_stash, QDialog)
CompareView = create_standard_view(Ui_compare, QDialog)

class ItemView(object):
    def __init__(self, parent, title="", items=[], dblclick=None):
        self.setWindowTitle(title)
        self.items_widget.addItems(items)
        if dblclick and type(self.items_widget) is QListWidget:
            self.connect(self.items_widget,
                         SIGNAL('itemDoubleClicked(QListWidgetItem*)'),
                         dblclick)
    def idx(self):
        return 0
    def selected(self):
        geom = qApp.desktop().screenGeometry()
        width = geom.width()
        height = geom.height()
        x = self.parent().x() + self.parent().width()/2 - self.width()/2
        y = self.parent().y() + self.parent().height()/3 - self.height()/2
        self.move(x, y)
        self.show()
        if self.exec_() == QDialog.Accepted:
            return self.value()
        else:
            return None

ComboViewBase = create_standard_view(Ui_combo, QDialog, ItemView)
class ComboView(ComboViewBase, ItemView):
    """A dialog for choosing branches."""
    def idx(self):
        return self.items_widget.currentIndex()
    def value(self):
        return str(self.items_widget.currentText())

ListViewBase = create_standard_view(Ui_items, QDialog, ItemView)
class ListView(ListViewBase, ItemView):
    """A dialog for an item from a list."""
    def idx(self):
        return self.items_widget.currentRow()
    def value(self):
        item = self.items_widget.currentItem()
        if not item:
            return None
        return str(item.text())


RemoteViewBase = create_standard_view(Ui_remote, QDialog)
class RemoteView(RemoteViewBase):
    """Dialog used by Fetch, Push and Pull"""

    def __init__(self, parent, action):
        """Customizes the dialog based on the remote action
        """
        RemoteViewBase.__init__(self, parent)
        if action:
            self.action_button.setText(action.title())
            self.setWindowTitle(action.title())
        if action == 'pull':
            self.tags_checkbox.hide()
            self.ffwd_only_checkbox.hide()
            self.local_label.hide()
            self.local_branch.hide()
            self.local_branches.hide()
        if action != 'pull':
            self.rebase_checkbox.hide()

    def select_first_remote(self):
        """Selects the first remote in the list view"""
        return self.select_remote(0)

    def select_remote(self, idx):
        """Selects a remote by index"""
        item = self.remotes.item(idx)
        if item:
            self.remotes.setItemSelected(item, True)
            self.remotes.setCurrentItem(item)
            self.remotename.setText(item.text())
            return True
        else:
            return False

    def select_local_branch(self, idx):
        """Selects a local branch by index in the list view"""
        item = self.local_branches.item(idx)
        if not item:
            return False
        self.local_branches.setItemSelected(item, True)
        self.local_branches.setCurrentItem(item)
        self.local_branch.setText(item.text())
        return True
