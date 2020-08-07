import os
import sys
import uuid
from configparser import ConfigParser

from qiniu import Auth, put_file


class QiniuManger(object):
    
    # 单例模式
    instance = None
    config_parser = ConfigParser()
    config_parser.read('./conf/config.cfg')
    config = config_parser['qiniu']

    def __init__(self, file_path, key):
        self.file_path = file_path
        self.key = key
        self.access_key = self.config['access_key']
        self.secret_key = self.config['secret_key']
        self.bucket = self.config['bucket']
        self.domain = self.config['domain']
        self.q = Auth(self.access_key, self.secret_key)

    def upload_file(self):
        token = self.q.upload_token(self.bucket, self.key, 60 * 60)
        try:
            put_file(token, self.key, file_path)
        except Exception as e:
            print('>>>', e)
            return

        choice = input('>>>文件上传成功请选择你想要的图片返回格式(默认返回 http 格式)🚀:\n1. 返回 http 格式链接🔗\n2. 返回Markdown格式链接🔗\n')
        file_url = os.path.join(self.domain, self.key)
        if choice and int(choice) == 2:
            markdown_format_url = '![{0}][{1}]'.format(self.key, file_url)
            print(markdown_format_url)
        else:
            print(file_url)

def validate_args(arg):
    if len(args) < 2:
        raise '请输入有效的图片文件夹地址'
    file_path = args[1]
    res = os.path.exists(file_path)
    if not res:
        raise '当前输入的文件不存在，请确认后在重新输入'
    return file_path

def get_hash_name(file_path):
    filename = os.path.basename(file_path)
    random_str = uuid.uuid4().hex[:8]
    ext = os.path.splitext(filename)[1]
    return random_str + ext

if __name__ == "__main__":
    args = sys.argv
    file_path = validate_args(args)
    random_name = get_hash_name(file_path)
    qiniu = QiniuManger(file_path, random_name)
    qiniu.upload_file()
