
# here put the import lib
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import ticker
import numpy as np

size1 = 10.5
mpl.rcParams.update(
{
'text.usetex': False,
'font.family': 'stixgeneral',
'mathtext.fontset': 'stix',
"font.family":'serif',
"font.size": size1,
"font.serif": ['Times New Roman'],
}
)
fontdict = {'weight': 'bold','size':size1,'family':'SimSun'}
fig,[ax1,ax2,ax3] = plt.subplots(1,3,figsize = (6,2))
for ax in [ax1,ax2,ax3]:
    ax.tick_params(axis='both',which='both',direction='out')
    ax.set_xticks(np.arange(-5,6,2))
    ax.set_ylim(-5000,5000)
    ax.set_xlim(-5,5)
    ax.plot(np.arange(-5,6),np.arange(-5,6)*1000)

ax1.set_title('实验组',fontdict = fontdict)
ax2.set_title('对照组',fontdict = fontdict)
ax3.set_title('空白组',fontdict = fontdict)

# 实验组
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True) 
formatter.set_powerlimits((0,0)) 
ax1.yaxis.set_major_formatter(formatter)
# 对照组
ax2.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
# 空白组

plt.tight_layout()
plt.savefig('demo1.png',dpi = 600)
plt.show()
