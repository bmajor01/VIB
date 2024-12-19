#include <AccelStepper.h>
#include <GCodeParser.h>

GCodeParser GCode = GCodeParser();

#define X_STEP_PIN 54
#define X_DIR_PIN 55
#define X_ENABLE_PIN 38
#define Y_HOME_PIN 3
#define X_HOME_PIN 2

AccelStepper stepperX(AccelStepper::DRIVER, X_STEP_PIN, X_DIR_PIN);

void setup(){

    pinMode(X_STEP_PIN, OUTPUT);
    pinMode(X_DIR_PIN, OUTPUT);
    pinMode(X_ENABLE_PIN, OUTPUT);

    digitalWrite(X_ENABLE_PIN, LOW);

    Serial.begin(115200);
    delay(100);

}

void loop(){

  if (Serial.available() > 0)
  {

    // Belépési ponty
    if (GCode.AddCharToLine(Serial.read()))
    {
      GCode.ParseLine();

      // G kódok
      if (GCode.HasWord('G'))
      {
        if (0 == (int)GCode.GetWordValue('G'))
        {
          Serial.println("So long and thanks for all the fish");
        }
      }

      // Abszolút parancsok
      if (1 == (int)GCode.GetWordValue('G'))
      {
        if (GCode.HasWord('X'))
        {
          if (GCode.HasWord('S'))
          {
            stepperX.setSpeed((int)GCode.GetWordValue('S'));
          }

          if (GCode.HasWord('A'))
          {
            stepperX.setAcceleration((int)GCode.GetWordValue('A'));
          }
          stepperX.runToNewPosition((int)GCode.GetWordValue('X'));
        }

        Serial.println("0");
      }

      // relativ parancsok
      if (2 == (int)GCode.GetWordValue('G'))
      {
        if (GCode.HasWord('X'))
        {
          if (GCode.HasWord('S'))
          {
            stepperX.setSpeed((int)GCode.GetWordValue('S'));
          }

          if (GCode.HasWord('A'))
          {
            stepperX.setAcceleration((int)GCode.GetWordValue('A'));
          }
          stepperX.move((int)GCode.GetWordValue('X'));
          while (stepperX.run());
        }

        if (GCode.HasWord('D'))
        {
          //stepperX.disableOutputs();
          //stepperY.disableOutputs();
          digitalWrite(X_ENABLE_PIN, HIGH);
          Serial.println("disable");
        }

        Serial.println("0");

      }
    }
  }
}