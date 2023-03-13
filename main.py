from flask import Flask, render_template, request, session, redirect, jsonify
import datetime
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

messages = []

@app.route('/', methods=['GET', 'POST'])
def index():
    user_ip = request.remote_addr
    now = datetime.datetime.now()
    dir_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir_path, "logfile.txt"), "a") as file:
        # Write input data and timestamp to file
        file.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')} - {user_ip} - visited index.html \n")
    file_path = os.path.relpath(os.path.join(dir_path, "logfile.txt"))
    print(f"Log file saved at {file_path}.")


    if request.method == 'POST':
        session['name'] = request.form['name']
        if not session['name']:
            return redirect('/')
        return redirect('/chat')
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    user_ip = request.remote_addr
    now = datetime.datetime.now()
    dir_path = os.path.dirname(os.path.abspath(__file__))
    

    name = session.get('name', '')
    if not name:
        return redirect('/')
    
    with open(os.path.join(dir_path, "logfile.txt"), "a") as file:
        # Write input data and timestamp to file
        file.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')} - {user_ip} - NAME:{name} visited chat.html \n")
    file_path = os.path.relpath(os.path.join(dir_path, "logfile.txt"))
    print(f"Log file saved at {file_path}.")
    
    return render_template('chat.html', name=name)

@app.route('/send', methods=['POST'])
def send():
    message = request.form['message']
    messages.append(f"{session['name']}: {message}")
    print(messages)

    user_ip = request.remote_addr
    now = datetime.datetime.now()
    dir_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir_path, "logfile.txt"), "a") as file:
        # Write input data and timestamp to file
        file.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')} - {user_ip} - {messages}")
    file_path = os.path.relpath(os.path.join(dir_path, "logfile.txt"))
    print(f"Log file saved at {file_path}.")

    
    return jsonify(status="OK")

    
    

@app.route('/receive', methods=['GET'])
def receive():
    return jsonify(messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
