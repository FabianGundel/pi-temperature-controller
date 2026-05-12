const int   PIN_NTC   = A0;      // analog input pin between R_ref and R_NTC
const float R_REF     = 2660.0;  // reference resistor value
const int   ADC_MAX   = 1023;
const int   NUM_READS = 10;      // number of measurements in N to calculate average ADC

void setup() {

  Serial.begin(9600);
  while (!Serial);  

  Serial.println("========================================");
  Serial.println("   NTC Calibration - Measurement Tool   ");
  Serial.println("========================================");
  Serial.println("----------------------------------------");
  Serial.println("    [type 'm' to start measurement]     ");
  Serial.println("----------------------------------------");
}

void loop() {

  // waiting for user input
  if (Serial.available() > 0) {
    char input = Serial.read();

    if (input == 'm' || input == 'M') {
      measurement();
    } 
  }
}

void measurement() {

  // measuring several ADC values and calculating ADC average 
  long sum = 0;
  for (int i = 0; i < NUM_READS; i++) {
    sum += analogRead(PIN_NTC);
    delay(10);
  }
  float adc_avg = (float)sum / NUM_READS;

  // calculating NTC resistance
  float R_ntc = R_REF * (adc_avg / (ADC_MAX - adc_avg));

  // output
  Serial.println("ADC_raw (avg): " + String(adc_avg));
  Serial.println("R_NTC: " + String(R_ntc) + " Ohm");
  Serial.println("----------------------------------------");
  Serial.println("    [type 'm' to start measurement]     ");
  Serial.println("----------------------------------------");
}

