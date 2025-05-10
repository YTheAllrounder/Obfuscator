import sys
import os
import subprocess
import threading
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit, 
                             QProgressBar, QHBoxLayout, QCheckBox)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class ObfuscatorGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Set Window Properties
        self.setWindowTitle("Obfuscation Tool")
        self.setGeometry(100, 100, 800, 500)
        self.setWindowIcon(QIcon("icon.png"))  

        # Layouts
        layout = QVBoxLayout()

        # Title
        self.title_label = QLabel("🔒 Obfuscation Tool")
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Selected File Label (Only Name)
        self.selected_file_label = QLabel("📂 No file selected")
        self.selected_file_label.setFont(QFont("Arial", 11))
        self.selected_file_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.selected_file_label)

        # Button Layout 
        btn_layout = QHBoxLayout()
        self.browse_button = QPushButton("📂 Browse")
        self.browse_button.setFont(QFont("Arial", 11))
        self.browse_button.clicked.connect(self.select_file)
        btn_layout.addWidget(self.browse_button)

        self.obfuscate_button = QPushButton("⚙️ Obfuscate")
        self.obfuscate_button.setFont(QFont("Arial", 11))
        self.obfuscate_button.setStyleSheet("padding: 8px;")
        self.obfuscate_button.clicked.connect(self.start_obfuscation)
        btn_layout.addWidget(self.obfuscate_button)
        
        layout.addLayout(btn_layout)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Log Output
        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Consolas", 10))
        layout.addWidget(self.log_output)

        # Save Log Button
        self.save_log_button = QPushButton("💾 Save Logs")
        self.save_log_button.clicked.connect(self.save_logs)
        layout.addWidget(self.save_log_button)

        # Dark Mode Toggle
        self.dark_mode_checkbox = QCheckBox("🌙 Dark Mode (ON)")
        self.dark_mode_checkbox.setChecked(True)  
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_theme)
        layout.addWidget(self.dark_mode_checkbox)

        self.setLayout(layout)

        # Apply Default Dark Theme
        self.is_dark_mode = True
        self.set_dark_theme()

        # Store Selected File Path
        self.selected_file_path = ""

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.selected_file_path = file_path
            file_name = os.path.basename(file_path)  
            self.selected_file_label.setText(f"📂 {file_name}")
            self.log_output.append(f"📂 Selected File: {file_path}")

    def start_obfuscation(self):
        if not self.selected_file_path:
            self.log_output.append("❌ Error: No file selected.")
            return

        self.progress_bar.setValue(25)
        self.log_output.append("⚙️ Starting obfuscation...")

        def run_obfuscation():
            try:
                self.progress_bar.setValue(50)
                
                obfuscator_path = os.path.abspath("obfuscator.py")
                if not os.path.exists(obfuscator_path):
                    self.log_output.append(f"❌ Error: Could not find 'obfuscator.py' at {obfuscator_path}")
                    return

                result = subprocess.run(["python", obfuscator_path, "--file", self.selected_file_path], 
                                        capture_output=True, text=True)
                self.progress_bar.setValue(75)

                if result.returncode == 0:
                    self.log_output.append(f"✔️ Success: File obfuscated. ({self.selected_file_path})")
                else:
                    self.log_output.append(f"❌ Error: {result.stderr}")

                self.progress_bar.setValue(100)
                
                # Prevent Auto-Close
                self.log_output.append("✅ Obfuscation Completed! The application will remain open.")
                
            except Exception as e:
                self.log_output.append(f"❌ Exception: {str(e)}")

        threading.Thread(target=run_obfuscation, daemon=True).start()

    def save_logs(self):
        log_text = self.log_output.toPlainText()
        if log_text:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Logs", "", "Text Files (*.txt)")
            if file_path:
                with open(file_path, "w") as log_file:
                    log_file.write(log_text)
                self.log_output.append("✔️ Logs saved successfully.")

    def toggle_theme(self, state):
        if state == Qt.Checked:
            self.set_dark_theme()
            self.dark_mode_checkbox.setText("🌙 Dark Mode (ON)")
        else:
            self.set_light_theme()
            self.dark_mode_checkbox.setText("☀️ Light Mode (ON)")

    def set_dark_theme(self):
        self.setStyleSheet("""
            QWidget { background-color: #2c2f33; color: white; }
            QLabel { color: white; font-weight: bold; }
            QPushButton { background-color: #7289da; color: white; padding: 8px; border-radius: 5px; }
            QPushButton:hover { background-color: #5b6eae; }
            QTextEdit { background-color: #23272a; color: white; border: 1px solid #7289da; }
            QProgressBar { border: 1px solid #7289da; background: #23272a; color: white; }
            QProgressBar::chunk { background: #7289da; }
        """)
        self.is_dark_mode = True

    def set_light_theme(self):
        self.setStyleSheet("""
            QWidget { background-color: white; color: black; }
            QLabel { color: black; font-weight: bold; }
            QPushButton { background-color: #3498db; color: white; padding: 8px; border-radius: 5px; }
            QPushButton:hover { background-color: #2980b9; }
            QTextEdit { background-color: #f0f0f0; color: black; border: 1px solid #3498db; }
            QProgressBar { border: 1px solid #3498db; background: #f0f0f0; color: black; }
            QProgressBar::chunk { background: #3498db; }
        """)
        self.is_dark_mode = False

# Run the GUI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ObfuscatorGUI()
    window.show()
    sys.exit(app.exec_())
