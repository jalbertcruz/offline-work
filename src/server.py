from flask import Flask

app = Flask(__name__, static_folder="./package")

app.run(debug=True, port=80)
