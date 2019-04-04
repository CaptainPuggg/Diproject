from flask import Flask, jsonify, request, abort
import json
import os, base64
import ware_calc
from flask import render_template
app = Flask(__name__, static_url_path='')


@app.route('/index', methods=['GET'])
def test_end():
    return app.send_static_file('main.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        base64Str = request.form['data'];
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(basepath, 'static', 'audio.mp3')

        with open(upload_path, 'wb') as fdecode:
            # print(base64Str)
            decode_base64 = base64.b64decode(base64Str[22:])
            fdecode.write(decode_base64)
        # base64.b64decode(strs)

        return json.dumps({"success": True})
    return json.dumps({"success": False})


@app.route('/compare', methods=['POST', 'GET'])
def compare():
    print('compare')
    pic_original, fft_original = ware_calc.calc_ware('./static/original')
    pic_audio, fft_audio = ware_calc.calc_ware('./static/audio')
    l = min(len(fft_original), len(fft_audio))
    same = 0
    for i in range(0,l):
        o_t = fft_original[i]
        a_t = fft_audio[i]
        f = abs(max(o_t, a_t)/min(o_t, a_t))
        if f < 3:
            same = same + 1
    print(same/l)
    return json.dumps({"success": True, "pic_original": "original.png",
                       "pic_audio": "audio.png", "similarity": same/l})


if __name__ == '__main__':
    app.run('127.0.0.1',8800)
