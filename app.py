from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'susp2026'

@app.route('/')
def home():
    return "SU-SP 2.0 Running"

if __name__ == "__main__":
    app.run(debug=True)