from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from sklearn.ensemble import IsolationForest
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize Isolation Forest for anomaly detection
model = IsolationForest()

# Predefined monitoring rules (Example: Offensive language)
monitoring_rules = {
    'offensive_language': ['bad', 'offensive', 'curse', 'vulgar'],
    # Add more rules as needed
}

# Risk threshold for alerting
risk_threshold = 0.7

# Real-time monitoring function
@socketio.on('user_interaction')
def handle_user_interaction(data):
    message = data['message']
    
    # Check for violations of monitoring rules
    for rule, keywords in monitoring_rules.items():
        if any(keyword in message.lower() for keyword in keywords):
            emit('alert', {'message': 'Potential violation of {rule} detected!'}, broadcast=True)
    
    # Convert message to feature vector (Example: dummy implementation)
    features = np.random.random(size=(1, 10))
    
    # Predict anomaly score using Isolation Forest
    anomaly_score = model.decision_function(features)
    
    # Check if anomaly score exceeds risk threshold
    if anomaly_score > risk_threshold:
        emit('alert', {'message': 'Potential risk detected!'}, broadcast=True)

@app.route('/')
def index():
    return render_template('Hackathon.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
