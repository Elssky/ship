import pandas as pd

# 读取excel文件
df = pd.read_excel('real_port.xlsx', header=None)

# 将第二列的浮点数转化为整数

# 保留前三列
df = df.iloc[:, :3]

# 将数据转换成用','分割的txt文本
df.to_csv('real_port.txt', sep=',', index=False, header=False)

# 输出转换后的DataFrame
print(df)