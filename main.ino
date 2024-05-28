#include <GyverOLED.h>
#include <GyverBME280.h>
#define btn 2
#define mainDELAY 2500
GyverBME280 bme;
GyverOLED<SSD1306_128x64, OLED_NO_BUFFER> oled;

int btnState = 0;
int flag = 0;
void setup() {
  if (!bme.begin(0x76)) Serial.println("Error!");
  pinMode(btn, INPUT);
  digitalWrite(btn, HIGH);
  oled.init();        // инициализация
  oled.clear();       // очистка
  oled.setScale(2);   // масштаб текста (1..4)
  oled.home();        // курсор в 0,0
  oled.print("Ведро ВКЛ!");
  Serial.begin(9600);
  delay(1000);

  oled.setScale(1);
  // курсор на начало 3 строки
  oled.setCursor(0, 3);
  oled.print("MeteoVedro v1.1");
  delay(2000);
  checkSerial();
}
void loop() {
    btnUpdate();
    if (btnState == 0){
      screenSetState1();
      delay(mainDELAY);
    }
    else if (btnState == 1){
      screenSetState2();
      delay(mainDELAY);
    }
    else if (btnState == 2){
      screenSetState3();
      delay(mainDELAY);
    }
    else if (btnState == 3){
      screenSetState4();
      delay(mainDELAY);
    }
    message();
}


void btnUpdate(){
  if (digitalRead(btn) == 0){
      btnState++;
      delay(500); 
  }
  if (btnState >= 5){
      btnState = 0;  
  }
}

void screenSetState1(){
  float temp = bme.readTemperature();
  float pres = bme.readPressure();
  float hum = bme.readHumidity();
  oled.clear();
  oled.setCursor(0,0);
  oled.setScale(2);
  oled.print("Главная:");
  oled.setCursor(0,3);
  oled.setScale(1);
  oled.print("Температура: ");
  oled.print(temp);
  oled.setCursor(0,5);
  oled.setScale(1);
  oled.print("Давление: ");
  oled.print(pres / 132);
  oled.setCursor(0,7);  
  oled.print("Влажность: ");
  oled.print(hum);
}


void screenSetState2(){
  float temp = bme.readTemperature();
  oled.clear();
  oled.setScale(2);
  oled.setCursor(0,2);
  oled.print("Temp: ");
  oled.setCursor(0,5);
  oled.print(temp);
  oled.print("°C");
}

void screenSetState3(){
  float pres = bme.readPressure();
  oled.clear();
  oled.setScale(2);
  oled.setCursor(0,2);
  oled.print("Давление: ");
  oled.setCursor(0,5);
  oled.print(pres / 132);
}

void screenSetState4(){
  float hum = bme.readHumidity();
  oled.clear();
  oled.setScale(2);
  oled.setCursor(0,2);
  oled.print("Влажность: ");
  oled.setCursor(0,5);
  oled.print(hum);
  oled.print("%");
}


void screenSetStateOFFLINE(){
  oled.clear();
  oled.setScale(2);
  oled.home();
  oled.print("Сервер ");
  oled.setCursor(0,2);
  oled.print("оффлайн!");
  delay(5000); 
}


bool checkSerial(){
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    if (data == "Server online"){
      flag = 1;
    }
  }
  else{
    screenSetStateOFFLINE();
  }
}

void message(){
  if (Serial.available() < 0){
    return;
  }
  float temp = bme.readTemperature();
  float pres = bme.readPressure();
  float hum = bme.readHumidity();
  if (Serial.readStringUntil('\n') == "Data request"){
    Serial.println(temp);
    Serial.println(pres / 132);
    Serial.println(hum);
  }
  if (Serial.readStringUntil('\n') == "Data set"){
    int max_data = Serial.parseInt();
    int min_data = Serial.parseInt();
    if (bme.readTemperature() <= min_data){
      tone(piezoPin, 550, 500);
    }  
    else if (bme.readTemperature() >= max_data){
      tone(piezoPin, 250, 500);
}
}