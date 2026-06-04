from flask import Flask, request, jsonify

PORT = 5000
app = Flask(__name__)

latest = ""
history = []
UPDATE_INTERVAL = 2000  # in ms

@app.route("/data", methods=["POST"])
def data():
    global latest, history
    latest = str(request.json["value"])
    history.append(latest)
    print("EMPFANGEN:", latest)
    return "ok"

@app.route("/latest")
def latest_data():
    return jsonify(values=history)

@app.route("/")
def index():
    return f"""
    <!doctype html>
    <html lang="de">
      <head>
        <meta charset="utf-8">
        <title>PID Daten</title>
      </head>
      <body>
        <pre id="values"></pre>

        <script>
          async function update() {{
            const response = await fetch('/latest');
            const data = await response.json();
            const output = document.getElementById('values');

            output.textContent = data.values.join('\\n');
            window.scrollTo(0, document.body.scrollHeight);
          }}

          update();
          setInterval(update, {UPDATE_INTERVAL});
        </script>
      </body>
    </html>
    """

app.run(host="0.0.0.0", port=PORT)
