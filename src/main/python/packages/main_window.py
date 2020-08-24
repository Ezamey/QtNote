from PySide2 import QtWidgets, QtGui

from packages.api.note import Note, get_notes


class MainWindow(QtWidgets.QWidget):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.setWindowTitle("PyNotes")
        self.setup_ui()
        self.populate_notes()

    def setup_ui(self):
        self.create_layouts()
        self.create_widgets()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.btn_create_note = QtWidgets.QPushButton("Créer une note")
        self.lw_note = QtWidgets.QListWidget()
        self.te_contenu = QtWidgets.QTextEdit()
        self.te_research = QtWidgets.QTextEdit()

    def modify_widgets(self):
        css_file = self.ctx.get_resource("style.css")
        with open(css_file, "r")as f:
            self.setStyleSheet(f.read())

        self.te_research.setText(" Rechercher ?")

    def create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout(self)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.btn_create_note, 0, 0, 1, 1)
        self.main_layout.addWidget(self.lw_note, 1, 0, 1, 1)
        self.main_layout.addWidget(self.te_research, 0, 1, 2, 1)
        self.main_layout.addWidget(self.te_contenu, 1, 1)

    def setup_connections(self):
        self.btn_create_note.clicked.connect(self.create_notes)
        self.te_contenu.textChanged.connect(self.save_note)
        self.lw_note.itemSelectionChanged.connect(self.populate_note_content)
        QtWidgets.QShortcut(QtGui.QKeySequence("Backspace"), self.lw_note, self.delete_selected_note)
        #
        # self.te_research.selectAll()
        self.te_research.textChanged.connect(self.research_note)

    # END UI

    def adding_lw_items(self, note):
        lw_item = QtWidgets.QListWidgetItem(note.title)
        lw_item.note = note
        self.lw_note.addItem(lw_item)

    def create_notes(self):
        title, resultat = QtWidgets.QInputDialog.getText(self, "Ajouter une note", "Titre :")
        if resultat and title:
            note = Note(title=title)
            note.save()
            self.adding_lw_items(note)

    def delete_selected_note(self):
        selected_item = self.is_selected_item()
        if selected_item:
            resultat = selected_item.note.delete()
            if resultat:
                self.lw_note.takeItem(self.lw_note.row(selected_item))

    def is_selected_item(self):
        selected_items = self.lw_note.selectedItems()
        if selected_items:
            return selected_items[0]
        return None

    def populate_notes(self):
        notes = get_notes()
        for note in notes:
            self.adding_lw_items(note)

    def populate_note_content(self):
        selected_item = self.is_selected_item()
        if selected_item:
            self.te_contenu.setText(selected_item.note.content)
        else:
            self.te_contenu.clear()

    def save_note(self):
        selected_item = self.is_selected_item()
        if selected_item:
            selected_item.note.content = self.te_contenu.toPlainText()
            selected_item.note.save()

    # OPTIONS

    def research_note(self):
        notes = get_notes()
        contenu = self.te_research.toPlainText()

        for note in notes:
            lw_item = QtWidgets.QListWidgetItem(note.title)
            if contenu in note.title or contenu in note.content:
                print(lw_item.text())




        if contenu=="":
            self.lw_note.setHidden(False)

