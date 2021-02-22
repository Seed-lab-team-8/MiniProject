/* Step Response Experiment

   Function:
   Output current time, motor voltage command, and angular velocity
   at each given sampling interval

   Setting up hardware:
   attach motor driver shield to arduino
   attach motor encoder to motor driver shield
      Green to ground
      Blue to 5V
      Yellow to digital i/o 2
      White to digital i/o 3
   also somehow hook up voltage command to driver ? pin 9/10?

*/

//variable declarations

unsigned long timeNow;
const int chanA = 2; //encoder channel a
const int chanB = 3; //encoder channel b
int samplingTime; //rate between 5-10 ms, if errors keep occuring, increase baud rate
int voltageCommand = 9; //output pin
int dutyCycle;
int velocity;
int count, lastCount;
double countsPerRevolution;

//interrupt associated with encoder
void wheelTurn() {
  //determine if clockwise or counterclockwise and increment accordingly
  if (digitalRead(chanA) != digitalRead(chanB)) {
    count++;
  }
  else {
    count--;
  }
}

void setup() {
  pinMode(chanA, INPUT_PULLUP);
  pinMode(chanB, INPUT_PULLUP);
  pinMode(voltageCommand, OUTPUT);
  samplingTime = 10;        //sampling time in ms
  countsPerRevolution = 64; //counts per rev on spec sheet (specific to motor)
  velocity = 0;
  count = 0;
  lastCount = 0;
  dutyCycle = 255;
  attachInterrupt(digitalPinToInterrupt(2), wheelTurn, CHANGE);
}

void loop() {
  //write voltageCommand at 1 second
  if (millis() == 1000) {
    analogWrite(voltageCommand, dutyCycle); 
  }
  //runs at fixed cycle time (sampling time)
  timeNow = millis();

  //calculate angular velocity (radians/sec)
  velocity = ((double)count - (double)lastCount) / countsPerRevolution * 2.0 * 3.14 / (samplingTime * 10 ^ -3);

  //only print data between 1 and 2 seconds
  if ((timeNow > 1000) && (timeNow < 2000)) {
    Serial.print(millis() / (double)1000);
    Serial.print("\t");
    Serial.print(analogRead(voltageCommand));
    Serial.print("\t");
    Serial.print(velocity);
    Serial.println();
  }

  //check to see if main running exceeded the sampling time
  if ((millis() - timeNow) > samplingTime) {
    Serial.println('Error: main exceeds sampling time');
  }

  //wait until sampling time to re run loop
  while ((millis() - timeNow) < samplingTime);




}
