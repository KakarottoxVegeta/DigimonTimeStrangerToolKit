#!/usr/bin/env python3
"""
DTS Toolkit Launcher
Unified launcher for all Digimon Time Stranger ToolKit utilities.
Provides a single entry point to manage and launch the complete modding suite.

Guidelines: [WF-001], [WF-003], [WF-010], [EH-001], [EH-002], [PG-001]
"""

import sys
import os
import subprocess
import threading
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QGridLayout, QMessageBox, QSizePolicy,
    QGroupBox, QTextEdit, QProgressBar
)
from PyQt6.QtCore import Qt, QProcess, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QIcon


class ToolRunner(QObject):
    """Manages external process execution with status feedback."""
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self):
        super().__init__()
        self.process = None

    def run(self, command, args=None, cwd=None):
        if args is None:
            args = []
        self.output_signal.emit(f"Launching: {command} {' '.join(args)}\n")
        self.process = QProcess(self)
        self.process.setProgram(command)
        self.process.setArguments(args)
        if cwd:
            self.process.setWorkingDirectory(cwd)
        self.process.readyReadStandardOutput.connect(self._read_stdout)
        self.process.readyReadStandardError.connect(self._read_stderr)
        self.process.finished.connect(lambda code, status: self._finished(code, status, command))
        self.process.start()

    def _read_stdout(self):
        data = self.process.readAllStandardOutput()
        text = bytes(data).decode("utf-8", errors="replace").strip()
        if text:
            self.output_signal.emit(text + "\n")

    def _read_stderr(self):
        data = self.process.readAllStandardError()
        text = bytes(data).decode("utf-8", errors="replace").strip()
        if text:
            self.output_signal.emit(f"[stderr] {text}\n")

    def _finished(self, exit_code, exit_status, command):
        status = "Success" if exit_code == 0 else f"Failed (code {exit_code})"
        self.finished_signal.emit(exit_code == 0, f"{command} -> {status}")
        self.process.deleteLater()
        self.process = None

    def terminate(self):
        if self.process and self.process.state() == QProcess.ProcessState.Running:
            self.process.kill()
            self.process.waitForFinished(3000)


