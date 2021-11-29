#if !( ARDUINO_ARCH_NRF52840 && TARGET_NAME == ARDUINO_NANO33BLE )
  #error This code is designed to run on nRF52-based Nano-33-BLE boards using mbed-RTOS platform! Please check your Tools->Board setting.
#endif
#define _TIMERINTERRUPT_LOGLEVEL_     0

#include "NRF52_MBED_TimerInterrupt.h"

#define TIMER0_INTERVAL_MS        20 //50Hz
#define TIMER1_INTERVAL_MS        25 //40Hz

#include <Arduino_LSM9DS1.h>
//-------------Init variables -----------------------------------
volatile int flag0=0;
volatile int flag1=0;
int timer0;
int timer1;
int timer_lab;
int label_id;
int counter;
int counter0;
int counter1;
uint32_t prevtime0;
uint32_t prevtime1;
volatile uint32_t preMillisTimer0 = 0;
volatile uint32_t preMillisTimer1 = 0;
bool started;
//----------------- TIMERS -------------------------------
// Init NRF52 timer NRF_TIMER3
NRF52_MBED_Timer ITimer0(NRF_TIMER_3);
void TimerHandler0()
{  
  flag0 = 1;
}

// Init NRF52 timer NRF_TIMER4
NRF52_MBED_Timer ITimer1(NRF_TIMER_4);
void TimerHandler1()
{
  flag1 = 1; 
}

//------------------ SETUP ------------------------------
void setup() {
  pinMode(12, OUTPUT);
  digitalWrite(12, 1);
  // put your setup code here, to run once:

  Serial.begin(115200); 
  Serial.print("setup test");
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
    
  Serial.setTimeout(1);
  
  flag0=0;
  flag1=0;
  timer0=0;
  timer1=1;
  timer_lab=7;
  counter=0;
  counter0=0;
  counter1=0;
  started=false;
  delay(100);
  
  // Interval in microsecs
  if (ITimer0.attachInterruptInterval(TIMER0_INTERVAL_MS * 1000, TimerHandler0))
  {
    preMillisTimer0 = millis();
    Serial.print(F("Starting ITimer0 OK, millis() = ")); Serial.println(preMillisTimer0);
//    flag0 = 1;
  }
  else
    Serial.println(F("Can't set ITimer0. Select another freq. or timer"));

  // Interval in microsecs
  if (ITimer1.attachInterruptInterval(TIMER1_INTERVAL_MS * 1000, TimerHandler1))
  {
    preMillisTimer1 = millis();
    Serial.print(F("Starting ITimer1 OK, millis() = ")); Serial.println(preMillisTimer1);
//    flag1 = 1;
  }
  else
    Serial.println(F("Can't set ITimer1. Select another freq. or timer"));
    
  prevtime0=(uint32_t)micros();
  prevtime1=prevtime0;
}
//------------------ LOOP ------------------------------
void loop() {
  // put your main code here, to run repeatedly:
  float Ax, Ay, Az, Gx, Gy, Gz, Mx, My, Mz;
    
  unsigned int pream = 0xAA55AA55;
  int interval0 = TIMER0_INTERVAL_MS;
  int interval1 = TIMER1_INTERVAL_MS;
  int com_code;
  
   if (!started)
   {
      if (Serial.available())
      {
        com_code = Serial.readString().toInt(); //Serial.read();
        if (com_code==0)
        {
          started=true;          
          Serial.write((byte *) &pream, 4);
          Serial.write((byte *) &timer_lab, 4);
          uint32_t time_micros = micros();  
          Serial.write((byte *) &time_micros, 8); 
          Serial.write((byte *) &com_code, 4);      
          Serial.write((byte *) &interval0, 4);
          Serial.write((byte *) &interval1, 4);
         }
         else{return;}
        }
        else {return;}      
    }  
        
    if (Serial.available()>0)
    {
      com_code = Serial.readString().toInt(); 
      if (com_code==-1)
      {
        started=false;
        return;  
      }
      else if(com_code>0)
      {
        Serial.write((byte *) &pream, 4);
        Serial.write((byte *) &timer_lab, 4);     
        uint32_t time_micros = micros();  
        Serial.write((byte *) &time_micros, 8); 
        Serial.write((byte *) &com_code, 4);  
      }
   }

    if (flag0==1)
    {
      flag0=0;
      counter0++;   
      int a0 = analogRead(A0);
      int a1 = analogRead(A1);
      int a2 = analogRead(A2);
      int a3 = analogRead(A3);
      int a4 = analogRead(A4);
      int a5 = analogRead(A5);
      int a6 = analogRead(A6);
      int a7 = analogRead(A7);
  
      Serial.write((byte *) &pream, 4);              
      Serial.write((byte *) &timer0, 4);
      Serial.write((byte *) &a0, 4);
      Serial.write((byte *) &a1, 4); 
      Serial.write((byte *) &a2, 4); 
      Serial.write((byte *) &a3, 4); 
      
      Serial.write((byte *) &a4, 4);
      Serial.write((byte *) &a5, 4); 
      Serial.write((byte *) &a6, 4); 
      Serial.write((byte *) &a7, 4);    
     }
  
    if (flag1==1)
    {
      flag1=0;     
      counter1++;
      if (IMU.accelerationAvailable()) 
      {
        IMU.readAcceleration(Ax, Ay, Az);
      }
      if (IMU.gyroscopeAvailable()) 
      {   
        IMU.readGyroscope(Gx, Gy, Gz);
      }  
      IMU.readMagneticField(Mx, My, Mz);
      
      
      Serial.write((byte *) &pream, 4); 
      Serial.write((byte *) &timer1, 4);     
      Serial.write((byte *) &Ax, 4);
      Serial.write((byte *) &Ay, 4);
      Serial.write((byte *) &Az, 4);  
      Serial.write((byte *) &Gx, 4);
      Serial.write((byte *) &Gy, 4);
      Serial.write((byte *) &Gz, 4);  
      Serial.write((byte *) &Mx, 4);
      Serial.write((byte *) &My, 4);
      Serial.write((byte *) &Mz, 4);  
    }
  
}
