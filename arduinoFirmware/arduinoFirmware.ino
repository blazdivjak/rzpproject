#include <CapacitiveSensor.h>
/*
 * CapitiveSense Library Demo Sketch
 * Paul Badger 2008
 * Uses a high value resistor e.g. 10 megohm between send pin and receive pin
 * Resistor effects sensitivity, experiment with values, 50 kilohm - 50 megohm. Larger resistor values yield larger sensor values.
 * Receive pin is the sensor pin - try different amounts of foil/metal on this pin
 * Best results are obtained if sensor foil and wire is covered with an insulator such as paper or plastic sheet
 */

#define SENSI 200
#define STEVILO_MERITEV 5
#define STEVILO_SENZOR_PINOV 3

// 1 - 40 Mohm resistor between pins 4 & x, pin x is sensor pin, and wire, foil
CapacitiveSensor   cs_4_2 = CapacitiveSensor(4,2);
CapacitiveSensor   cs_4_5 = CapacitiveSensor(4,5);
CapacitiveSensor   cs_4_8 = CapacitiveSensor(4,8);
//CapacitiveSensor   cs_4_10 = CapacitiveSensor(4,10);
//CapacitiveSensor   cs_4_12 = CapacitiveSensor(4,12);
meritve = [ STEVILO_MERITEV * STEVILO_SENZOR_PINOV ]
poprecje = [ STEVILO_SENZOR_PINOV ]
stevec = 0

void setup()                    
{

   cs_4_2.set_CS_AutocaL_Millis(0xFFFFFFFF);     // turn off autocalibrate on channel 1 - just as an example
   cs_4_5.set_CS_AutocaL_Millis(0xFFFFFFFF);
   cs_4_8.set_CS_AutocaL_Millis(0xFFFFFFFF);
   //cs_4_10.set_CS_AutocaL_Millis(0xFFFFFFFF);
   //cs_4_12.set_CS_AutocaL_Millis(0xFFFFFFFF);
   Serial.begin(9600);
}

void loop()                    
{
    long start = millis();
    long total1 =  cs_4_2.capacitiveSensor(30);
    meritve[stevec + 0] = total1;
    long total2 =  cs_4_5.capacitiveSensor(30);
    meritve[stevec + 1] = total2;
    long total3 =  cs_4_8.capacitiveSensor(30);
    meritve[stevec + 2] = total3;

    //if (total1 > SENSI) {total1=1;}else{total1=0;}
    //if (total2 > SENSI) {total2=1;}else{total2=0;}
    //if (total3 > SENSI) {total3=1;}else{total3=0;}
    for (int i=0; i < STEVILO_SENZOR_PINOV; i++){
        poprecje[i] = 0;
        for (int j=0; j < STEVILO_MERITEV; j++){
            poprecje[i] += meritve[i+j*STEVILO_MERITEV];
        }
        povprecje[i] = (int) (povprecje[i] / STEVILO_MERITEV);
    }

    Serial.print(millis() - start);        // check on performance in milliseconds
    Serial.print("\t");                    // tab character for debug windown spacing
    Serial.print(povprecje[0]);                  // print sensor output 1
    Serial.print("\t");
    Serial.print(povprecje[1]);                  // print sensor output 2
    Serial.print("\t");
    Serial.println(povprecje[2]);                // print sensor output 3

    delay(10);                             // arbitrary delay to limit data to serial port 
    stevec += STEVILO_MERITEV;
    if(stevec >= STEVILO_MERITEV * STEVILO_SENZOR_PINOV){
        stevec = 0;
    }
}
