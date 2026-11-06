import sys
import os
import json
import random
import winreg
from PyQt6.QtWidgets import (
    QApplication, QWidget, QSystemTrayIcon, QMenu, QDialog,
    QVBoxLayout, QLabel, QPushButton, QScrollArea, QStyle
)
from PyQt6.QtGui import QIcon, QPixmap, QAction, QActionGroup
from PyQt6.QtCore import Qt, QTimer, QUrl, QEvent
from PyQt6.QtGui import QDesktopServices

APP_NAME = "Bug Dance"
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
CONFIG_FILE = "bug_dance_config.json"

class BugWidget(QWidget):
    """Floating transparent widget representing an animated bug."""
    def __init__(self, image_path, speed_factor=1.0, always_on_top=True, parent=None):
        super().__init__(parent)
        self.always_on_top = always_on_top
        self.set_window_flags_mode()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self.original_pixmap = QPixmap(image_path)
        self.speed_factor = speed_factor

        self.label = QLabel(self)
        self.update_size()

        screen = QApplication.primaryScreen().geometry()
        self.x_pos = random.randint(100, max(200, screen.width() - 200))
        self.y_pos = random.randint(100, max(200, screen.height() - 200))
        self.move(int(self.x_pos), int(self.y_pos))

        self.dx = random.choice([-1, 1]) * random.uniform(1.5, 3.5)
        self.dy = random.choice([-1, 1]) * random.uniform(1.5, 3.5)

    def set_window_flags_mode(self):
        flags = (
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput
        )
        if self.always_on_top:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)

    def set_always_on_top(self, enable):
        self.always_on_top = enable
        self.set_window_flags_mode()
        self.show()

    def update_size(self):
        if self.original_pixmap.isNull():
            return
        base_width = 80
        scaled = self.original_pixmap.scaledToWidth(
            base_width, Qt.TransformationMode.SmoothTransformation
        )
        self.label.setPixmap(scaled)
        self.resize(scaled.size())

    def set_speed_factor(self, factor):
        self.speed_factor = factor

    def step(self):
        screen = QApplication.primaryScreen().geometry()
        self.x_pos += self.dx * self.speed_factor
        self.y_pos += self.dy * self.speed_factor

        if self.x_pos <= 0 or self.x_pos + self.width() >= screen.width():
            self.dx *= -1
            self.x_pos = max(0, min(self.x_pos, screen.width() - self.width()))

        if self.y_pos <= 0 or self.y_pos + self.height() >= screen.height():
            self.dy *= -1
            self.y_pos = max(0, min(self.y_pos, screen.height() - self.height()))

        self.move(int(self.x_pos), int(self.y_pos))


class CatalogWindow(QDialog):
    """Sub-window displaying the Catalog of Bugs (1000px wide)."""
    def __init__(self, catalog_image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Catalog of Bugs")
        self.setFixedWidth(1000)
        self.setFixedHeight(700)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        container = QWidget()
        scroll_layout = QVBoxLayout(container)

        img_label = QLabel(container)
        if os.path.exists(catalog_image_path):
            pixmap = QPixmap(catalog_image_path)
            if not pixmap.isNull():
                img_label.setPixmap(pixmap.scaledToWidth(950, Qt.TransformationMode.SmoothTransformation))
            else:
                img_label.setText("Catalog of Bugs image could not be loaded.")
        else:
            img_label.setText("Catalog of Bugs image (Catalog_of_Bugs.png) not found.")

        img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(img_label)
        scroll.setWidget(container)

        close_btn = QPushButton("CLOSE", self)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)


class CustomMenu(QMenu):
    """Custom QMenu that keeps the menu open when clicking checkable Bug items."""
    def mouseReleaseEvent(self, event):
        action = self.actionAt(event.pos())
        if action and action.isCheckable():
            action.trigger()
            # Do not close menu on checkable action click
            return
        super().mouseReleaseEvent(event)


class AboutDialog(QDialog):
    """About Dialog with updated legal notice and HERE link opening Catalog Window."""
    def __init__(self, base_dir, parent=None):
        super().__init__(parent)
        self.base_dir = base_dir
        self.setWindowTitle("About Bug Dance")
        self.setFixedSize(480, 480)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        about_text = (
            "##############################################<br>"
            "<b>#JXD VibeLabs#</b><br>"
            "<b>#Stoned penguin is watching you!#</b><br>"
            "Tux © Larry Ewing<br>"
            "Photo © Jaroslav M. Soukup<br>"
            "Software © Jiri X. Dolezal<br>"
            "Questions <a href='mailto:jxd@jxd.cz'>jxd@jxd.cz</a><br>"
            "<a href='https://jxd.cz/'>https://jxd.cz/</a><br>"
            "To select Bugs, open their catalog <a href='app://catalog'>HERE</a><br>"
            "<b>#VIBE coding is poetry.#</b><br>"
            "<b>#Fear the penguin!#</b><br>"
            "##############################################<br>"
            "The invertebrates are real; the photographs<br>"
            "were taken between 2022 and 2029 in<br>"
            "the Czech Republic. No creatures, beetles,<br>"
            "or spiders were harmed during the photography<br>"
            "or the development of this software.<br>"
            "##############################################"
        )

        label = QLabel(about_text, self)
        label.setOpenExternalLinks(False)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.linkActivated.connect(self.handle_link)
        layout.addWidget(label)

        close_btn = QPushButton("CLOSE", self)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def handle_link(self, url_str):
        if url_str == "app://catalog":
            catalog_img_path = os.path.join(self.base_dir, "Catalog_of_Bugs.png")
            dlg = CatalogWindow(catalog_img_path, self)
            dlg.exec()
        else:
            QDesktopServices.openUrl(QUrl(url_str))


