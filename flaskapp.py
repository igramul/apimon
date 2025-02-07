from flask import Flask, jsonify

import version

app = Flask(__name__)


@app.route('/')
def get_root():
    return jsonify({
        'name': 'apimon',
        'version': version.version,
    })


if __name__ == '__main__':
    app.run()
