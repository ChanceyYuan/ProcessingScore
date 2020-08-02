'''打开excel文件，对文件进行数据清洗，增加总分列，以及通过总分列进行判断总成绩级别（优秀，良好，一般）'''



import pandas as pd

#打开excel文件
df = pd.read_excel(r'F:\python_work\ProcessingScore\rz.xlsx')         
#查看文件 
print(df.shape)             
print(df)
 #删除相同的数据
df = df.drop_duplicates('学号')          
#填充空数据
df = df.fillna(0)           
#将作弊和缺考的填充为0
df = df.replace(['作弊','缺考'],0)         
#转换为str类型,去除两边空格
a1 = list(df.columns)
df[a1]= df[a1].astype(str)         
for i in a1:
    df[i] = df[i].str.strip()           
#部分数据转化为int类型
b1 = ['英语','体育','军训','数分','高代','解几']
df[b1] = df[b1].astype(int)            
#保存一份副本，下一个问题需要用到
df1 = df.copy()             
#总分score
score = ['英语','体育','军训','数分','高代','解几']         
df['score'] = df.英语 + df.体育 + df.军训 + df.数分 + df.高代 + df.解几
print(df.score.describe())
#类别判断总分score
bins = [df.score.min()-1,400,450,df.score.max()+1]              
label = ['一般','较好','优秀']
df['类别'] = pd.cut(df.score,bins,right = False,labels = label)

print(df)




'''军训课程分数差异较大，影响总成绩，对各科成绩标准化，再汇总'''


#标准化各科分数
for i in list(df1.columns[4:]):
    df1[i] = (df1[i] - df1[i].min()) / (df1[i].max() - df1[i].min())
#生成score标准化
df1['score标准化'] = df1.英语 + df1.体育 + df1.军训 + df1.数分 + df1.高代 + df1.解几         
print(df1.score标准化.describe())
#生成标准化总分判断
bins1 = [df1.score标准化.min() -1,3,4,df1.score标准化.max()+1]
label1 = label[:]
df1['类别'] = pd.cut(df1.score标准化,bins1,right = False,labels = label1)
print(df1)



'''导出excel'''

writer = pd.ExcelWriter('F:\python_work\ProcessingScore\\001.xlsx')

df.to_excel(writer,sheet_name='sheet1')
df1.to_excel(writer,sheet_name='sheet2')

writer.save()
