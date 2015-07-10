#define CM 1      //Centimeter
#define INC 0     //Inch
#define TP 8      //Trig_pin
#define EP 9      //Echo_pin

int sonarFron;
int sonarDer;
int sonarIzq;
int distance_cm;
long microseconds;
int orientacion;

void setup(){
  pinMode(TP,OUTPUT);       // set TP output for trigger  
  pinMode(EP,INPUT);        // set EP input for echo
  Serial.begin(19200);      // init serial 9600
}
 
void loop(){
  for(int i = 0; i < 300; i++){  
    SendMessage(1);
    delay(100);
  }
  EndCom();
  
}

long TP_init(){                     
  digitalWrite(TP, LOW);                    
  delayMicroseconds(2);
  digitalWrite(TP, HIGH);                 // pull the Trig pin to high level for more than 10us impulse 
  delayMicroseconds(10);
  digitalWrite(TP, LOW);
  long microseconds = pulseIn(EP,HIGH);   // waits for the pin to go HIGH, and returns the length of the pulse in microseconds
  return microseconds;                    // return microseconds
}

void EndCom(){
  Serial.print(0);
  Serial.print(" ");
  Serial.println(millis());
}

void SendMessage(int mssType){
  microseconds = TP_init();
  sonarIzq = microseconds/58;
  sonarFron = 0;
  sonarDer = 0;
  orientacion = 0;
  
  Serial.print(mssType);
  Serial.print(" ");
  Serial.print(millis());
  Serial.print(" ");
  Serial.print(orientacion);
  Serial.print(" ");
  Serial.print(sonarIzq);
  Serial.print(" ");
  Serial.print(sonarFron);
  Serial.print(" ");
  Serial.println(sonarDer);
  
}
