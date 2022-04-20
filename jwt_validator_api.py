from flask import Flask, request, jsonify

app = Flask('JWT_VALIDATOR')

correct_tokens = ["qwertyuiop", "wqwgwDJSDKLASKA", "KUDYAUDUASDSUDUASY", "SAJDGASKDASHDASJKDHASKASHDJK"]


@app.route('/', methods=['POST'])
def hello():
    data = request.get_json(force=True)
    if data['token'] in correct_tokens:
        return jsonify({"is_valid": True})
    return jsonify({"is_valid": False}), 401


if __name__ == "__main__":
    app.run('0.0.0.0', '5001', debug=True)
