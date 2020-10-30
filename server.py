from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
app.secret_key = "SECRET"


@app.route("/")
def show_homepage():
    """Show the application's homepage."""

    return render_template("homepage.html")


if __name__ == "__main__":
  # connect_to_***********
    app.run(debug=True, host='0.0.0.0')