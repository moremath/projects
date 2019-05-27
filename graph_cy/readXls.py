import xlrd


path = '/media/linf/Free/Book1.xlsx'
workbook = xlrd.open_workbook(path)
workbook = xlrd.open_workbook(path)
print([e for e in dir(workbook) if 'close' in e])
# sheet2_name = workbook.sheet_names() # 获取所有sheet名称

# 根据sheet索引或者名称获取sheet内容
sheet1 = workbook.sheet_by_index(0) # sheet索引从0开始
# sheet1 = workbook.sheet_by_name('sheet2')
# sheet1的名称，行数，列数
print(sheet1.name, sheet1.nrows, sheet1.ncols)
# 获取整行和整列的值（数组）
rows = sheet1.row_values(1) # 获取第三行内容
rows2 = sheet1.row_values(1) # 获取第三行内容
cols = sheet1.col_values(0) # 获取第1列内容
print([e for e in dir(sheet1) if 'cell' in e ])

print( 'rows',rows)
print( 'rows',rows2)
print('cols',cols)
# 获取单元格内容
# print(sheet1.cell(1, 0).value.encode('utf-8'))
# print(sheet1.cell_value(1, 0).encode('utf-8'))
# print(sheet1.row(2)[0].value.encode('utf-8'))
# # 获取单元格内容的数据类型
# print(sheet1.cell(2, 0).ctype)
# print(sheet1.cell(2, 0).ctype)

