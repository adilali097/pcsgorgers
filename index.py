import bluetooth
import sys

def discover_devices():
    print("Scanning for devices...")
    devices = bluetooth.discover_devices(duration=8, lookup_names=True, lookup_class=True, device_id=-1, device_name=None, device_class=None, device_oui=None)
    return devices

def connect_to_device(device_address):
    port = 1  # You can change the port number if needed

    try:
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        socket.connect((device_address, port))
        print(f"Connected to {device_address}")
        return socket
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def send_data(socket, data):
    try:
        socket.send(data)
        print(f"Sent data: {data}")
    except Exception as e:
        print(f"Failed to send data: {e}")

def receive_data(socket, buffer_size=1024):
    try:
        data = socket.recv(buffer_size)
        print(f"Received data: {data}")
        return data
    except Exception as e:
        print(f"Failed to receive data: {e}")
        return None

def disconnect(socket):
    try:
        socket.close()
        print("Disconnected")
    except Exception as e:
        print(f"Failed to disconnect: {e}")

def main():
    devices = discover_devices()

    if not devices:
        print("No devices found.")
        sys.exit(1)

    for i, (addr, name, _) in enumerate(devices):
        print(f"{i + 1}. {name} ({addr})")

    try:
        choice = int(input("Enter the number of the device to connect: "))
        selected_device = devices[choice - 1]
        device_address = selected_device[0]

        socket = connect_to_device(device_address)

        if socket:
            data_to_send = input("Enter data to send: ")
            send_data(socket, data_to_send)

            received_data = receive_data(socket)
            print(f"Received: {received_data}")

            disconnect(socket)
    except KeyboardInterrupt:
        print("\nOperation aborted.")
        sys.exit(0)

if __name__ == "__main__":
    main()
