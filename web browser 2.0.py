
import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QAction,
    QLineEdit,
    QProgressBar,
    QShortcut
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineView


# =========================================================
# CUSTOM EPIC BROWSER HOMEPAGE
# =========================================================

HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Segoe UI, Arial;
    color: white;
    min-height: 100vh;

    background:
        radial-gradient(circle at 20% 20%, #28205e, transparent 45%),
        radial-gradient(circle at 80% 80%, #39134f, transparent 45%),
        #10111b;

    display: flex;
    justify-content: center;
    align-items: center;
}

.container {
    width: 850px;
    max-width: 90%;
    text-align: center;
}

.logo {
    font-size: 65px;
    font-weight: bold;
    letter-spacing: 2px;
    margin-bottom: 10px;
}

.logo span {
    color: #a855f7;
}

.subtitle {
    color: #aaa;
    font-size: 18px;
    margin-bottom: 45px;
}

.search {
    display: flex;
    background: #222333;
    border: 2px solid #7c3aed;
    border-radius: 35px;
    padding: 8px;
    box-shadow: 0 0 25px #7c3aed55;
}

.search input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: white;
    font-size: 17px;
    padding: 15px;
}

.search input::placeholder {
    color: #aaa;
}

.search button {
    background: #7c3aed;
    color: white;
    border: none;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    font-size: 22px;
    cursor: pointer;
}

.search button:hover {
    background: #9333ea;
}

h3 {
    margin-top: 45px;
    color: #aaa;
    font-weight: normal;
}

.shortcuts {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 15px;
    margin-top: 20px;
}

.shortcut {
    width: 105px;
    padding: 20px 10px;
    border-radius: 15px;
    background: #25263a;
    text-decoration: none;
    color: white;
    transition: 0.2s;
}

.shortcut:hover {
    background: #3b2b60;
    transform: translateY(-5px);
}

.icon {
    font-size: 30px;
    margin-bottom: 12px;
}

footer {
    margin-top: 60px;
    color: #777;
    font-size: 13px;
}

</style>
</head>

<body>

<div class="container">

    <div class="logo">
        Epic <span>Browser</span>
    </div>

    <div class="subtitle">
        Browse Smarter. Explore More.
    </div>

    <form class="search" onsubmit="searchGoogle(); return false;">

        <input id="searchBox"
               placeholder="Search Google or enter website URL..."
               autocomplete="off">

        <button type="submit">➜</button>

    </form>

    <h3>Quick Access</h3>

    <div class="shortcuts">

        <a class="shortcut" href="https://youtube.com">
            <div class="icon">▶️</div>
            YouTube
        </a>

        <a class="shortcut" href="https://drive.google.com">
            <div class="icon">📁</div>
            Drive
        </a>

        <a class="shortcut" href="https://gmail.com">
            <div class="icon">✉️</div>
            Gmail
        </a>

        <a class="shortcut" href="https://chatgpt.com">
            <div class="icon">🤖</div>
            ChatGPT
        </a>

        <a class="shortcut" href="https://wikipedia.org">
            <div class="icon">📚</div>
            Wikipedia
        </a>

        <a class="shortcut" href="https://microsoft.com">
            <div class="icon">🪟</div>
            Microsoft
        </a>

    </div>

    <footer>
        Dream Big. Browse Better. — Epic Browser
    </footer>

</div>

<script>

function searchGoogle() {

    let text = document.getElementById("searchBox").value.trim();

    if (!text) return;

    if (/^[a-zA-Z0-9-]+\\.[a-zA-Z]{2,}/.test(text)) {

        if (!text.startsWith("http")) {
            text = "https://" + text;
        }

        window.location.href = text;

    } else {

        window.location.href =
            "https://www.google.com/search?q=" +
            encodeURIComponent(text);

    }

}

</script>

