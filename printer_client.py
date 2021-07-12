import requests
import base64
import os
import json
import sys, time
from printer_softward import Ui_Form
from PyQt5.Qt import QApplication, QWidget, QFileDialog, QThread, QObject, pyqtSignal, QProcess
from multiprocessing import Process, Pool


class Emit_Str(QObject):
    text_reWrite = pyqtSignal(str)
    def write(self, text):
        self.text_reWrite.emit(str(text))


def printer_client(host, port, file_path):
    # url = "http://192.168.1.118:5001/printer"
    # url = "http://192.168.1.116:5002/printer"
    url = "http://{}:{}/printer".format(host, port)

    # file_path = r'G:\健康.pdf'
    # file_path = file
    print('准备传输文件',file_path)
    if not os.path.exists(file_path):
        print('输入文件不存在')

    file_name = file_path.split('/')[-1]
    file = open(file_path, 'rb')
    # print('***')
    # 拼接参数
    files = {'file': (file_name, file)}

    # 发送post请求到服务器端
    r = requests.post(url, files=files)
    print('传输完成， 等待打印...')
    result = r.content.decode('utf-8')
    my_json = json.loads(result)
    print(json.dumps(my_json, sort_keys=True, indent=4, ensure_ascii=False))


class My_Thread(QThread):
    def __init__(self):
        super(My_Thread, self).__init__()

    def run(self) -> None:
        printer_client(self.ip, self.port, self.file_path)

    def getP(self, ip, port, file_path):
        self.ip = ip
        self.port = port
        self.file_path = file_path


class Main():
    def __init__(self):
        super(Main, self).__init__()
        self.file_name = []
        self.use_thread = True

        app = QApplication(sys.argv)
        form = QWidget()
        form.setFixedSize(435, 430)
        # form.setWindowTitle('远程打印机平台')
        self.w = Ui_Form()
        self.w.setupUi(form)
        sys.stdout = Emit_Str(text_reWrite=self.output_text_write)
        sys.stderr = Emit_Str(text_reWrite=self.output_text_write)
        self.ip = self.w.ip_line.text()
        self.port = self.w.port_line.text()

        self.my_connect()

        form.show()
        sys.exit(app.exec())

    def build(self):
        pass

    def output_text_write(self, text):
        if text != '\n':
            self.w.textEdit.appendPlainText(text)


    def my_connect(self):
        self.w.test_btn.clicked.connect(self.test_connect_func)
        self.w.load_btn.clicked.connect(self.load_files)
        self.w.start_btn.clicked.connect(self.start_func)
        self.w.stop_btn.clicked.connect(self.stop_func)

        self.w.ip_line.textChanged.connect(self.ip_change)
        self.w.port_line.textChanged.connect(self.port_cahnge)

    def test_connect_func(self):
        # print('正在进行通讯连接测试')
        self.w.textEdit.appendPlainText('正在进行通讯连接测试')
        self.test_connect(self.ip, self.port)
        print('完成测试连接')


    def ip_change(self):
        self.ip = self.w.ip_line.text()

    def port_cahnge(self):
        self.port = self.w.port_line.text()

    def load_files(self):
        self.file_name = []
        dialog = QFileDialog()
        file_names = dialog.getOpenFileNames(self.w.load_btn, '选择要打印的文件', '/',
                                             'PDF(*.pdf);;WORD(*.doc *.docx);;EXCEL(*.xlsx *.xls);;'
                                             'PPT(*.ppt *.pptx);;image(*.jpg *.png *.tif);;TXT(*.txt);;'
                                             'CAJ(*.caj);;ALL(*.*)',
                                             'PDF(*.pdf)')

        for i in file_names[0]:
            print('选中的文件有-> {}'.format(i))
            self.file_name.append(i)
        # print(self.file_name)

    def start_func(self):
        if len(self.file_name) == 0:
            print('请选择您要打印的文件')
        else:
            for i in self.file_name:
                printer_client(self.ip, self.port, i)
            self.file_name = []

    def stop_func(self):
        pass


    @staticmethod
    def test_connect(host, port):
        # url = "http://192.168.1.118:5001/test_connect"
        url = "http://{}:{}/test_connect".format(host, port)
        print('测试连接:', url)

        try:
            r = requests.post(url)
            result = r.content.decode('utf-8')
            my_json = json.loads(result)
            print(json.dumps(my_json, sort_keys=True, indent=4, ensure_ascii=False))
        except Exception as e:
            print('连接出错, 错误原因是：{}'.format(e))


if __name__ == '__main__':
    Main()
