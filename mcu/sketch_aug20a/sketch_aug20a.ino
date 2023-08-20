int x; 
char streaming = 0;
void setup() { 
	Serial.begin(115200); 
	Serial.setTimeout(1); 
} 
void loop() { 
  delay(1000);
  if (streaming){
    int data1= random(0,255);
    int data2= random(0,255);

    Serial.println(String(data1) +" "+String(data2));
    Serial.println(",");
    Serial.print(data2);
    Serial.println();

  }
	while (!Serial.available()); 
	x = Serial.readString().toInt();
  if (x==1){
    Serial.println("found 1");
    streaming = 1;
  }
} 
