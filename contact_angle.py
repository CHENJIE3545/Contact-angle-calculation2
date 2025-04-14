import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# 读取图像（替换为你的图像路径）
image_path = 'C:/Users/chenj/Desktop/Python/YWNW/new_test/RUN6-368K-500bar.png'
image = plt.imread(image_path)

# 全局变量存储点和结果
points = []
circle_center = None
radius = None
ca_left = None
ca_right = None

# 创建图形和轴
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(bottom=0.2)
ax.imshow(image)
ax.set_title('点击选取3个点，然后点击“计算”按钮')

# 计算圆的函数
def calculate_circle():
    global circle_center, radius, ca_left, ca_right
    
    if len(points) < 3:
        print("需要至少3个点！")
        return
    
    # 提取点的坐标
    x1, y1 = points[0]
    x2, y2 = points[1]
    x3, y3 = points[2]
    
    # 构造线性方程组 A * [a; b] = B
    A = np.array([
        [x1 - x2, y1 - y2],
        [x3 - x2, y3 - y2]
    ])
    B = np.array([
        (x1**2 - x2**2 + y1**2 - y2**2),
        (x3**2 - x2**2 + y3**2 - y2**2)
    ])
    
    # 解方程组求圆心 (a, b)
    ab = np.linalg.solve(A, B)
    a = ab[0] / 2
    b = ab[1] / 2
    circle_center = (a, b)
    
    # 计算半径
    radius = np.sqrt((x1 - a)**2 + (y1 - b)**2)
    
    # 计算角度（转换为度数）
    ca_left = 90 - np.arcsin((circle_center[1] - y1) / radius) * 180 / np.pi
    ca_right = 90 - np.arcsin((circle_center[1] - y2) / radius) * 180 / np.pi
    
    # 绘制圆
    theta = np.linspace(0, 2 * np.pi, 360)
    circle_x = circle_center[0] + radius * np.cos(theta)
    circle_y = circle_center[1] + radius * np.sin(theta)
    ax.plot(circle_x, circle_y, 'r-', linewidth=3)
    
    # 绘制两点间的线段
    ax.plot([x1, x2], [y1, y2], 'r-', linewidth=3)
    
    # 显示结果
    print(f"圆心坐标: ({circle_center[0]:.2f}, {circle_center[1]:.2f})")
    print(f"半径: {radius:.2f}")
    print(f"左角度: {ca_left:.2f}°")
    print(f"右角度: {ca_right:.2f}°")
    
    plt.draw()

# 点击事件处理函数
def onclick(event):
    if event.inaxes != ax:
        return
    
    # 添加点
    x, y = event.xdata, event.ydata
    points.append((x, y))
    ax.plot(x, y, 'ro', markersize=5)
    
    # 显示点的坐标
    print(f"选取点 {len(points)}: ({x:.2f}, {y:.2f})")
    
    # 如果选了3个点，自动计算
    if len(points) == 3:
        calculate_circle()

# 按钮回调函数
def on_calculate(event):
    calculate_circle()

# 添加计算按钮
button_ax = plt.axes([0.4, 0.05, 0.2, 0.075])
button = Button(button_ax, '计算')
button.on_clicked(on_calculate)

# 绑定点击事件
fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()