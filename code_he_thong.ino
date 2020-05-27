#include <LiquidCrystal.h>
#include <string.h>
#include <TimerOne.h>
#include <TimerThree.h>
#include <AccelStepper.h>

const int rs = A8, en = A7, d4 = A6, d5 = A5, d6 = A4, d7 = A3;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

#define pwm1 7 // Bang tai 1
#define dir1A 6
#define dir1B 5

#define pwm2 8 // Bang tai 2
#define dir2A 9
#define dir2B 10

#define en 3
#define cw 4
#define clk 2

#define congtac PINB&B00000001
#define sensor1 PINL&B01000000
#define sensor2 PINL&B00000001
#define sensor3 PINL&B00010000
#define Cu_chan_ON digitalWrite(29,LOW)
#define Cu_chan_OFF digitalWrite(29,HIGH)
#define Tay_gap_ON digitalWrite(25,LOW)
#define Tay_gap_OFF digitalWrite(25,HIGH)
#define Giac_hut_ON digitalWrite(27,LOW)
#define Giac_hut_OFF digitalWrite(27,HIGH)
AccelStepper stepper(1, clk, cw);

boolean key, Run = false,Run1=true;
char Result[] = {};     // tra ve ket qua mach pass fail
unsigned char Data;
boolean Pass1 = false, Pass2 = false;
unsigned int mode = 0;

void PC();
void prossesing();
void Check_pass_fail();
void insert_Pass();
void insert_Fail();
void replease_Pass_Fail();
void quay_bang_tai_1();
void quay_bang_tai_2();
void dung_bang_tai_1();
void dung_bang_tai_2();
void Stop();
void Start();
void tay_may(int so_buoc, int van_toc, boolean dir);
void tay_gap_bang(long int Step);
void set_goc();
void check();

void setup() {
  lcd.begin(16, 2);
  Serial.begin(9600);
  Timer1.initialize(10000);
  Timer1.attachInterrupt(PC);
  Timer3.initialize(15000);
  Timer3.attachInterrupt(prossesing);

  pinMode(pwm1, OUTPUT); pinMode(dir1A, OUTPUT); pinMode(dir1B, OUTPUT);
  pinMode(pwm2, OUTPUT); pinMode(dir2A, OUTPUT); pinMode(dir2B, OUTPUT);
  pinMode(en, OUTPUT); pinMode(cw, OUTPUT); pinMode(clk, OUTPUT);
  pinMode(23, OUTPUT); pinMode(25, OUTPUT); pinMode(27, OUTPUT);
  pinMode(29, OUTPUT);
  digitalWrite(23, HIGH);
  digitalWrite(25, HIGH);
  digitalWrite(27, HIGH);
  digitalWrite(29, HIGH);

  pinMode(20, INPUT_PULLUP); pinMode(21, INPUT_PULLUP);
  pinMode(43, INPUT); pinMode(45, INPUT);
  pinMode(47, INPUT); pinMode(49, INPUT);
  pinMode(51, INPUT); pinMode(53, INPUT);

  dung_bang_tai_1();
  dung_bang_tai_2();

  // interrupt
  attachInterrupt(2, Stop, FALLING);
  attachInterrupt(3, Start, FALLING);
  delay(5);
  set_goc();
}
/********************************************* Main ****************************************************/
void loop()
{
    lcd.setCursor(0, 0);
    lcd.print(Result);
    lcd.print(" ");
    if(Run == true && mode == 2)
    {
        tay_gap_bang(-738);
        Tay_gap_ON;
        delay(1000);
        Giac_hut_ON;
        Tay_gap_OFF;
        delay(1500);
        tay_gap_bang(0);
        Tay_gap_ON;
        delay(1000);
        Giac_hut_OFF;
        Tay_gap_OFF;
        Cu_chan_OFF;
        delay(1500);
        set_goc();
        replease_Pass_Fail();
        mode = 0;
    } 
    else if(Run == true && mode == 1)
      {
        Cu_chan_OFF;
        while(sensor_filter(check_sensor(sensor3)) == 1);
        replease_Pass_Fail();
        mode = 0;
      }
}
/******************************************** Function ****************************************************/

