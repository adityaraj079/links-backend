from flask import Flask, redirect, url_for, render_template
# WSGI Application
app=Flask(__name__)

@app.route('/')  #Decorator (which comes with function)
def welcome():
    return 'HI'

@app.route('/success/<int:score>')
def success(score):
    return "Passed with "+str(score)

@app.route('/fail/<int:score>')
def fail(score):
    return "Failed with "+str(score)

if __name__=='__main__':
    app.run(debug=True)