// Taken from https://github.com/rdrachmanto/SitS/blob/dev/src/sensing/orp2/orp2.ino
// On 8 July 2026, based on code from Dec 31, 2025


#define VOLTAGE 5.0   //vcc voltage(unit: V)
#define OFFSET 16      //UNUSED - zero drift voltage(unit: mV)
#define LED 13         //operating instructions
#define ArrayLenth  40 //times of collection
#define orpPin A0       //orp meter output,connect to Arduino controller ADC pin
#define calPin A1       //orp cal control pin, get a offset by set it to low

double orpValue; 
// double offset=0.0;
int offset=0;
bool is_calibrated = false;
int wait_count = 5;
int orpArray[ArrayLenth];
int orpArrayIndex=0;

double avergearray(int* arr, int number);

void setup(void) {  
  Serial.begin(9600);
  pinMode(LED,OUTPUT);
  pinMode(calPin,OUTPUT);
  // digitalWrite(calPin, LOW);
  digitalWrite(calPin, HIGH);
}

void loop(void) {
  static unsigned long orpTimer=millis();   //analog sampling interval
  static unsigned long printTime=millis();
  if(millis() >= orpTimer)
  {
    orpTimer=millis()+20;
    orpArray[orpArrayIndex++]=analogRead(orpPin);    //read an analog value every 20ms
    if (orpArrayIndex==ArrayLenth) {
      orpArrayIndex=0;
    }   
    orpValue=((30*(double)VOLTAGE*1000)-(75*avergearray(orpArray, ArrayLenth)*VOLTAGE*1000/1024))/75-offset;
  }
  if(millis() >= printTime)   //Every 800 milliseconds, print a numerical
  {
    if(!is_calibrated) {
      if(wait_count==0){
        offset += (int)orpValue; 
        is_calibrated = true;
        digitalWrite(calPin, LOW);
        //Serial.print("offset: ");
        //Serial.print((int)offset);
        //Serial.println(" mV");
      }
      wait_count--;
    }
    else {
      // Serial.print("sensorid:orp2, ori:");
      Serial.print(orpArray[10]);
      Serial.print("_");
      Serial.print(orpArray[12]);
      Serial.print("_");
      Serial.print(orpArray[14]);
      Serial.print("_");
      Serial.print(orpArray[16]);
      Serial.print("_");
      Serial.print(orpArray[18]);
      Serial.print("_");
      Serial.print(orpArray[20]);
      Serial.print("_");
      Serial.print(orpArray[22]);
      Serial.print("_");
      Serial.print(orpArray[23]);
      Serial.print("_");
      Serial.print(orpArray[25]);
      Serial.print("_");
      Serial.print(orpArray[27]);
      Serial.print("_");
      Serial.print(orpArray[29]);
 
      Serial.print(",");
      Serial.println((int)orpValue);
      //Serial.println(" mV");
      digitalWrite(LED,1-digitalRead(LED)); // convert the state of the LED indicator      
    } 
    printTime=millis()+300;   
  }
}

double avergearray(int* arr, int number){
  int i;
  int max,min;
  double avg;
  long amount=0;
  if(number<=0){
    printf("Error number for the array to avraging!/n");
    return 0;
  }
  if(number<5){   //less than 5, calculated directly statistics
    for(i=0;i<number;i++){
      amount+=arr[i];
    }
    avg = amount/number;
    return avg;
  }else{
    if(arr[0]<arr[1]){
      min = arr[0];max=arr[1];
    }
    else{
      min=arr[1];max=arr[0];
    }
    for(i=2;i<number;i++){
      if(arr[i]<min){
        amount+=min;        //arr<min
        min=arr[i];
      }else {
        if(arr[i]>max){
          amount+=max;    //arr>max
          max=arr[i];
        }else{
          amount+=arr[i]; //min<=arr<=max
        }
      }//if
    }//for
    avg = (double)amount/(number-2);
  }//if
  return avg;
}
