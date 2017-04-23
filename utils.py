import time



def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.gua.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)

def format_time(t):
    import time
    format = '%Y-%m-%d %l:%M %p'
    # print(type(t), t)
    value = time.localtime(int(t))
    dt = time.strftime(format, value)
    return dt