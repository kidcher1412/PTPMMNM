from flask import Flask, request, jsonify
from RoomGame import RoomGame

app = Flask(__name__)

@app.route('/create_room', methods=['POST'])
def create_room():
    data = request.get_json()
    try:
        if 'room_name' in data:
            room_name = data['room_name']
            new_chat_room = RoomGame()
            return jsonify({'message': 'Room {} created successfully'.format(new_chat_room.get_return_ID())})
        else:
            return jsonify({'message': 'Missing room_name parameter'}), 400
    except Exception as e:
        return jsonify({'message': 'Error: {}'.format(str(e))}), 500

@app.route('/hello', methods=['POST'])
def hello():
    data = request.get_json()
    try:
        return jsonify({'message': 'ACK catch {}'.format(data)})
    except Exception as e:
        return jsonify({'message': 'Error: {}'.format(str(e))}), 500

if __name__ == '__main__':
    app.run(port=8080)
