"""
Dialog box for importing texts.
"""

import codecs

# pylint: disable=no-name-in-module
from aqt.deckchooser import DeckChooser
from aqt.qt import QDesktopServices, QDialog, QUrl, qtmajor
from aqt.utils import getFile, showWarning, askUser, tooltip
from anki.notes import Note

if qtmajor > 5:
    from . import import_dialog6 as lpcg_form
else:
    from . import import_dialog5 as lpcg_form  # type: ignore

# pylint: disable=wrong-import-position
from .gen_notes import add_notes, cleanse_text
from . import models
from .bible_fetcher import get_esv_text
from .bible_data import (
    get_book_names,
    get_chapter_count,
    get_verse_count,
    format_reference,
)


class LPCGDialog(QDialog):
    """
    Import Bible Passage dialog, the core of the add-on. The user can either
    enter the text of a bible passage in the editor or import a text file from somewhere
    else on the computer. The bible passage can be entered with usual markup (blank
    lines between verses, one level of indentation with tabs or spaces in
    front of lines). LPCG then processes it into notes with two lines of
    context and adds them to the user's collection.
    """

    def __init__(self, mw):
        self.mw = mw

        QDialog.__init__(self)
        self.form = lpcg_form.Ui_Dialog()
        self.form.setupUi(self)
        self.deckChooser = DeckChooser(self.mw, self.form.deckChooser)

        self.form.addCardsButton.clicked.connect(self.accept)
        self.form.cancelButton.clicked.connect(self.reject)
        self.form.openFileButton.clicked.connect(self.onOpenFile)
        self.form.helpButton.clicked.connect(self.onHelp)
        self.form.fetchPassageButton.clicked.connect(self.onFetchPassage)

        self.addonConfig = self.mw.addonManager.getConfig(__name__)
        self.form.contextLinesSpin.setValue(self.addonConfig["defaultLinesOfContext"])
        self.form.reciteLinesSpin.setValue(self.addonConfig["defaultLinesToRecite"])
        self.form.groupLinesSpin.setValue(self.addonConfig["defaultLinesInGroupsOf"])

        # Setup Bible selection dropdowns
        self.setupBibleDropdowns()

        # Connect dropdown change events
        self.form.bookCombo.currentTextChanged.connect(self.onBookChanged)
        self.form.chapterCombo.currentTextChanged.connect(self.onChapterChanged)

        # Set default to John 1:1 for testing
        self.setDefaultSelection()

    def setupBibleDropdowns(self):
        """Setup the Bible book, chapter, and verse dropdowns."""
        # Populate book dropdown
        books = get_book_names()
        self.form.bookCombo.addItems(books)

        # Initialize chapter and verse dropdowns as empty
        self.form.chapterCombo.clear()
        self.form.startVerseCombo.clear()
        self.form.endVerseCombo.clear()

        # Add "None" option for end verse (for single verse selections)
        self.form.endVerseCombo.addItem("None")

    def onBookChanged(self):
        """Update chapter dropdown when book selection changes."""
        book = self.form.bookCombo.currentText()
        if not book:
            return

        # Clear and populate chapter dropdown
        self.form.chapterCombo.clear()
        chapter_count = get_chapter_count(book)
        for i in range(1, chapter_count + 1):
            self.form.chapterCombo.addItem(str(i))

    def onChapterChanged(self):
        """Update verse dropdowns when chapter selection changes."""
        book = self.form.bookCombo.currentText()
        chapter_text = self.form.chapterCombo.currentText()

        if not book or not chapter_text:
            return

        try:
            chapter = int(chapter_text)
            verse_count = get_verse_count(book, chapter)

            # Clear and populate verse dropdowns
            self.form.startVerseCombo.clear()
            self.form.endVerseCombo.clear()
            self.form.endVerseCombo.addItem("None")

            for i in range(1, verse_count + 1):
                self.form.startVerseCombo.addItem(str(i))
                self.form.endVerseCombo.addItem(str(i))

        except ValueError:
            # Handle invalid chapter number
            pass

    def setDefaultSelection(self):
        """Set default selection to John 1:1."""
        # Set book to John
        john_index = self.form.bookCombo.findText("John")
        if john_index >= 0:
            self.form.bookCombo.setCurrentIndex(john_index)
            # This will trigger onBookChanged, which populates chapters

            # Set chapter to 1
            chapter_index = self.form.chapterCombo.findText("1")
            if chapter_index >= 0:
                self.form.chapterCombo.setCurrentIndex(chapter_index)
                # This will trigger onChapterChanged, which populates verses

                # Set verse to 1
                verse_index = self.form.startVerseCombo.findText("1")
                if verse_index >= 0:
                    self.form.startVerseCombo.setCurrentIndex(verse_index)

    def onFetchPassage(self):
        """Fetch the selected Bible passage and populate the text editor."""
        book = self.form.bookCombo.currentText()
        chapter_text = self.form.chapterCombo.currentText()
        start_verse_text = self.form.startVerseCombo.currentText()
        end_verse_text = self.form.endVerseCombo.currentText()

        if not book or not chapter_text or not start_verse_text:
            showWarning("Please select a book, chapter, and starting verse.")
            return

        try:
            chapter = int(chapter_text)
            start_verse = int(start_verse_text)
            end_verse = None

            if end_verse_text and end_verse_text != "None":
                end_verse = int(end_verse_text)

            # Format the Bible reference
            reference = format_reference(book, chapter, start_verse, end_verse)

            # Fetch the passage
            passage_text = get_esv_text(reference)

            # Update the form fields
            self.form.titleBox.setText(reference)
            self.form.textBox.setPlainText(passage_text)
            self.form.authorBox.setText(book.split()[0])  # Use book name as author
            self.form.tagsBox.setText("bible " + book.lower().replace(" ", ""))

        except ValueError as e:
            showWarning(f"Invalid verse selection: {e}")
        except Exception as e:
            showWarning(f"Error fetching passage: {e}")

    def accept(self):
        "On close, create notes from the contents of the bible passage editor."
        title = self.form.titleBox.text().strip()

        if not title:
            showWarning("You must enter a title for this bible passage.")
            return
        escaped_title = title.replace('"', '\\"')
        if self.mw.col.find_notes(
            f'"note:{models.LpcgOne.name}" '  # pylint: disable=no-member
            f'"Title:{escaped_title}"'
        ):
            showWarning(
                "You already have a bible passage by that title in your "
                "database. Please check to see if you've already "
                "added it, or use a different name."
            )
            return
        if not self.form.textBox.toPlainText().strip():
            showWarning(
                "There's nothing to generate cards from! "
                "Please type a bible passage in the box, or use the "
                '"Open File" button to import a text file.'
            )
            return

        author = self.form.authorBox.text().strip()
        tags = self.mw.col.tags.split(self.form.tagsBox.text())
        text = cleanse_text(self.form.textBox.toPlainText().strip(), self.addonConfig)
        context_lines = self.form.contextLinesSpin.value()
        recite_lines = self.form.reciteLinesSpin.value()
        group_lines = self.form.groupLinesSpin.value()
        did = self.deckChooser.selectedId()

        try:
            notes_generated = add_notes(
                self.mw.col,
                Note,
                title,
                author,
                tags,
                text,
                did,
                context_lines,
                group_lines,
                recite_lines,
            )
        except KeyError as e:
            showWarning(
                "The field {field} was not found on the {name} note type"
                " in your collection. If you don't have any LPCG notes"
                " yet, you can delete the note type in Tools -> Manage"
                " Note Types and restart Anki to fix this problem."
                " Otherwise, please add the field back to the note type. ".format(
                    field=str(e), name=models.LpcgOne.name
                )
            )  # pylint: disable=no-member
            return

        if notes_generated:
            super(LPCGDialog, self).accept()
            self.deckChooser.cleanup()
            self.mw.reset()
            tooltip("%i notes added." % notes_generated)

    def onOpenFile(self):
        """
        Read a text file (in UTF-8 encoding) and replace the contents of the
        bible passage editor with the contents of the file.
        """
        if self.form.textBox.toPlainText().strip() and not askUser(
            "Importing a file will replace the current "
            "contents of the bible passage editor. Continue?"
        ):
            return
        filename = getFile(self, "Import file", None, key="import")
        if not filename:  # canceled
            return
        with codecs.open(filename, "r", "utf-8") as f:
            text = f.read()
        self.form.textBox.setPlainText(text)

    def onHelp(self):
        """
        Open the documentation on importing files in a browser.
        """
        doc_url = "https://ankilpcg.readthedocs.io/en/latest/importing.html"
        QDesktopServices.openUrl(QUrl(doc_url))
