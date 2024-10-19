from flask import Flask, jsonify, request
from flask_cors import CORS
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
CORS(app)

# Modified function for actual football analysis data
def football_analysis():
    # Simulated data (this should be replaced by the actual logic of football analysis)
    return {
        'goals_scored': 3,
        'possession': '60%',
        'shots_on_target': 10,
        'passing_accuracy': '85%',
        'tackles_made': 15,
        'corners_taken': 5,
        'fouls_committed': 12
    }

@app.route('/analysis', methods=['GET'])
def get_analysis():
    return jsonify(football_analysis())

# Function to generate chart for football analysis
@app.route('/chart', methods=['GET'])
def get_chart():
    # Simulating chart for goals, shots on target, possession
    fig, ax = plt.subplots()
    ax.bar(['Goals Scored', 'Shots on Target', 'Possession (%)'], [3, 10, 60], color=['blue', 'green', 'red'])

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return jsonify({'chart': plot_url})

if __name__ == '__main__':
    app.run(debug=True)
