/*
 * Crypto Alert takes in a Y/N command to enable/disable LED
 */

/*
 * The output pin for you LED
 */
const int ledPin = 14;

void setup()
{
  Serial.begin(9600); // USB is always 12 Mbit/sec
  pinMode(ledPin, OUTPUT);
}

void loop()
{
  String data;
  Serial.println("Crypto Alert is listening...");
  delay(1000);  // do not print too fast!
  if (Serial.available() > 0) {
    data = Serial.read();
    Serial.print("Bitcoin Alert received: ");
    Serial.println(data);
    if (data == "Y") {
      digitalWrite(ledPin, HIGH);   // set the LED on
    }
    if (data == "N") {
      digitalWrite(ledPin, LOW);   // set the LED off
    }
  }
}

