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
double dutyCycle;                //Controls speed of motor     
int input;
double posA, posD;              //in radians/sec
int count;        //counts to determine velocity
double countsPerRevolution;   //constant with motor
double error, errorPt2;
double Kp, Ki;

//return to zero function
void returnToZero(){
  posA = 0;
}


//Read in I2C

//INSERT CODE HERE


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
  input = 2;
  posD = (double)input * 3.14/2.0;  
  posA = 0;                      
  count = 0;    
  error = 0;
  errorPt2 = 0;                                    
  dutyCycle = 200;                          //will modify angular velocity of motor
  Kp = 6;
  Ki = 0.08;


  //enable interrupt
  attachInterrupt(digitalPinToInterrupt(2), wheelTurn, CHANGE); 
}

//Main code, responsible for writing controller
void loop() {

  posD = (double)input * 3.14/4.0;  
  
  //stores current time to determine when to stop printing data and to determine if main exceeds sampling time
  timeNow = millis();
  error = posD - posA;                //units: radians
  if(error<0){
    digitalWrite(voltageDirection, LOW);
  }
  else{
    digitalWrite(voltageDirection, HIGH);
  }
  if(abs(error)<0.05){
    dutyCycle = max(0,min((Kp+Ki*0.001)*abs(error)/5.0*255.0,255));
  }
  else{
    dutyCycle = max(0,min((Kp)*abs(error)/5.0*255.0,255));
  }
  
  //dutyCycle = dutyCycle/7.8*255.0;  //possible add max 

  
  //write voltageCommand 
  analogWrite(voltageCommand,(int)dutyCycle);

  //calculate angular velocity (radians/sec)
  //velocity = ((double)count - (double)lastCount) / countsPerRevolution * 2.0 * 3.14 / (samplingTime * 0.001);
  posA = (1.0*count)/countsPerRevolution*2*3.14;
  
  
  //only print data between 1 and 2 seconds
  //if ((timeNow > 1000) && (timeNow < 2000)) {
    Serial.print(millis() / (double)1000);
    Serial.print("\t");
    Serial.print(dutyCycle);
    Serial.print("\t");
    Serial.print(posA);
    Serial.print("\t");
    Serial.print(error);
    Serial.println();
  //}

  //check to see if main running exceeded the sampling time
  if ((millis() - timeNow) > samplingTime) {
    Serial.println("Error: main exceeds sampling time");
  }

  //wait until sampling time to re run loop
  while ((millis() - timeNow) < samplingTime);
}
