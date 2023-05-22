from scipy.optimize import minimize_scalar
import math

# 目标函数
def f(x):
    return math.sin(2 * math.pi * x / 1440)

# 在区间[0, 2]内寻找最小值
res = minimize_scalar(f, bounds=(720, 1240), method='bounded')

# 输出结果
print("最小值为：", res.fun)
print("最小值出现在x=", res.x)

