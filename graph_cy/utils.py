import xlrd
from graph import Graph,sum_user_property


default_xls = './call.xls'
phone_dict=dict()


def rowOfXls(path,rowIndex,sheetIndex=0):
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(sheetIndex)
    return sheet.row_values(rowIndex)

def jsonOfXls(path= default_xls  ):
    workbook = xlrd.open_workbook(path)
    sheet1 = workbook.sheet_by_index(0)
    # titles = sheet1.row_values(0)
    r=dict()
    r['tbody']=[]
    ncols = 0
    max_ncol = 10
    for e in sheet1.row_values(0)[:max_ncol]:
        if e:
            ncols += 1
        else:
            break
    for i in range(1,sheet1.nrows):
        if sheet1.cell(i,0).ctype == 3:
            year,month,day,hour,minite=(xlrd.xldate.xldate_as_tuple(sheet1.cell(i,0).value,0))[:5]
            row_vals =[
                '{}/{}/{} {}:{}'.format(year,month,day,hour,minite)
            ]
        else:
            row_vals = sheet1.cell(i,0).value
        for val in sheet1.row_values(i)[1:ncols]:
            val = str(val).rsplit('.0',1)[0]
            row_vals.append(val)
        r['tbody'].append( row_vals )
        # print([type(e) for e in  sheet1.row_values(i)[:ncols] ])
    # print(r['tbody'])
    r['thead'] = sheet1.row_values(0)[:ncols]
    return r


def jsonOfXlsWithLink(path= default_xls):
    htmlLink= """<a href="/one/{user}" target="_blank">{user}</a>"""
    _data= jsonOfXls(path)
    print('--------_data',_data)
    for row in _data['tbody']:
        Alice = row.pop(2)
        row.insert(2, htmlLink.format(user=Alice) )
        Bob = row.pop(4)
        row.insert(4, htmlLink.format(user=Bob) )
    return _data


def getGraph(path= default_xls ):
    g=Graph()
    chartJson = jsonOfXls(path)
    tbody= chartJson['tbody']
    thead= chartJson['thead']

    # for i,e in enumerate(thead):
    for row in tbody:
        Bob_dict=dict()
        Bob_dict['startTime'] =  [ row[0] ]
        Bob_dict['callSpanTime'] = int(row[5])
        # Bob_dict['cell'] = [row[7] ]
        # Bob_dict['loc'] = [ row[8] ]
        # Alice 主叫姓名，Bob，被叫姓名
        Alice_phone,Alice,Bob_phone,Bob =row[1],row[2],row[3],row[4]
        # 丈夫 / 妻子
        Alice_role, Bob_role = row[6].split('/',1)
        Bob_dict['relationship'] = { Bob_role }
        phone_dict[Bob] = phone_dict.get('phoneNum',set()) |{ Bob_phone }
        g.addLink( Alice,Bob,Bob_dict )
        # bug :shadow copy        
        # property_dict['relationship'] = { Alice_role }
        Alice_dict=dict()
        Alice_dict.update(Bob_dict)
        Alice_dict['relationship'] = { Alice_role }
        phone_dict[Alice] = phone_dict.get('phoneNum',set())|{ Alice_phone }
        g.addLink(Bob,Alice, Alice_dict)

        g[Alice][Bob]['callCount'] = g[Alice][Bob].get('callCount',0) + 1
        # g[Bob][Alice]['callCount'] = g[Bob][Alice].get('callCount',0) + 1
    return g


def graphData(path=default_xls):
    data= getGraph(path).nodes
    _data =dict()
    _data['id_list'] = [ k for k in data]
    _data['link_list'] = list()
    for k,v in data.items():
        for k1,v1 in v.items():
            if 'callCount' not in v1:
                continue
            _data['link_list'].append(
                [k,k1,str(v1['callCount'])]
            )
    return _data


def search_single(user,path=default_xls ):
    _data = getGraph(path).nodes
    if user not in phone_dict:
        return []
    tbody = [
        ['本机号码','/'.join( phone_dict[user])],
        ['联系人总数:',len(_data[user])],
        ['联系人:',' ,'.join([u for u in _data[user] ])],
        ['通话总时长:',str( sum_user_property(_data,user,'callSpanTime'))+'秒'],
        # callCount differs with others,it's single side,it counld be empty,cause keyError
        # ['通话次数:',sum_user_property(_data,user,'callCount')],
        ['主叫次数:',sum(_data[user][u].get('callCount',0) for u in _data[user]) ],
        ['通话记录:',' 和 '.join( set(sum_user_property(_data,user,'startTime') ))],
    ]
    return tbody


def singleGraphData(user,path=default_xls):
    data= getGraph(path).nodes
    _data =dict()
    _data['id_list'] = [ k for k in data[user]] +[user]
    _data['link_list'] = [[user,Bob,data[user][Bob]['callCount']] for Bob in data[user] if 'callCount' in data[user][Bob] ]
    for k,v in data.items():
        if k == user:
            continue
        for k1,v1 in v.items():
            if k1 == user and 'callCount' in v1:
                _data['link_list'].append(
                    [k,k1,str(v1['callCount'])]
                )
    return _data


def read_relationship(path='关系推导.xls'):
    workbook = xlrd.open_workbook(path)
    sheet1 = workbook.sheet_by_index(0)
    sheet2 = workbook.sheet_by_index(1)

    relationship= []
    for i in range(1, sheet1.nrows):
        row_data= sheet1.row_values(i)
        row_data = [e for e in row_data if e]
        relationship.append(row_data)
    for i in range(1, sheet2.nrows):
        row_data= sheet2.row_values(i)
        row_data = [e for e in row_data if e]
        relationship.append(row_data)
    # print(read_relationship())
    return relationship

def search_two(u1,u2,path=default_xls):
    if (u1 not in phone_dict) or (u2 not in phone_dict):
        return "人名{} 或 {} 输入错误".format(u1,u2)
    if u1 == u2:
        return "{} 和 {} 是同一个人啦".format(u1,u2)
    relationship_data = read_relationship()
    g = getGraph(path)
    _data =g.nodes
    for r in g.shortestPath(u1,u2):
        # print('rrrr:',r)
        # print('_data',_data[u1],_data[u2])
        if len(r) == 2:
            return "{} 和 {} 是{}/{}".format(
                u1,u2,*_data[u2][u1]['relationship'],*_data[u1][u2]['relationship'],
            )
        if len(r) in [3,4]:
            relationship_list = list()
            for i in range(1,len(r)):
                relationship_list.append(
                    '{}/{}'.format(
                        *_data[r[i+1]][r[i]]['relationship'],
                        *_data[r[i ]][r[i+1]]['relationship'],
                    )
                )
            if relationship_list in relationship_data:
                return '{} 和 {} 是{}噢'.format(
                    u1,u2,relationship_list[-1]
                )

    return '{} 和 {} 不在同一个人际圈'.format(
        u1,u2
    )

# print(graphData())