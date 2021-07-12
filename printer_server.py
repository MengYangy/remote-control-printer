from flask import Flask, request, jsonify
import win32print, tempfile, win32api
import os, socket, time
'''
实现Python控制打印机
'''
app = Flask(__name__)


@app.route('/printer', methods=['POST', 'GET'])
def printer():
    upload_file = request.files['file']
    file_name = upload_file.filename
    save_path = r'F:\printer'
    save_file = os.path.join(save_path, file_name)
    print(save_file )
    if os.path.exists(save_file):
        os.remove(save_file)
    if upload_file:
        upload_file.save(save_file)
        try:
            print_file(save_file)
        except Exception as e:
            return jsonify(Error='打印失败，请检查打印机是否启动，检查文件是否有误;{}'.format(e), result ='None')
        return jsonify(result = '启动打印机，等待打印...', Error ='None')
    else:
        return jsonify(Error='文件传输失败', result ='None')

@app.route('/test_connect', methods=['POST'])
def test_connect():
    return jsonify(status='连接成功')

def print_file(filename):
    open(filename,"r")
    win32api.ShellExecute(
        0,
        "print",
        filename,
        '/d:"%s"' % win32print.GetDefaultPrinter(),
        ".",
        0
    )
    time.sleep(1)
    # win32print.ClosePrinter()


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


if __name__ == '__main__':
    # print_file()
    self_ip = get_host_ip()
    print('请检查客户端连接的IP是否是: {}'.format(self_ip))
    app.run(host='0.0.0.0', port=5001)
