import asyncio
from bleak import BleakClient, BleakError
import RPi.GPIO as GPIO

# --- Constants ---
LIGHT_CHARACTERISTIC_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"  # UUID of the Bluetooth characteristic for light data
ARDUINO_MAC_ADDRESS = "08:3A:8D:9B:F7:3A"  # Replace with your Arduino's Bluetooth MAC address

led_pins = [17, 18, 27]  # GPIO pins connected to the LEDs (adjust to your setup)
thresholds = [100, 500, 900]  # Light levels that trigger each LED

# --- Setup ---
def setup():
    """Initializes GPIO pins for LED control."""
    GPIO.setmode(GPIO.BCM)       # Use BCM pin numbering
    GPIO.setwarnings(False)      # Disable unnecessary warnings
    for pin in led_pins:
        GPIO.setup(pin, GPIO.OUT) # Set pins as output
        GPIO.output(pin, GPIO.LOW)# Turn off all LEDs initially

# --- LED Control ---
def led_control(value):
    """Controls LEDs based on the light value.
    
       Args:
           value: The light value received from the Bluetooth sensor.
    """
    for i, pin in enumerate(led_pins):
        GPIO.output(pin, value >= thresholds[i])  # Turn on LED if value exceeds its threshold


# --- Main Async Loop ---
async def run():
    client = BleakClient(ARDUINO_MAC_ADDRESS, timeout=10.0)  
    while True:
        setup()  # Ensure GPIO is set up on each loop iteration (in case of errors)

        # --- Connection ---
        if not client.is_connected:
            print("Connecting to LightSensor device...")
            try:
                await client.connect()  # Attempt connection
                print("Connected to LightSensor!")
            except BleakError as e:
                print(f"Connection error: {e}") 
                await asyncio.sleep(5)  # Wait before retrying
                continue

        # --- Data Reading and LED Control ---
        try:
            light_value_bytes = await client.read_gatt_char(LIGHT_CHARACTERISTIC_UUID)  # Read light data
            light_value = int.from_bytes(light_value_bytes, byteorder='little') # Convert to integer
            print(f"Received light value: {light_value}")
            led_control(light_value)  # Adjust LEDs based on value
            await asyncio.sleep(1)    # Pause for 1 second before next reading
        except BleakError as e:
            print(f"Error reading characteristic or disconnected: {e}")


# --- Script Execution ---
if __name__ == "__main__":
    asyncio.run(run())  # Start the async event loop
    GPIO.cleanup()      # Clean up GPIO pins when the script ends
