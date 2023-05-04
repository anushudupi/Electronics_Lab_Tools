#include <AD9833.h>     // Include the library

#define FNC_PIN 10       // Can be any digital IO pin

AD9833 gen(FNC_PIN);       // Defaults to 25MHz internal reference frequency

WaveformType waveType=SINE_WAVE;
int hz=100;

void setup() {
    gen.Begin();             
    Serial.begin(250000);
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readString();
    int separatorIndex = input.indexOf(":");
    if (separatorIndex >= 0) {
      String a = input.substring(0, separatorIndex);
      String b = input.substring(separatorIndex + 1);
      int wt = a.toInt();
      hz = b.toInt();
      switch (wt) {
        case 1:
          waveType=TRIANGLE_WAVE;
          break;
        case 2:
          waveType=SINE_WAVE;
          break;
        case 3:
          waveType=SQUARE_WAVE;
          break;
    }
    }
  } 
  else {
        gen.ApplySignal(waveType,REG0,hz);
        gen.EnableOutput(true);  
        Serial.println(analogRead(A0)); 
    }
}
