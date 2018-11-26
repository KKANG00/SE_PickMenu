from flask import Flask, render_template

app = Flask(__name__)

#식사방법정하기 화면(메인화면)
@app.route("/")
def main():
    return render_template('howToEat.html')

if __name__ == "__main__" :
    app.run()
