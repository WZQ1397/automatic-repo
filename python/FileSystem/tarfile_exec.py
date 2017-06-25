#python tar

import os
import tarfile
'''
    python中的tarfile模块实现文档的归档压缩和解压缩
    
    功能：
        把工作空间下面的所有文件，打包生成一个tar文件
        同时提供一个方法把该tar文件中的一些文件解压缩到
        指定的目录中
'''
#global var
SHOW_LOG = True
#tar文件存放位置
TAR_PATH = ''
#取出文件存放目录
EXT_PATH = ''

def write_tar_file(path, content):
    '''打开指定path的tar格式的文件，如果该文件不存在
    系统会自动创建该文件，如果该文件以及存在，则打开文件
    打开文件后，向文件中添加文件(这个功能类似于把几个文件
    打包成tar包文件)'''
    with tarfile.open(path, 'w') as tar:
        if SHOW_LOG:
            print('打开文件:[{}]'.format(path))
        for n in content:
            if SHOW_LOG:
                print('压缩文件:[{}]'.format(n))
            tar.add(n)
        if SHOW_LOG:
            print('关闭文件[{}]'.format(path))
        tar.close()
        
def get_workspace_files():
    '''获取工作空间下面的所有文件，然后以列表的形式返回'''
    if  SHOW_LOG:
        print('获取工作空间下的所有文件...')
    return os.listdir('./')

def extract_files(tar_path, ext_path, ext_name):
    '''解压tar文件中的部分文件到指定目录中'''
    with tarfile.open(tar_path) as tar:
        if SHOW_LOG:
            print('打开文件:[{}]'.format(tar_path))
        names = tar.getnames()
        if SHOW_LOG:
            print('获取到所有文件名称:{}'.format(names))
        for name in names:
            if name.split('.')[-1] == ext_name:
                if SHOW_LOG:
                    print('提取文件：[{}]'.format(name))
                tar.extract(name, path = ext_path)

def mkdir(path):
    '''创建不存在的目录'''
    if os.path.exists(path):
        if SHOW_LOG:
            print('存在目录:[{}]'.format(path))
    else:
        if SHOW_LOG:
            print('创建目录:[{}]'.format(path))
        os.mkdir(path)

def init():
    global SHOW_LOG
    SHOW_LOG = True
    #tar文件存放位置
    global TAR_PATH
    TAR_PATH = 'c:\\test\\hongten.tar'
    #取出文件存放目录
    global EXT_PATH
    EXT_PATH = 'c:\\test\\temp'
    #创建目录，如果目录不存在
    path = os.path.split(TAR_PATH)[0]
    mkdir(path)
    mkdir(EXT_PATH)
    
def main():
    init()
    content = get_workspace_files()
    #打包文件
    write_tar_file(TAR_PATH, content)
    print('#' * 50)
    #提取文件
    extract_files(TAR_PATH, EXT_PATH, 'html')
        

if __name__ == '__main__':
    main()
