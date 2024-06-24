import numpy as np
import matplotlib.pyplot as plt

# 网格和时间步长
Nx, Ny = 200, 200
dx, dy = 1.0, 1.0
dt = 0.01

# 初始化相场变量 φ 和温度场 T
phi = np.zeros((Nx, Ny))
T = np.zeros((Nx, Ny))

# 初始条件：中心处有一个小冰核
phi[Nx // 2, Ny // 2] = 1.0
T[:, :] = -1.0  # 低于冰点的初始温度

# 定义参数
L = 1.0
epsilon = 1.0
T_m = 273.15  # 冰的熔点（K）
k = 0.1  # 热导率
M = 1.0  # 成分的移动性


# 定义插值函数 h(φ)
def h(phi):
    return phi ** 3 * (6 * phi ** 2 - 15 * phi + 10)


# 各向异性函数
def anisotropy(phi, i, j):
    theta = np.arctan2(j - Ny // 2, i - Nx // 2)
    return 1 + 0.1 * np.cos(6 * theta)


# 定义自由能密度 f(φ, T)
def free_energy_density(phi, T):
    G_ice = -10 * (phi - 1) ** 2  # 冰的自由能
    G_water = -10 * phi ** 2  # 水的自由能
    return h(phi) * G_ice + (1 - h(phi)) * G_water


# 更新相场变量 φ
def update_phi(phi, T, L, epsilon, dt, dx, dy):
    phi_new = phi.copy()
    for i in range(1, Nx - 1):
        for j in range(1, Ny - 1):
            d2phi_dx2 = (phi[i + 1, j] - 2 * phi[i, j] + phi[i - 1, j]) / dx ** 2
            d2phi_dy2 = (phi[i, j + 1] - 2 * phi[i, j] + phi[i, j - 1]) / dy ** 2
            laplacian_phi = d2phi_dx2 + d2phi_dy2

            f_phi = free_energy_density(phi[i, j], T[i, j])
            anisotropy_factor = anisotropy(phi, i, j)
            dF_dphi = f_phi - (epsilon * anisotropy_factor) ** 2 * laplacian_phi

            phi_new[i, j] = phi[i, j] - dt * L * dF_dphi
    return phi_new


# 更新温度场 T
def update_temperature(T, phi, k, dt, dx, dy):
    T_new = T.copy()
    for i in range(1, Nx - 1):
        for j in range(1, Ny - 1):
            d2T_dx2 = (T[i + 1, j] - 2 * T[i, j] + T[i - 1, j]) / dx ** 2
            d2T_dy2 = (T[i, j + 1] - 2 * T[i, j] + T[i, j - 1]) / dy ** 2
            T_new[i, j] = T[i, j] + dt * k * (d2T_dx2 + d2T_dy2)
    return T_new


# 迭代求解
num_steps = 3000
for step in range(num_steps):
    print(step)
    phi = update_phi(phi, T, L, epsilon, dt, dx, dy)
    T = update_temperature(T, phi, k, dt, dx, dy)

    # 可视化每100步的结果
    if step % 300 == 0:
        plt.figure(figsize=(10, 5))
        plt.imshow(phi, cmap='coolwarm')
        plt.title(f'Step {step}: Phase Field φ')
        plt.colorbar()
        plt.show()
