from pymodbus.client import ModbusTcpClient
import paho.mqtt.client as mqtt
import time

# Modbus connection
modbus_client = ModbusTcpClient("127.0.0.1", port=502)

# Connect to Modbus Slave
if not modbus_client.connect():
    print("Modbus connection failed")
    exit()

# MQTT connection
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.connect("127.0.0.1", 1883)
mqtt_client.loop_start()

print("Gateway Started")

while True:

    # Read 10 holding registers from Modbus Slave
    result = modbus_client.read_holding_registers(
        address=0,
        count=10
    )

    if result.isError():
        print("Modbus read failed")

    else:
        values = result.registers

        print("10 Register Values:")

        for i, value in enumerate(values):
            print(f"Register {i}: {value}")

            # Publish each register separately
            mqtt_client.publish(
                f"solar/register{i}",
                str(value)
            )

    time.sleep(5)