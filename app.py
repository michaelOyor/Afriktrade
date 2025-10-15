from flask import Flask, render_template

app = Flask(__name__)

# Hardcoded exchange rates (1 foreign unit to NGN, approx. Sep 2025)
exchange_rates = [
    {"currency": "USD (US Dollar)", "rate": 1508},
    {"currency": "CNY (Chinese Yuan)", "rate": 215},
    {"currency": "JPY (Japanese Yen)", "rate": 10.4},
    {"currency": "KRW (South Korean Won)", "rate": 1.1},
    {"currency": "INR (Indian Rupee)", "rate": 17.2},
    {"currency": "SGD (Singapore Dollar)", "rate": 1195},
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/why-partner')
def why_partner():
    return render_template('why_partner.html')

@app.route('/strategic-goals')
def strategic_goals():
    return render_template('strategic_goals.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/currencies')
def currencies():
    return render_template('currencies.html', rates=exchange_rates)

if __name__ == '__main__':
    app.run(debug=True)