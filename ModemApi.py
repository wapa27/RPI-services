from flask import Flask, request, jsonify
import serial

# Set up Flask app
app = Flask(__name__)

# Initialize serial connection
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

@app.route('/passCounts', methods=['POST'])
def write_to_serial():
    try:
        if not ser.is_open:
            ser.open()
        # Get the JSON data from the POST request
        data = request.get_json()
        print(data)

        if data and 'message' in data:
            # Extract the message from the JSON payload
            message = data['message']
            command = f"AT$APP msg {message}\r"
            print(command)
            ser.write(command.encode())
            ser.flush()
            response = ser.read(100)

            print(response.decode())
            # ser.close()

            return jsonify({"status": "success", "message": f"Data '{message}' written to serial port."}), 200
        else:
            # ser.close()
            return jsonify({"status": "error", "message": "Invalid data format or 'message' key missing"}), 400

    except Exception as e:
        # ser.close()
        return jsonify({"status": "error", "message": str(e)}), 500


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Accessible externally
