from pymodbus.client import ModbusTcpClient
import paho.mqtt.client as mqtt
import time

# Modbus connection
modbus_client = ModbusTcpClient("127.0.0.1", port=502)

# MQTT connection
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.connect("127.0.0.1", 1883)
mqtt_client.loop_start()

print("Gateway Started")

while True:

    # Read power from Modbus
    result = modbus_client.read_holding_registers(address=0, count=1)

    if result.isError():
        print("Modbus read failed")
    else:
        power = result.registers[0]

        print("Solar Power:", power)

        # Publish to MQTT
        mqtt_client.publish("solar/power", str(power))

        print("Published to MQTT")

    time.sleep(5)