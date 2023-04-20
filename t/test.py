import matplotlib.pylab as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

index = 0
scale = 0.0

nrows = 3
ncols = 3
fig = plt.figure()

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题
for _ in range(nrows):
    for _ in range(ncols):
        index += 1

        # 正确率
        scale += 0.01
        xs = np.random.normal(0.9, scale, size=1000)
        ax: plt.Axes = fig.add_subplot(nrows, ncols, index)  # type: ignore
        ax.set_title(f'scale {scale:.3f}')
        ax.hist(xs, 50, (0, 1), weights=[1 / len(xs)] * len(xs))
        ax.set_xlim(0, 1)
        ax.set_xticks(np.arange(0, 1.1, 0.1))
        formatter = FuncFormatter(lambda y, p: f'{y:.1%}')
        ax.yaxis.set_major_formatter(formatter)
        ax.set_xlabel('正确率')
        ax.set_ylabel('概率')

        # 答题时间
        # scale += 0.2
        # xs = np.random.normal(10, scale, size=1000)
        # ax: plt.Axes = fig.add_subplot(nrows, ncols, index)  # type: ignore
        # ax.set_title(f'scale {scale:.3f}')
        # ax.hist(xs, 30, (0, 30), weights=[1 / len(xs)] * len(xs))
        # ax.set_xlim(0, 30)
        # ax.set_xticks(np.arange(0, 31, 5))
        # formatter = FuncFormatter(lambda y, p: f'{100*y:.1f}%')
        # ax.yaxis.set_major_formatter(formatter)

plt.show()
