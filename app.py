from flask import Flask, request, jsonify

app = Flask(__name__)

ALLOWED_EMAILS = {
    'gcptrail0@gmail.com',
    'pravinrajagcp@gmail.com',
    'parthibank72@gmail.com',
    'prvnrajh@gmail.com'
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    if email in ALLOWED_EMAILS:
        return jsonify({"message": "Login allowed!", "email": email}), 200
    else:
        return jsonify({"message": "Access denied."}), 403

if __name__ == '__main__':
    app.run(debug=True)
