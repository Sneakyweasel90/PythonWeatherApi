import sys
import os
from dotenv import load_dotenv
load_dotenv()
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self) #Be deleted later, only for testing
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName('city_label')
        self.city_input.setObjectName('city_input')
        self.temperature_label.setObjectName('temperature_label')
        self.emoji_label.setObjectName('emoji_label')
        self.description_label.setObjectName('description_label')
        self.get_weather_button.setObjectName('get_weather_button')

        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: calibri;
            }
            QLabel#city_label {
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 50px;
            }
            """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        # IF YOU WANT TO RUN THIS PLEASE MAKE A .ENV FILE AND PLACE IN API_KEY={YOUR API KEY HERE}
        api_key = os.getenv("API_KEY")
        # IF YOU WANT TO RUN THIS PLEASE MAKE A .ENV FILE AND PLACE IN API_KEY={YOUR API KEY HERE}
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data['cod'] == 200:
                self.display_weather(data)


        except requests.exceptions.HTTPError as e:
            status_messages = {
                400: "Bad request:\nPlease check your input",
                401: "Unauthorized:\nInvalid API key",
                403: "Forbidden:\nPlease check your input",
                404: "Not Found:\nCity not found",
                500: "Internal Server Error:\nPlease try again later",
                502: "Bad Gateway:\nInvalid response from the server",
                503: "Service unavailable:\nService is down",
                504: "Gateway timeout:\nNo response from the server"
            }
            message = status_messages.get(response.status_code, f"HTTP Error occurred:\n {e}")
            self.display_error(message)
        except requests.exceptions.ConnectionError:
            self.display_error("Connection error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request took too long")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many requests:\nCheck the URL")
        except requests.exceptions.RequestException as e:
            self.display_error(f"Request Error:\n {e}")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        weather_description = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]

        self.temperature_label.setStyleSheet("font-size: 50px")
        self.temperature_label.setText(f"{temperature_c:.2f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        emoji_map = [
            ((200, 232), "⛈️"),  # Thunderstorm
            ((300, 321), "🌦️"),  # Drizzle
            ((500, 531), "🌧️"),  # Rain
            ((600, 622), "❄️"),  # Snow
            ((700, 741), "🌫️"),  # Mist/Fog
            ((762, 762), "🌋"),  # Volcanic Ash
            ((771, 771), "💨"),  # Squalls
            ((781, 781), "🌪️"),  # Tornado
            ((800, 800), "☀️"),  # Clear
            ((801, 804), "☁️"),  # Clouds
        ]

        for (low, high), emoji in emoji_map:
            if low <= weather_id <= high:
                return emoji
        return ""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = WeatherApp()
    main.show()
    sys.exit(app.exec_())