</body>
</html>
"""


# =========================================================
# MAIN BROWSER WINDOW
# =========================================================

class MainScreen(QMainWindow):

    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("Epic Browser")
        self.resize(1300, 800)

        # Browser
        self.Browser = QWebEngineView()
        self.setCentralWidget(self.Browser)

        # Toolbar
        NavBar = QToolBar("Navigation")
        NavBar.setMovable(False)
        NavBar.setFloatable(False)
        self.addToolBar(NavBar)

        # Back button
        BackButton = QAction("◀", self)
        BackButton.setToolTip("Back")
        BackButton.triggered.connect(self.Browser.back)
        NavBar.addAction(BackButton)

        # Forward button
        ForwardButton = QAction("▶", self)
        ForwardButton.setToolTip("Forward")
        ForwardButton.triggered.connect(self.Browser.forward)
        NavBar.addAction(ForwardButton)

        # Reload button
        ReloadButton = QAction("⟳", self)
        ReloadButton.setToolTip("Reload")
        ReloadButton.triggered.connect(self.Browser.reload)
        NavBar.addAction(ReloadButton)

        # Home button
        HomeButton = QAction("⌂", self)
        HomeButton.setToolTip("Home")
        HomeButton.triggered.connect(self.NavigateHome)
        NavBar.addAction(HomeButton)

        # URL bar
        self.UrlBar = QLineEdit()
        self.UrlBar.setPlaceholderText(
            "Search Google or enter website URL..."
        )
        self.UrlBar.returnPressed.connect(self.NavigateToUrl)
        NavBar.addWidget(self.UrlBar)

        # Go button
        GoButton = QAction("Go", self)
        GoButton.triggered.connect(self.NavigateToUrl)
        NavBar.addAction(GoButton)

        # Browser events
        self.Browser.urlChanged.connect(self.UpdateUrl)
        self.Browser.titleChanged.connect(self.UpdateTitle)
        self.Browser.loadProgress.connect(self.UpdateProgress)

        # Progress bar
        self.ProgressBar = QProgressBar()
        self.ProgressBar.setMaximumWidth(150)
        self.ProgressBar.setMaximumHeight(15)
        self.ProgressBar.setTextVisible(False)

        self.statusBar().addPermanentWidget(self.ProgressBar)
        self.ProgressBar.hide()

        # Dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }

            QToolBar {
                background-color: #202124;
                border: none;
                spacing: 8px;
                padding: 10px;
            }

            QToolButton {
                background-color: #303134;
                color: white;
                border-radius: 8px;
                padding: 8px;
                min-width: 25px;
                font-size: 16px;
            }

            QToolButton:hover {
                background-color: #45464a;
            }

            QLineEdit {
                background-color: #303134;
                color: white;
                border: 2px solid #303134;
                border-radius: 18px;
                padding: 10px 15px;
                font-size: 14px;
                min-width: 300px;
            }

            QLineEdit:focus {
                border: 2px solid #8ab4f8;
                background-color: #202124;
            }

            QStatusBar {
                background-color: #202124;
                color: white;
            }

            QProgressBar {
                background-color: #303134;
                border: none;
                border-radius: 5px;
            }

            QProgressBar::chunk {
                background-color: #8ab4f8;
                border-radius: 5px;
            }
        """)

        # Keyboard shortcuts
        self.addShortcut("Ctrl+L", self.FocusUrlBar)
        self.addShortcut("Ctrl+R", self.Browser.reload)
        self.addShortcut("Alt+Left", self.Browser.back)
        self.addShortcut("Alt+Right", self.Browser.forward)

        # Open custom homepage
        self.NavigateHome()

        # Show browser
        self.showMaximized()

    # =====================================================
    # HOMEPAGE
    # =====================================================

    def NavigateHome(self):
        self.Browser.setHtml(HOME_HTML, QUrl("https://epic-browser.local/"))
        self.UrlBar.setText("Epic Browser - Home")
        self.setWindowTitle("Epic Browser - Home")

    # =====================================================
    # NAVIGATE TO URL
    # =====================================================

    def NavigateToUrl(self):

        text = self.UrlBar.text().strip()

        if not text:
            return

        # Website address
        if "." in text and " " not in text:

            if not text.startswith(("http://", "https://")):
                text = "https://" + text

            self.Browser.setUrl(QUrl(text))

        else:

            # Google search
            search_url = (
                "https://www.google.com/search?q="
                + text.replace(" ", "+")
            )

            self.Browser.setUrl(QUrl(search_url))

    # =====================================================
    # UPDATE URL BAR
    # =====================================================

    def UpdateUrl(self, url):

        address = url.toString()

        if address and address != "about:blank":
            self.UrlBar.setText(address)

    # =====================================================
    # UPDATE WINDOW TITLE
    # =====================================================

    def UpdateTitle(self, title):

        if title:
            self.setWindowTitle(title + " - Epic Browser")

    # =====================================================
    # LOADING PROGRESS
    # =====================================================

    def UpdateProgress(self, progress):

        self.ProgressBar.show()
        self.ProgressBar.setValue(progress)

        if progress == 100:
            self.ProgressBar.hide()

    # =====================================================
    # FOCUS URL BAR
    # =====================================================

    def FocusUrlBar(self):

        self.UrlBar.setFocus()
        self.UrlBar.selectAll()

    # =====================================================
    # KEYBOARD SHORTCUTS
    # =====================================================

    def addShortcut(self, key, function):

        shortcut = QShortcut(QKeySequence(key), self)
        shortcut.activated.connect(function)


# =========================================================
# APPLICATION
# =========================================================

Application = QApplication(sys.argv)

Application.setApplicationName("Epic Browser")
Application.setStyle("Fusion")

Window = MainScreen()

sys.exit(Application.exec_())
