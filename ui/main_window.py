from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QMessageBox, QApplication, QFrame
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer


class SitSmartWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SitSmart")
        self.setFixedSize(900, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: white;
                font-family: Arial;
            }

            QLineEdit {
                background-color: #1e293b;
                border: 1px solid #263449;
                border-radius: 8px;
                padding: 10px;
                font-size: 15px;
                color: white;
            }

            QPushButton {
                background-color: #1e293b;
                border: none;
                border-radius: 9px;
                padding: 8px;
                font-size: 15px;
                color: white;
                min-height: 36px;
                max-width: 145px;
            }

            QPushButton:hover {
                background-color: #334155;
            }
        """)

        self.time_left = 1500
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        title = QLabel("SitSmart")
        title.setStyleSheet("font-size: 42px; font-weight: bold; margin-bottom: 0px;")

        subtitle = QLabel("Healthy breaks for productive work")
        subtitle.setStyleSheet("font-size: 16px; color: #94a3b8; margin-top: 0px;")

        status = QLabel("●  Time to focus")
        status.setStyleSheet("""
            background-color: #202a3d;
            color: white;
            border-radius: 9px;
            padding: 10px 18px;
            font-size: 15px;
        """)

        self.timer_label = QLabel("25:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("""
            font-size: 76px;
            font-weight: 400;
            margin-top: 25px;
            margin-bottom: 10px;
        """)

        line = QFrame()
        line.setFixedHeight(5)
        line.setStyleSheet("""
            background-color: #263449;
            border-radius: 3px;
            max-width: 480px;
        """)

        self.image_label = QLabel()
        pixmap = QPixmap("ui/static/vector_graphic.png")

        cropped = pixmap.copy(520, 120, 850, 700)

        self.image_label.setPixmap(
            cropped.scaled(340, 340, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        self.image_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.work_input = QLineEdit()
        self.work_input.setPlaceholderText("25")

        self.break_input = QLineEdit()
        self.break_input.setPlaceholderText("5")

        work_label = QLabel("WORK TIME (MINUTES)")
        break_label = QLabel("BREAK TIME (MINUTES)")
        work_label.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: bold;")
        break_label.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: bold;")

        input_labels = QHBoxLayout()
        input_labels.addWidget(work_label)
        input_labels.addWidget(break_label)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(18)
        input_layout.addWidget(self.work_input)
        input_layout.addWidget(self.break_input)

        self.start_button = QPushButton("▷  Start")
        self.pause_button = QPushButton("Ⅱ  Pause")
        self.reset_button = QPushButton("↻  Reset")

        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #a855f7
                );
                border: none;
                border-radius: 9px;
                padding: 8px;
                font-size: 15px;
                color: white;
                min-height: 36px;
                max-width: 145px;
            }
        """)

        self.start_button.clicked.connect(self.start_timer)
        self.pause_button.clicked.connect(self.pause_timer)
        self.reset_button.clicked.connect(self.reset_timer)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(14)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.reset_button)

        top_text = QVBoxLayout()
        top_text.setSpacing(2)
        top_text.addWidget(title)
        top_text.addWidget(subtitle)

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(30, 30, 0, 30)
        left_layout.setSpacing(18)
        left_layout.addLayout(top_text)
        left_layout.addSpacing(25)
        left_layout.addWidget(status)
        left_layout.addWidget(self.timer_label)
        left_layout.addWidget(line)
        left_layout.addSpacing(15)
        left_layout.addLayout(input_labels)
        left_layout.addLayout(input_layout)
        left_layout.addLayout(button_layout)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(0)

        main_layout.addLayout(left_layout, 3)
        main_layout.addWidget(self.image_label, 2)

        self.setLayout(main_layout)

    def start_timer(self):
        work_minutes = self.work_input.text()
        if work_minutes.isdigit():
            self.time_left = int(work_minutes) * 60
        self.timer.start(1000)

    def update_timer(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.setText(f"{minutes:02}:{seconds:02}")

        if self.time_left > 0:
            self.time_left -= 1
        else:
            self.timer.stop()
            QApplication.beep()
            QMessageBox.information(
                self,
                "Session Complete",
                "Time to stand up and take a break!"
            )

    def pause_timer(self):
        self.timer.stop()

    def reset_timer(self):
        self.timer.stop()
        self.time_left = 1500
        self.timer_label.setText("25:00")