import time
import threading

def sub(i):
  print('子线程开始...')
  time.sleep(1)
  print(i)
  print('子线程结束！')

def main():
  print('主线程开始...')
  start = time.time()
  #使用线程
  for i in range(5): #开启5个线程
    # 第一个参数target是线程调用函数，第二个参数args是一个数组变量，用于给worker函数传参，有几个参数就写几个，用","分割，最后的逗号不能少，少了就不是数组了，就会出错。
    th = threading.Thread(target=sub, args=(i,))
    '''
    若setDaemon()的参数为True，主线程结束且子线程尚未结束，则子线程也一并结束；
    若setDaemon()的参数为False(默认值)，主线程结束且子线程尚未结束，则子线程继续执行。
    注意：
    setDaemon()必须设置在start()之前才有效。
    '''
    th.setDaemon(True)
    th.start()
    end = time.time()
  print("总运行时长：%s秒" % (end-start))
  print('主线程结束！')

if __name__ == "__main__":
  main()
