from utils import savePage,novelsType,random_break,log
import time
from lxml import html


if __name__ == '__main__':
    host="http://www.17k.com"
    for novel in novelsType:
        t0=time.time()
        log()('Enter:',novel,'.....')
        homePage = host + novelsType[novel]
        text = savePage(novel,homePage)
        pages=100
        pattern ='/html/body/div[4]/div[3]/div[3]/text()'
        tem = html.fromstring(text).xpath(pattern)
        try:
            pages =[ e.rstrip().split()[1] for e in tem if '页' in e]
            log()('==pages',tem,pages)
            pages=int(pages[0])
        except:
            log()('ERROR in parse',pages)

        for p in range(2, pages+1 ):
            url = homePage.rsplit('_',1)[0]+ '_{}.html'.format(p)
            savePage(novel,url)
            # 对于17k网站非必须
            random_break()

        log()(novel,pages,'页','===done in ',time.time()-t0,'秒')



