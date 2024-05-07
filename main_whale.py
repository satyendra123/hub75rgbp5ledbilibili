"""
说明: Hub75全彩屏显示程序
版本: V1.0
作者: 王铭东
编程语言: MicroPython
官网: www.itprojects.cn
"""

import hub75
import matrixdata
from logo import logo
from whale import SquirtyTheWhale
import time


# 定义屏幕的每行、每列的led个数，其实就是分辨率
ROW_SIZE = 64
COL_SIZE = 64

config = hub75.Hub75SpiConfiguration()
matrix = matrixdata.MatrixData(ROW_SIZE, COL_SIZE)
hub75spi = hub75.Hub75Spi(matrix, config)

# Show Python Logo
matrix.set_pixels(0, 16, logo)

for i in range(500):
    hub75spi.display_data()

# Squirty the whale
squirty = SquirtyTheWhale(matrix, hub75spi)
squirty.run_loop()

