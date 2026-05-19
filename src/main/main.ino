// work in progress
//--------------------------------------------------------------


//pid parameter
double Kp = 0.0;//insert Kp;
double Ki = 0.0;//insert Ki;
double Kd = 0.0;//insert Kd;

//temperature
double setpoint = 50.0; // °C (<= 90°C !!!)
const int NUM_READS = 5;
const double TEMP_MAX = 95.0; // °C

//steinhart-hart
const double A = 0.0007927;
const double B = 0.0003015;
const double C = -0.0000002659;

//hardware
const int PIN_NTC = A0;
const int PIN_MOSFET = 9;

const double V_REF = 5.0;
const double R_REF = 2660.0;

//intern

double temperature = 0.0;
double lastPrintedTemp = 0.0;

double errorPid = 0.0;
double previousError = 0.0;

double integral = 0.0;
double derivative = 0.0;

double output = 0.0;

unsigned long previousTime = 0;

//setup

void setup() {

  Serial.begin(115200);

  pinMode(PIN_MOSFET, OUTPUT);

  analogWrite(PIN_MOSFET, 0);

  previousTime = millis();

  Serial.println("PID Temperaturcontroller gestartet");
}

//loop
void loop() {

  //time
  unsigned long currentTime = millis();
  double dt = (currentTime - previousTime) / 1000.0;

  if (dt <= 0.0) return;

  previousTime = currentTime;

  temperature = readTemperature();

  //safety cutoff
  if (temperature > TEMP_MAX) {
    Serial.println("WARNING: Temperature is too high!");
    while (true) {
      analogWrite(PIN_MOSFET, 0);
    } 
  }

  //pid controll calculation
  errorPid = setpoint - temperature;

  derivative = (errorPid - previousError) / dt;

  double rawOutput = (Kp * errorPid) + (Ki * integral) + (Kd * derivative);

  if (rawOutput > 0 && rawOutput < 255) { 
    integral += errorPid * dt; 
    
    rawOutput = (Kp * errorPid) + (Ki * integral) + (Kd * derivative);
  } //integral only for finetuning

  
  previousError = errorPid;

  //pwm output
  output = constrain(rawOutput, 0, 255);

  analogWrite(PIN_MOSFET, (int)output);

  //serial output
  if (abs(temperature - lastPrintedTemp) > 0.1) {

    Serial.println("Setpoint: " + String(setpoint) + "°C");
    Serial.println("Process: " + String(temperature) + "°C");
    Serial.println("PWM: " + String(output));
    Serial.println("Error: " + String(errorPid));
    Serial.println("---------------------------------------");

    lastPrintedTemp = temperature;
  }
  
  
}


//temperature measurement
double readTemperature() {

  long sum = 0;
  for (int i = 0; i < NUM_READS; i++) {
    sum += analogRead(PIN_NTC);
    delay(10);
  }
  float adc_avg = (float)sum / NUM_READS;

  adc_avg = constrain(adc_avg, 1, 1022);

 
  double voltage =
    (adc_avg * V_REF) / 1023.0;

 
  double ntcResistance =
    R_REF * ((V_REF / voltage) - 1.0);

 
  double lnR = log(ntcResistance);

  double temperatureKelvin =
    1.0 / (A + (B * lnR) + (C * lnR * lnR * lnR));

  double temperatureCelsius = temperatureKelvin - 273.15;

  return temperatureCelsius;
}
