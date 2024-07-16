from flask import Flask, request, jsonify
from main import main
app = Flask(__name__)

# Initialize an empty list to store data
data_list = []

@app.route('/post_video', methods=['POST'])
def receive_data():

    # Validate and process the data using your custom function
    try:
        video_path = r"C:\Users\prani\OneDrive\Pictures\Camera Roll\WIN_20240716_12_38_55_Pro.mp4"
        main(video_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Bad request

    # Return a success response (optional)
    return jsonify({'message': 'Data received successfully'}), 200

if __name__ == '__main__':
    app.run(host='192.168.29.216', port=5000, debug=True)
