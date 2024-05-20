#include <ArduinoBLE.h>  // Include the ArduinoBLE library

// --- Constants ---
const int lightSensorPin = A7;       // Analog pin for the light sensor

// Bluetooth Low Energy (BLE) Service and Characteristic Setup
BLEService lightService("19b10000-e8f2-537e-4f6c-d104768a1214");      // Create a BLE service
BLEIntCharacteristic lightCharacteristic("19b10001-e8f2-537e-4f6c-d104768a1214", BLERead | BLENotify); // Create a characteristic for light data (readable and notifiable)


// --- Setup ---
void setup() {
    Serial.begin(9600);   // Initialize serial communication for debugging
    while (!Serial);      // Wait for serial port to connect (important on some boards)

    // Initialize BLE
    if (!BLE.begin()) {
        Serial.println("Starting BLE failed!");
        while (1);         // Halt if BLE initialization fails
    }

    // Set up BLE Peripheral
    BLE.setLocalName("LightSensor");          // Set the device name (seen by the central device)
    BLE.setAdvertisedService(lightService);    // Advertise the light service

    // Add characteristic to the service
    lightService.addCharacteristic(lightCharacteristic);

    // Add service to the device
    BLE.addService(lightService);

    // Start advertising
    BLE.advertise();   
    Serial.println("BLE Light Sensor Peripheral Ready"); // Confirmation message
}

// --- Main Loop ---
void loop() {
    BLEDevice central = BLE.central();  // Check for a central device (e.g., your Raspberry Pi) trying to connect

    if (central) {  // If a central is connected...
        Serial.println("Connected to central device!");

        while (central.connected()) {  // While connected...
            int lightValue = analogRead(lightSensorPin);  // Read light sensor value
            Serial.print("Light Value: ");
            Serial.println(lightValue);

            lightCharacteristic.writeValue(lightValue);  // Update the BLE characteristic with the light value
            delay(1000); // Delay for 1 second (adjust as needed)
        }

        Serial.print("Disconnected from central: ");
        Serial.println(central.address());
    }
}