class BugDanceApp:
    def __init__(self, app_instance):
        self.app = app_instance
        self.base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        self.is_paused = False
        self.current_speed = 1.0
        self.always_on_top = True
        self.active_bugs = {}
        self.selected_bug_indices = set(range(1, 25))

        self.bug_images = {
            i: os.path.join(self.base_dir, f"Jaroslav.M.Soukup_bugs_{i}.png")
            for i in range(1, 25)
        }

        self.load_config()

        self.tray_icon = QSystemTrayIcon()
        icon_path = os.path.join(self.base_dir, "Bug_Dance.ico")
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            self.tray_icon.setIcon(self.app.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))

        self.tray_icon.setToolTip("Bug Dance")
        self.build_menu()
        self.tray_icon.show()

        for i in range(1, 25):
            if i in self.selected_bug_indices:
                self.toggle_bug(i, True)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_bugs)
        self.timer.start(16)

    def load_config(self):
        config_path = os.path.join(self.base_dir, CONFIG_FILE)
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.current_speed = data.get("speed", 1.0)
                    self.always_on_top = data.get("always_on_top", True)
                    selected = data.get("selected_bugs", list(range(1, 25)))
                    self.selected_bug_indices = set(selected)
            except Exception as e:
                print(f"Error loading config: {e}")

    def save_config(self):
        config_path = os.path.join(self.base_dir, CONFIG_FILE)
        try:
            data = {
                "speed": self.current_speed,
                "always_on_top": self.always_on_top,
                "selected_bugs": sorted(list(self.selected_bug_indices))
            }
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def build_menu(self):
        self.menu = QMenu()

        self.pause_action = QAction("Pause", self.menu)
        self.pause_action.triggered.connect(self.toggle_pause)
        self.menu.addAction(self.pause_action)
        self.menu.addSeparator()

        speed_menu = self.menu.addMenu("Speed")
        speed_group = QActionGroup(self.menu)
        speed_options = [
            ("Very Slow", 0.3), ("Slow", 0.6), ("Normal", 1.0),
            ("Fast", 1.8), ("Very Fast", 3.0)
        ]
        for label, factor in speed_options:
            act = QAction(label, speed_menu, checkable=True)
            if abs(factor - self.current_speed) < 0.05:
                act.setChecked(True)
            act.triggered.connect(lambda checked, f=factor: self.set_speed(f))
            speed_group.addAction(act)
            speed_menu.addAction(act)

        self.aot_action = QAction("Always on top", self.menu, checkable=True)
        self.aot_action.setChecked(self.always_on_top)
        self.aot_action.triggered.connect(self.toggle_always_on_top)
        self.menu.addAction(self.aot_action)

        # Custom Bugs Submenu (uses CustomMenu so clicking checkboxes keeps it open)
        bugs_menu = CustomMenu("Bugs", self.menu)
        self.menu.addMenu(bugs_menu)

        for i in range(1, 25):
            act = QAction(f"Bug #{i}", bugs_menu, checkable=True)
            act.setChecked(i in self.selected_bug_indices)
            act.triggered.connect(lambda checked, idx=i: self.toggle_bug(idx, checked))
            bugs_menu.addAction(act)

        self.menu.addSeparator()

        about_action = QAction("About", self.menu)
        about_action.triggered.connect(lambda: AboutDialog(self.base_dir).exec())
        self.menu.addAction(about_action)

        self.startup_action = QAction("Run at Windows start-up", self.menu, checkable=True)
        self.startup_action.setChecked(self.is_startup_enabled())
        self.startup_action.triggered.connect(self.toggle_startup)
        self.menu.addAction(self.startup_action)

        self.menu.addSeparator()

        exit_action = QAction("Exit", self.menu)
        exit_action.triggered.connect(self.exit_app)
        self.menu.addAction(exit_action)

        self.tray_icon.setContextMenu(self.menu)

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_action.setText("Play" if self.is_paused else "Pause")

    def set_speed(self, factor):
        self.current_speed = factor
        for bug in self.active_bugs.values():
            bug.set_speed_factor(factor)

    def toggle_always_on_top(self, enable):
        self.always_on_top = enable
        for bug in self.active_bugs.values():
            bug.set_always_on_top(enable)

    def toggle_bug(self, index, enable):
        if enable:
            self.selected_bug_indices.add(index)
            if index not in self.active_bugs:
                img_path = self.bug_images[index]
                if os.path.exists(img_path):
                    bug = BugWidget(img_path, self.current_speed, self.always_on_top)
                    bug.show()
                    self.active_bugs[index] = bug
        else:
            self.selected_bug_indices.discard(index)
            if index in self.active_bugs:
                bug = self.active_bugs.pop(index)
                bug.close()
                bug.deleteLater()

    def update_bugs(self):
        if not self.is_paused:
            for bug in self.active_bugs.values():
                bug.step()

    def is_startup_enabled(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
            winreg.QueryValueEx(key, APP_NAME)
            winreg.CloseKey(key)
            return True
        except Exception:
            return False

    def toggle_startup(self, enable):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE)
            if enable:
                exe_path = f'"{sys.executable}"' if getattr(sys, 'frozen', False) else f'"{sys.executable}" "{os.path.abspath(sys.argv[0])}"'
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
            else:
                try: winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError: pass
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Startup reg error: {e}")

    def exit_app(self):
        self.save_config()
        self.timer.stop()
        for bug in list(self.active_bugs.values()):
            bug.close()
        self.app.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    bug_dance = BugDanceApp(app)
    sys.exit(app.exec())
