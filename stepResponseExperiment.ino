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
   Motor driver shield powered by battery

*/

//variable declarations
unsigned long timeNow;
const int chanA = 2;          //encoder channel a
const int chanB = 3;          //encoder channel b
const int enable = 4;
int samplingTime;             //rate between 5-10 ms
int voltageCommand = 10;      //pwm pin controlling motor
int voltageDirection = 8; 
int dutyCycle;                //Controls speed of motor     
double velocity;              //in radians/sec
int count, lastCount;         //counts to determine velocity
double countsPerRevolution;   //constant with motor

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
  pinMode(enable, OUTPUT);                  //MUST BE SET HIGH
  pinMode(voltageCommand, OUTPUT);          //PWM
  pinMode(voltageDirection, OUTPUT);
  digitalWrite(voltageDirection,HIGH);
  digitalWrite(enable,HIGH);
  Serial.begin(115200);                     //Must change baud rate in serial monitor as well
  samplingTime = 10;                        //sampling time in ms
  countsPerRevolution = 3200;               //counts per rev on spec sheet (specific to motor)
  velocity = 0;                        
  count = 0;                                        
  lastCount = 0;
  dutyCycle = 200;                          //will modify angular velocity of motor

  //enable interrupt
  attachInterrupt(digitalPinToInterrupt(2), wheelTurn, CHANGE); 
}

//Main code, responsible for writing duty cycle at 1 second,
//calculating velocity, and displaying this data from 1-2 seconds
void loop() {
  
  //stores current time to determine when to stop printing data and to determine if main exceeds sampling time
  timeNow = millis();
  
  //write voltageCommand at 1 second
  if (millis() > 1000) {
    analogWrite(voltageCommand, dutyCycle); 
  } 

  //calculate angular velocity (radians/sec)
  velocity = ((double)count - (double)lastCount) / countsPerRevolution * 2.0 * 3.14 / (samplingTime * 0.001);
  //position calculation (helpful later on) = (1.0*count)/countsPerRevolution*2*3.14;
  lastCount = count;
  
  //only print data between 1 and 2 seconds
  if ((timeNow > 1000) && (timeNow < 2000)) {
    Serial.print(millis() / (double)1000);
    Serial.print("\t");
    Serial.print(dutyCycle);
    Serial.print("\t");
    Serial.print(velocity);
    Serial.println();
  }

  //check to see if main running exceeded the sampling time
  if ((millis() - timeNow) > samplingTime) {
    Serial.println("Error: main exceeds sampling time");
  }

  //wait until sampling time to re run loop
  while ((millis() - timeNow) < samplingTime);
}