void set_goc()
{
  int position_homing = 1;
  stepper.setMaxSpeed(100.0);
  stepper.setAcceleration(100.0);
  delay(5);
  // Xet goc toa do
  while (!sensor_filter(check_sensor(congtac))) {
    stepper.moveTo(position_homing);
    stepper.run();
    position_homing++;
    delay(5);
  }
  stepper.setCurrentPosition(0);  // Xet lai vi tri
  stepper.setMaxSpeed(100.0);     // Xet van toc
  stepper.setAcceleration(100.0); // Xet gia toc
  position_homing = -1;

  while (sensor_filter(check_sensor(congtac))) {
    stepper.moveTo(position_homing);
    stepper.run();
    position_homing--;
    delay(5);
  }
  stepper.setCurrentPosition(0);
  stepper.setMaxSpeed(1500.0);
  stepper.setAcceleration(1000.0);
}

void tay_gap_bang(long int Step)
{
  stepper.moveTo(Step);
  while (stepper.distanceToGo() != 0)
  {
    stepper.run();
  }
}
bool check_sensor(byte pin)
{
  if (pin) return false;
  else return true;
}

bool sensor_filter(bool sensor)
{
  int finish = 50;
  unsigned int count = 0;
  for (int i = 0; i < finish; i++)
  {
    if (sensor == true) count++;
    else {
      count == 0;
      return 0;
    }
  }
  if (count == finish) {
    count = 0;
    return 1;
  }
}
void check()
{
   if (Check_pass_fail(Result) == '0') {
    Cu_chan_ON;
    mode = 2;
    }
    else {
      Cu_chan_OFF;
      mode = 1;
    }
}
void prossesing()
{
  if(Run == true)
  { 
        if (sensor_filter(check_sensor(sensor1)) == 0)
        {
          if (sensor_filter(check_sensor(sensor2)) == 0)
          {
            if (sensor_filter(check_sensor(sensor3)) == 1)
            {
              check();
            }
          } else {
            if (sensor_filter(check_sensor(sensor3)) == 0)
            {
              quay_bang_tai_2();  // neu vi tri 3 chua co phoi thi cho qua
              quay_bang_tai_1();
            } else {
              dung_bang_tai_1();
              check();
            }
           }
          } 
        else if (sensor_filter(check_sensor(sensor2)) == 0 && sensor_filter(check_sensor(sensor3)) == 0) 
        {
          quay_bang_tai_1();  // doi den khi gap cb1
        }
  }
}
void PC()
{
  if (Serial.available() > 0)
  {
    Data = Serial.read();
    if (Data == 'w') {
      key = false;
      lcd.setCursor(0,1);
      lcd.print("OK");
    }
    else if (Data == 'p') {
      if (key == false) {
        insert_Pass();
        key = true;
      }
    }
    else if (Data == 'f') {
      if (key == false) {
        insert_Fail();
        key = true;
      }
    }
    else if(Data == 'a'){
      Run1 = false;
    }
  }

}
char Check_pass_fail(char* data)
{
  return data[0];
}

void insert_Pass()
{
  unsigned int lenght = strlen(Result);
  Result[lenght] = '1';
  Result[lenght+1] = '\0';
}

void insert_Fail()
{
  unsigned int lenght = strlen(Result);
  Result[lenght] = '0';
  Result[lenght+1] = '\0';
}

void replease_Pass_Fail()
{
  int lenght = strlen(Result);
  for(int i = 0; i < lenght; i++)
  {
    Result[i] = Result[i + 1];
  }
   Result[lenght-1] = '\0';
}

void quay_bang_tai_1()
{
  digitalWrite(dir2A, HIGH);
  digitalWrite(dir2B, LOW);
  analogWrite(pwm2, 30);
}

void quay_bang_tai_2()
{
  digitalWrite(dir1A, LOW);
  digitalWrite(dir1B, HIGH);
  analogWrite(pwm1, 150);
}

void dung_bang_tai_1()
{
  analogWrite(pwm2, 0);
}

void dung_bang_tai_2()
{
  analogWrite(pwm1, 0);
}

void Start()
{
  Run = true;
  lcd.setCursor(0, 1);
  lcd.print("ON");
}

void Stop()
{
  lcd.setCursor(0, 1);
  lcd.print("OF");
  dung_bang_tai_1();
  dung_bang_tai_2();
  Run = false;
}
