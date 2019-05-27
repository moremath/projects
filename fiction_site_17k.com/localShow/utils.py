from config import *
import random
import time,os,requests


def random_user_agent():
    print(random.choice(user_agents) )
    return random.choice(user_agents)


def random_break():
    t= 0.3+ random.random()*0.7
    print('have a break ',t)
    time.sleep(t)



root = root
def _save(d,name,text):
    path = root+ d
    if not os.path.exists(path):
        os.mkdir(path)
        log(root)('mkdir:' ,path)
    with open(path+'/'+name,'w') as f:
        f.write(text)


def savePage(d,url):
    headers = {'User-Agent': random_user_agent()}
    text = requests.get(url=url, headers=headers).text
    _save(d, url.rsplit('/', 1)[-1], text)
    return text


def dt():
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    return dt

def log(dir_name=root):
    def f(*args, **kwargs):
        path = dir_name + '/{}.log'.format(dt())
        with open(path, 'a', encoding='utf-8') as f:
            print(dt(), *args, **kwargs)
            print(dt(), *args, file=f, **kwargs)
    return f