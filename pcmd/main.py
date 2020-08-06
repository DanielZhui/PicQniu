import os
import sys
from configparser import ConfigParser

from qiniu import Auth


class QiniuManger(object):
    
    # 单例模式
    instance = None
    config_parser = ConfigParser()
    config_parser.read('./conf/config.cfg')
    config = config_parser['qiniu']

    def __init__(self, file_path):
        self.file_path = file_path
        self.access_key = self.config['access_key']
        self.secret_key = self.config['secret_key']
        self.bucket = self.config['bucket']
        self.domain = self.config['domain']
        self.q = Auth(self.access_key, self.secret_key)

    def get_file_size(self):
        pass

    def upload_file_qiniu(self):
        pass
    
    @classmethod
    def validate_file(file_path):
        res = os.path.exists(file_path)
        if not res:
            raise '当前输入的文件'
        return res


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        raise '请输入有效的图片文件夹地址'
    file_path = args[1]
    res = os.path.exists(file_path)
    if not res:
        raise '当前输入的文件不存在，请确认后在重新输入'
    print(file_path)
