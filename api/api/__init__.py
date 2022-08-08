from flask import Flask

# Buat object Flask
app = Flask(__name__, template_folder="templates", instance_relative_config=True)
