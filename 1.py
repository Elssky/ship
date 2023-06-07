import matplotlib.pyplot as plt
import numpy as np

# 创建一个图像和颜色条
fig, ax = plt.subplots()
image = ax.imshow(np.random.random((10, 10)), cmap='viridis')
colorbar = plt.colorbar(image)

# 设置颜色条的标签
colorbar.set_label('m')

# 显示图像和颜色条
plt.show()
