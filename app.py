from flask import Flask, request, jsonify
from screen import screen_stocks

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/screen', methods=['POST'])
def screen():
    data = request.get_json()
    risk = data.get('risk', 'medium')
    goal = data.get('goal', 'growth')
    results = screen_stocks(risk, goal)
    # Ensure numeric types are native float
    for r in results:
        for k, v in list(r.items()):
            if isinstance(v, (float, int)):
                r[k] = float(v)
            elif hasattr(v, 'item'):  # numpy scalar
                r[k] = float(v.item())
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)