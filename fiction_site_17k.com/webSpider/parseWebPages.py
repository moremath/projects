from lxml import html
from config import root,novelsType
from utils import log
from dbModel import DB
import os


def parseHTML(tree,novel):
    pattern_link = '/html/body/div[4]/div[3]/div[2]/table/tbody/tr/td[3]/span/a/@href'
    pattern_name = '/html/body/div[4]/div[3]/div[2]/table/tbody/tr/td[3]/span/a/text()'
    # /html/body/div[4]/div[3]/div[2]/table/tbody/tr[3]/td[3]/span/a

    # /html/body/div[4]/div[3]/div[2]/table/tbody/tr[2]/td[2]/a
    pattern_type = '/html/body/div[4]/div[3]/div[2]/table/tbody/tr/td[2]/a/text()'
    pattern_type_link = '/html/body/div[4]/div[3]/div[2]/table/tbody/tr/td[2]/a/@href'

    pattern_words = '/html/body/div[4]/div[3]/div[2]/table/tbody/tr/td[5]/text()'
    pattern_author = '/html/body/div[4]/div[3]/div[2]/table/tbody/tr/td[6]/a/text()'
    # tree=html.fromstring(text)
    # log(root)( '==\n',tree.xpath(pattern_link),'==\n',tree.xpath(pattern_name),'\n',tree.xpath(pattern_type_link))
    #  ['\n                        ', '\n            \n            \n            \n            \n            \n            ', '\n\n                        ', '\n            \n                        ', '\n            \n                        ', '\n            \n                        ', '\n            \n            ...\n\n                        ', '\n            \n            共 65 页 ', '\n            ', '\n        ']
    pattern_pages = '/html/body/div[4]/div[3]/div[3]/text()'
    # es=tree.xpath('//*[id="text"]')
    # es=tree.xpath(p)
    cls = dict()
    for link,name in zip(tree.xpath(pattern_type_link), tree.xpath(pattern_type)):
        if name not in cls:
            cls[name]= [1,{link}]
        else:
            cls[name][0] += 1
            cls[name][1].add(link)
    return [
        cls,
        zip(
            [novel] * 30,
            tree.xpath(pattern_type),
            tree.xpath(pattern_name),
            [e.rsplit('/', 1)[1].split('.', 1)[0] for e in tree.xpath(pattern_link)],
            tree.xpath(pattern_words),
            tree.xpath(pattern_author),
        )
    ]



if __name__ == '__main__':
    # it takes 8min to run on my machine
    root = '/media/linf/Free/17k'
    type_info=dict()
    db = DB(root+'/novel.sqlite')
    sql = '''
        INSERT INTO
            `book` (`type`,`subtype`,`name`,`bookid`,`words`,`author`)
        VALUES 
            (?,?,?,?,?,?);
        '''
    for novel in novelsType:
        log()('Enter:',novel)
        type_info[novel]=dict()
        d = root + '/' + novel
        for f in os.listdir(d):
            path = d+'/'+f
            with open(path) as f1:
                text = f1.read()
            tree = html.fromstring(text)
            info,sqls = parseHTML(tree,novel)
            for k in info:
                if k not in type_info[novel]:
                    type_info[novel][k]=info[k]
                else:
                    type_info[novel][k][0] += info[k][0]
                    type_info[novel][k][1] = type_info[novel][k][1] | info[k][1]
            for cmd in sqls:
                db.run(sql,cmd)
        db.commit()
    db.close()
    print(type_info)


