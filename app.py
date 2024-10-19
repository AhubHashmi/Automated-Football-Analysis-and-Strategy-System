from flask import Flask, jsonify, render_template, send_file, make_response
from flask_cors import CORS
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

app = Flask(__name__)
CORS(app)

# Sample football analysis data
football_data = {
    "goals_scored": {"Team A": 2, "Team B": 3},
    "possession": {"Team A": 55, "Team B": 45},
    "shots_on_target": {"Team A": 5, "Team B": 7},
    "goals_timeline": {"Team A": 0, "Team B": 3},
    "passing_accuracy": {"Team A": 85, "Team B": 80},
    "tackles_made": {"Team A": 14, "Team B": 12},
    "corners_taken": {"Team A": 6, "Team B": 4},
    "fouls_committed": {"Team A": 10, "Team B": 8}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    return jsonify(football_data)

# Helper function to create and encode chart image
def create_chart(fig):
    png_image = io.BytesIO()
    fig.savefig(png_image, format="png")
    png_image.seek(0)
    png_image_b64_string = base64.b64encode(png_image.getvalue()).decode('utf8')
    plt.close(fig)  # Close the figure after saving it to avoid memory issues
    return png_image_b64_string

# Possession chart
@app.route('/chart/possession')
def possession_chart():
    labels = ['Team A', 'Team B']
    sizes = [football_data['possession']['Team A'], football_data['possession']['Team B']]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#3498db', '#e74c3c'])
    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle
    return jsonify(chart=create_chart(fig))

# Shots on target chart
@app.route('/chart/shots_on_target')
def shots_on_target_chart():
    teams = ['Team A', 'Team B']
    shots = [football_data['shots_on_target']['Team A'], football_data['shots_on_target']['Team B']]
    fig, ax = plt.subplots()
    ax.bar(teams, shots, color=['#3498db', '#e74c3c'])
    ax.set_ylabel('Shots on Target')
    ax.set_title('Shots on Target by Team')
    return jsonify(chart=create_chart(fig))

# Goals over time chart
@app.route('/chart/goals_timeline')
def goals_timeline_chart():
    time_points = np.array([15, 30, 45, 60, 75, 90])
    goals_team_a = np.array([0, 1, 1, 2, 2, 2])
    goals_team_b = np.array([0, 0, 1, 2, 3, 3])
    
    fig, ax = plt.subplots()
    ax.plot(time_points, goals_team_a, label='Team A', color='#3498db', marker='o')
    ax.plot(time_points, goals_team_b, label='Team B', color='#e74c3c', marker='o')
    ax.set_xlabel('Time (minutes)')
    ax.set_ylabel('Goals')
    ax.set_title('Goals Scored Over Time')
    ax.legend()
    
    return jsonify(chart=create_chart(fig))

# Passing accuracy chart
@app.route('/chart/passing_accuracy')
def passing_accuracy_chart():
    teams = ['Team A', 'Team B']
    accuracy = [football_data['passing_accuracy']['Team A'], football_data['passing_accuracy']['Team B']]
    
    fig, ax = plt.subplots()
    ax.bar(teams, accuracy, color=['#3498db', '#e74c3c'])
    ax.set_ylabel('Passing Accuracy (%)')
    ax.set_title('Passing Accuracy by Team')
    
    return jsonify(chart=create_chart(fig))

if __name__ == '__main__':
    app.run(debug=True)