class ToolCard(QFrame):
    """A card widget representing a tool in the launcher dashboard."""

    def __init__(self, name, description, command, args, cwd, launcher):
        super().__init__()
        self.tool_name = name
        self.command = command
        self.args = args
        self.cwd = cwd
        self.launcher = launcher
        self.runner = ToolRunner()
        self.runner.output_signal.connect(self.launcher.log_output)
        self.runner.finished_signal.connect(self.launcher.tool_finished)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            ToolCard {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
            }
            ToolCard:hover {
                border: 1px solid #80bdff;
                background-color: #e9ecef;
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
            QPushButton:pressed {
                background-color: #0a58ca;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
            QLabel { color: #212529; }
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(6)
        layout.setContentsMargins(12, 12, 12, 12)

        # Title
        title = QLabel(self.tool_name)
        title_font = QFont("Segoe UI", 11, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setWordWrap(True)
        layout.addWidget(title)

        # Description
        self.description = self._get_description()
        desc = QLabel(self.description)
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #495057; font-size: 10pt;")
        layout.addWidget(desc)

        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #198754; font-size: 9pt;")
        layout.addWidget(self.status_label)

        # Launch button
        self.launch_btn = QPushButton("▶ Launch")
        self.launch_btn.clicked.connect(self.launch)
        layout.addWidget(self.launch_btn)

        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMaximumHeight(200)

    def _get_description(self):
        descriptions = {
            "Digimon Editor": "Full Digimon editor: stats, skills, traits, evolutions, model, battle data. Supports Base/DLC/dsts-loader.",
            "MBE Editor": "Direct binary MBE file editor. Open/save .mbe directories or CSV, multi-sheet tabbed view with search.",
            "Lua Decompiler": "Batch decompile .lua files via unluac.jar. Progress tracking and timeout safety.",
            "MVGL Tools": "Frontend for MVGLToolsCLI.exe. Pack/unpack MVGL/MBE/AFS2 archives and encrypt/decrypt game files.",
        }
        return descriptions.get(self.tool_name, "Tool utility.")

    def launch(self):
        if self.runner.process is not None and self.runner.process.state() == QProcess.ProcessState.Running:
            self.runner.terminate()
            self.launch_btn.setText("▶ Launch")
            self.status_label.setText("Terminated")
            self.status_label.setStyleSheet("color: #dc3545; font-size: 9pt;")
            return

        # Resolve paths relative to toolkit root
        base_dir = Path(__file__).parent.resolve()
        exe_path = base_dir / self.command
        if self.command.endswith(".py") and not exe_path.exists():
            alt = base_dir / (self.command.replace(".py", ".exe"))
            if alt.exists():
                exe_path = alt
                cmd = str(exe_path)
                args = []
            else:
                cmd = sys.executable
                args = [str(exe_path)]
        else:
            cmd = str(exe_path)
            args = list(self.args)

        if not Path(cmd).exists():
            self.launcher.log_output(f"[ERROR] Executable not found: {cmd}\n")
            self.status_label.setText("Missing: " + self.command)
            self.status_label.setStyleSheet("color: #dc3545; font-size: 9pt;")
            return

        self.launch_btn.setText("⏹ Stop")
        self.status_label.setText("Running...")
        self.status_label.setStyleSheet("color: #0d6efd; font-size: 9pt;")
        self.runner.run(cmd, args, cwd=str(self.cwd) if self.cwd else str(base_dir))

    def on_tool_finished(self, success, message):
        self.launch_btn.setText("▶ Launch")
        if success:
            self.status_label.setText("Finished")
            self.status_label.setStyleSheet("color: #198754; font-size: 9pt;")
        else:
            self.status_label.setText("Error")
            self.status_label.setStyleSheet("color: #dc3545; font-size: 9pt;")


class DTSToolkitLauncher(QMainWindow):
    """Unified launcher dashboard for DTS Toolkit."""

    def __init__(self):
        super().__init__()
        self.runner = ToolRunner()
        self.runner.output_signal.connect(self.log_output)
        self.runner.finished_signal.connect(self.log_finished)
        self.tool_cards = []
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("DTS Toolkit Launcher")
        self.setMinimumSize(900, 640)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QLabel {
                color: #212529;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 10pt;
                border: 1px solid #ced4da;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #0d6efd;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: Consolas, Monaco, monospace;
                font-size: 9pt;
                border-radius: 4px;
            }
        """)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        header = QLabel("DIGIMON TIME STRANGER TOOLKIT")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("font-size: 18pt; font-weight: bold; color: #0d6efd; letter-spacing: 1px;")
        main_layout.addWidget(header)

        subtitle = QLabel("Unified Launcher — Manage and launch all modding utilities")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 9pt; color: #6c757d;")
        main_layout.addWidget(subtitle)

        # Tools grid
        tools_group = QGroupBox("Applications")
        grid = QGridLayout()
        grid.setSpacing(16)

        base_dir = Path(__file__).parent.resolve()
        tools = [
            ("Digimon Editor", self._resolve("digimon_editor.py"), ["digimon_editor.py"]),
            ("MBE Editor", self._resolve("MBE_Editor.py"), ["MBE_Editor.py"]),
            ("Lua Decompiler", self._resolve("lua_decompiler_gui.py"), ["lua_decompiler_gui.py"]),
            ("MVGL Tools", self._resolve("mvgl_tools_gui.py"), ["mvgl_tools_gui.py"]),
        ]
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for (r, c), (name, cmd, args) in zip(positions, tools):
            card = ToolCard(name, "", cmd, args, base_dir, self)
            self.tool_cards.append(card)
            grid.addWidget(card, r, c)

        tools_group.setLayout(grid)
        main_layout.addWidget(tools_group)

        # Batch launchers
        batch_group = QGroupBox("Launchers")
        batch_layout = QHBoxLayout()
        batch_layout.setSpacing(10)

        batches = [
            ("Lua_Decompiler.bat", "Decompile Lua Scripts"),
            ("Launch_MVGL_GUI.bat", "Launch MVGL GUI"),
        ]
        for bat, label in batches:
            btn = QPushButton(label)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #6f42c1;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #5a32a3;
                }
            """)
            btn.clicked.connect(lambda checked, b=bat: self.launch_batch(b))
            batch_layout.addWidget(btn)

        batch_group.setLayout(batch_layout)
        main_layout.addWidget(batch_group)

        # Log panel
        log_group = QGroupBox("Activity Log")
        log_layout = QVBoxLayout()
        log_layout.setContentsMargins(8, 12, 8, 8)

        # Clear log button
        clear_row = QHBoxLayout()
        clear_btn = QPushButton("Clear Log")
        clear_btn.setMaximumWidth(100)
        clear_btn.setStyleSheet("background-color: #6c757d; padding: 4px 8px; font-size: 9pt;")
        clear_btn.clicked.connect(lambda: self.log.clear())
        clear_row.addWidget(clear_btn)
        clear_row.addStretch()
        log_layout.addLayout(clear_row)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("Tool output and status messages will appear here...")
        log_layout.addWidget(self.log)

        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group, stretch=1)

        # Footer
        footer = QLabel("DTS Toolkit Launcher v1.0 | All tools execute from the toolkit root")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("font-size: 8pt; color: #adb5bd;")
        main_layout.addWidget(footer)

    def _resolve(self, filename):
        base_dir = Path(__file__).parent.resolve()
        path = base_dir / filename
        if path.exists():
            return str(path)
        # Try .exe fallback
        alt = base_dir / filename.replace(".py", ".exe")
        if alt.exists():
            return str(alt)
        return str(path)

    def launch_batch(self, bat):
        base_dir = Path(__file__).parent.resolve()
        bat_path = base_dir / bat
        if not bat_path.exists():
            self.log_output(f"[ERROR] Batch file not found: {bat}\n")
            return
        cmd = "cmd.exe" if sys.platform == "win32" else "sh"
        args = ["/c", str(bat_path)]
        self.log_output(f"Launching batch: {bat}\n")
        if sys.platform == "win32":
            subprocess.Popen(args, cwd=str(base_dir), shell=False)
        else:
            subprocess.Popen([cmd, "/c", str(bat_path)], cwd=str(base_dir))

    def log_output(self, text):
        self.log.append(text.rstrip("\n"))

    def log_finished(self, success, message):
        color = "#198754" if success else "#dc3545"
        self.log_output(f'<span style="color:{color};">[{"OK" if success else "ERR"}] {message}</span>')

    def tool_finished(self, success, message):
        for card in self.tool_cards:
            card.on_tool_finished(success, message)

    def closeEvent(self, event):
        if self.runner.process and self.runner.process.state() == QProcess.ProcessState.Running:
            reply = QMessageBox.question(
                self, "Confirm Exit",
                "A tool is currently running. Do you want to stop it and exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.runner.terminate()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Set application-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = DTSToolkitLauncher()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
