# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 12:06:36 2026

@author: User
"""

#ab7c15728a2503fd0d0dc5da72cc8ca0
import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel
                             ,QWidget,QVBoxLayout,QHBoxLayout,
                             QGridLayout,QPushButton,QCheckBox,
                             QRadioButton,QButtonGroup,QLineEdit 
                             )
from PyQt5.QtCore import Qt,QTime,QTimer
from PyQt5.QtGui import QFont,QFontDatabase


class wetherapp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_lable=QLabel("Enter city name: ",self)
        self.city_input=QLineEdit(self)
        self.get_wether_button=QPushButton("get Wethear:",self)
        self.tempreture_lable=QLabel(self)
        self.emoji_label=QLabel(self)
        self.description_label=QLabel(self)
        self.initUI()
    
    
    def initUI(self):
        self.setWindowTitle("wether app")
        
        vbox=QVBoxLayout()
        vbox.addWidget(self.city_lable)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_wether_button)
        vbox.addWidget(self.tempreture_lable)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        
        self.setLayout(vbox)
        
        self.city_lable.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.tempreture_lable.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        
        self.city_lable.setObjectName("city_lable")
        self.city_input.setObjectName("city_input")
        self.get_wether_button.setObjectName("get_wether_button")
        self.tempreture_lable.setObjectName("tempreture_lable")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        
        
        self.setStyleSheet("""
               QLabel,QPushButton{
                   font-family:calibri;
                   
                   } 
               QLabel#city_lable{
                   font-size:40px;
                   font-style:italic;
               }
              QLineEdit#city_input{
                  font-size:40px;
              
              }
              QPushButton#get_wether_button{
                  font-size:30px;
                  font-weight:bold;
              
              }            
             QLabel#tempreture_lable{
                 font-size:75px;
                 
             
             }  
            QLabel#emoji_label{
                font-size:100px;
                font-family:segoe UI emoji;
            
            }
            QLabel#description_label{
               font-size:50px;
            
            }
                           
                           """)
    
        self.get_wether_button.clicked.connect(self.get_wether)
        
        
    def get_wether(self):
        api_key="ab7c15728a2503fd0d0dc5da72cc8ca0"
        city=self.city_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()
            
            print(data)
            
            if data["cod"]==200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_Error:
            match response.status_code:
                case 400:
                    self.display_error("bad requast \n please check your input")
                case 401:
                    self.display_error("unauthorized \n invalid API key")
                case 403:
                    self.display_error("forbidden \n Access is denied")
                case 404:
                    self.display_error("not found \n ctiy not found")
                case 500:
                    self.display_error("internal server error \n please try again")
                case 502:
                    self.display_error("bad get way \n invalid response from server")
                case 503:
                    self.display_error("service anavailable \n service is down")
                case 504:
                    self.display_error("getway timeout \n no response from the server ")
                case _:
                    self.display_error(f"http error occured\n {http_Error}")
                    
        
        except requests.exceptions.ConnectionError:
            self.display_error("connection error \n check your connection")
        except requests.exceptions.Timeout:
            self.display_error("time error \n requast time out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("to mant redirects \n check the url")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"requast error\n {req_error}")
        
        
        
        
    def display_error(self,massage):
        self.tempreture_lable.setText(massage)
        self.tempreture_lable.setStyleSheet("font-size:30px;")
        self.emoji_label.clear()
        self.description_label.clear()
    def display_weather(self,data):
        self.tempreture_lable.setStyleSheet("font-size:75px;")
        tempreture_k=data["main"]["temp"]
        print(tempreture_k)
        tempreture_c=tempreture_k-273.15
        tempreture_f=(tempreture_k * 9/5) - 459.67
        weather_id=data["weather"][0]["id"]
        
        wethera_description=data["weather"][0]["description"]
        
        self.tempreture_lable.setText(f"{tempreture_f:.0f} F")
        self.emoji_label.setText(self.get_wether_emoji(weather_id))
        self.description_label.setText(wethera_description)
        
    @staticmethod 
    def get_wether_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "☁"
        elif 300 <= weather_id <=321:
            return"⛅"
        elif 500 <= weather_id <= 531:
            return "🌨"
        elif 600 <= weather_id <= 622:
            return "🌬"
        elif 701 <=weather_id <=741:
            return "🌫"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "⚡"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "🌤"
        elif 801 <= weather_id <=804:
            return "☁"
        else:
            return " "
        
            
        
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    wether_app = wetherapp()
    wether_app.show()
    sys.exit(app.exec_())
