
import sys
import webbrowser
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDateTimeEdit
from PyQt5.QtCore import QDateTime, QTimer, Qt

class WebAppScheduler(QMainWindow):
    """
    QMainWindow를 상속받아 웹사이트 예약 프로그램을 구현하는 메인 클래스입니다.
    """
    def __init__(self):
        """
        생성자입니다. 부모 클래스의 생성자를 호출하고 UI를 초기화합니다.
        """
        super().__init__()
        self.url_to_open = ""  # 예약된 URL을 저장할 변수
        self.initUI()

    def initUI(self):
        """
        사용자 인터페이스를 생성하고 설정합니다.
        """
        # 윈도우 기본 설정
        self.setWindowTitle('웹사이트 예약 프로그램')
        self.setGeometry(300, 300, 400, 200)

        # 중앙 위젯 및 레이아웃 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # URL 입력 부분
        url_layout = QHBoxLayout()
        url_label = QLabel('웹사이트 주소:')
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('https://www.example.com')
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        main_layout.addLayout(url_layout)

        # 날짜 및 시간 선택 부분
        datetime_layout = QHBoxLayout()
        datetime_label = QLabel('예약 시간:')
        self.datetime_edit = QDateTimeEdit(self)
        self.datetime_edit.setDateTime(QDateTime.currentDateTime())
        self.datetime_edit.setCalendarPopup(True)
        self.datetime_edit.setDisplayFormat('yyyy-MM-dd hh:mm:ss')
        datetime_layout.addWidget(datetime_label)
        datetime_layout.addWidget(self.datetime_edit)
        main_layout.addLayout(datetime_layout)

        # 예약 버튼
        self.schedule_button = QPushButton('예약하기', self)
        self.schedule_button.clicked.connect(self.schedule_website)
        main_layout.addWidget(self.schedule_button)

        # 상태 표시 라벨
        self.status_label = QLabel('예약을 설정해주세요.', self)
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

    def schedule_website(self):
        """
        입력된 정보로 웹사이트 열기를 예약합니다.
        """
        url = self.url_input.text()
        if not url.startswith('http'):
            url = 'http://' + url
        
        self.url_to_open = url
        schedule_time = self.datetime_edit.dateTime()
        current_time = QDateTime.currentDateTime()

        msecs_to_schedule = current_time.msecsTo(schedule_time)

        if msecs_to_schedule < 0:
            self.status_label.setText('오류: 현재 시간보다 이전으로 예약할 수 없습니다.')
            return

        # QTimer.singleShot을 사용하여 지정된 시간 후에 open_website 메서드를 한 번 호출합니다.
        QTimer.singleShot(msecs_to_schedule, self.open_website)
        
        # 사용자에게 예약 완료 상태를 알립니다.
        schedule_time_str = schedule_time.toString('yyyy-MM-dd hh:mm:ss')
        self.status_label.setText(f'예약 완료: {schedule_time_str}')
        self.schedule_button.setEnabled(False) # 예약 후 버튼 비활성화

    def open_website(self):
        """
        예약된 시간에 웹사이트를 엽니다.
        """
        if self.url_to_open:
            webbrowser.open(self.url_to_open)
            self.status_label.setText(f'완료: "{self.url_to_open}"을(를) 열었습니다.')
            self.schedule_button.setEnabled(True) # 작업 완료 후 버튼 다시 활성화

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WebAppScheduler()
    ex.show()
    sys.exit(app.exec_())
