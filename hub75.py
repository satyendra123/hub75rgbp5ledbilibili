"""
说明: Hub75全彩屏显示程序
版本: V1.0
作者: 王铭东
编程语言: MicroPython
官网: www.itprojects.cn
"""

from machine import Pin, SoftSPI, freq
from utime import sleep_us

#freq(160000000)  # default NodeMCU ESP-32S v1.1
freq(240000000)


class Hub75SpiConfiguration:
    """
    配置HUB75 RGB LED矩阵的SoftSPI
    """

    def __init__(self):
        self.spi_baud_rate = 240000000

        self.illumination_time_microseconds = 1

        # 行，引脚的配置，因为是32扫，所以2^5=32，需要接5个引脚ABCDE
        self.line_select_a_pin_number = 32
        self.line_select_b_pin_number = 33
        self.line_select_c_pin_number = 21
        self.line_select_d_pin_number = 15
        self.line_select_e_pin_number = 12

        """
        # 数据引脚(方式1)
        self.red1_pin_number = 27
        self.blue1_pin_number = 26
        self.green1_pin_number = 25
        self.red2_pin_number = 13
        self.blue2_pin_number = 17
        self.green2_pin_number = 14
        
        """
        # 数据引脚(方式2)
        self.red1_pin_number = 25
        self.blue1_pin_number = 27
        self.green1_pin_number = 26
        self.red2_pin_number = 14
        self.blue2_pin_number = 13
        self.green2_pin_number = 17
        
        

        # 时钟引脚
        self.clock_pin_number = 16
        self.latch_pin_number = 4
        # 使能引脚（低电平）
        self.output_enable_pin_number = 22

        # 未连接
        self.spi_miso_pin_number = 35


class Hub75Spi:
    """
    HUB75 RGB LED 驱动显示
    """

    def __init__(self, matrix_data, config):
        self.config = config
        self.matrix_data = matrix_data
        self.half_row_size = matrix_data.row_size // 2

        # 创建ABCDE以及使能等引脚对象
        self.latch_pin = Pin(config.latch_pin_number, Pin.OUT)
        self.output_enable_pin = Pin(config.output_enable_pin_number, Pin.OUT)
        self.line_select_a_pin = Pin(config.line_select_a_pin_number, Pin.OUT)
        self.line_select_b_pin = Pin(config.line_select_b_pin_number, Pin.OUT)
        self.line_select_c_pin = Pin(config.line_select_c_pin_number, Pin.OUT)
        self.line_select_d_pin = Pin(config.line_select_d_pin_number, Pin.OUT)
        self.line_select_e_pin = Pin(config.line_select_e_pin_number, Pin.OUT)

        # 默认让不选中任何行
        self.line_select_a_pin.off()
        self.line_select_b_pin.off()
        self.line_select_c_pin.off()
        self.line_select_d_pin.off()
        self.line_select_e_pin.off()

        # 创建RGB引脚对象
        self.red1_mosi_pin = Pin(config.red1_pin_number)
        self.red2_mosi_pin = Pin(config.red2_pin_number)
        self.green1_mosi_pin = Pin(config.green1_pin_number)
        self.green2_mosi_pin = Pin(config.green2_pin_number)
        self.blue1_mosi_pin = Pin(config.blue1_pin_number)
        self.blue2_mosi_pin = Pin(config.blue2_pin_number)

        # 创建RGB对应的SPI对象
        self.red1_spi = SoftSPI(baudrate=config.spi_baud_rate, polarity=1, phase=0, sck=Pin(config.clock_pin_number), mosi=self.red1_mosi_pin, miso=Pin(config.spi_miso_pin_number))
        self.red2_spi = SoftSPI(baudrate=config.spi_baud_rate, polarity=1, phase=0, sck=Pin(config.clock_pin_number), mosi=self.red2_mosi_pin, miso=Pin(config.spi_miso_pin_number))
        self.green1_spi = SoftSPI(baudrate=config.spi_baud_rate, polarity=1, phase=0, sck=Pin(config.clock_pin_number), mosi=self.green1_mosi_pin, miso=Pin(config.spi_miso_pin_number))
        self.green2_spi = SoftSPI(baudrate=config.spi_baud_rate, polarity=1, phase=0, sck=Pin(config.clock_pin_number), mosi=self.green2_mosi_pin, miso=Pin(config.spi_miso_pin_number))
        self.blue1_spi = SoftSPI(baudrate=config.spi_baud_rate, polarity=1, phase=0, sck=Pin(config.clock_pin_number), mosi=self.blue1_mosi_pin, miso=Pin(config.spi_miso_pin_number))
        self.blue2_spi = SoftSPI(baudrate=config.spi_baud_rate, polarity=1, phase=0, sck=Pin(config.clock_pin_number), mosi=self.blue2_mosi_pin, miso=Pin(config.spi_miso_pin_number))

    def display_data(self):
        
        for row in range(self.matrix_data.row_size):
            
            if row < self.half_row_size:
                # shift in data
                row_data = self.matrix_data.red_matrix_data[row]
                # print(row, row_data)
                self.red1_spi.write(row_data)
                self.red1_mosi_pin.off()
                self.output_enable_pin.on() # disable

                self.line_select_a_pin.value(row & 1)
                self.line_select_b_pin.value(row & 2)
                self.line_select_c_pin.value(row & 4)
                self.line_select_d_pin.value(row & 8)
                self.line_select_e_pin.value(row & 16)

                self.latch_pin.on()
                self.latch_pin.off()
                self.output_enable_pin.off() # enable
                sleep_us(self.config.illumination_time_microseconds)

                # shift in data
                row_data = self.matrix_data.green_matrix_data[row]
                self.green1_spi.write(row_data)
                self.green1_mosi_pin.off()
                self.output_enable_pin.on() # disable
                self.latch_pin.on()
                self.latch_pin.off()
                self.output_enable_pin.off() # enable
                sleep_us(self.config.illumination_time_microseconds)

                # shift in data
                row_data = self.matrix_data.blue_matrix_data[row]
                self.blue1_spi.write(row_data)
                self.blue1_mosi_pin.off()
                self.output_enable_pin.on() # disable
                self.latch_pin.on()
                self.latch_pin.off()
                self.output_enable_pin.off() # enable
                sleep_us(self.config.illumination_time_microseconds)

            else:
                
                # shift in data
                row_data = self.matrix_data.red_matrix_data[row]
                self.red2_spi.write(row_data)
                self.red2_mosi_pin.off()
                self.output_enable_pin.on() # disable

                self.line_select_a_pin.value(row & 1)
                self.line_select_b_pin.value(row & 2)
                self.line_select_c_pin.value(row & 4)
                self.line_select_d_pin.value(row & 8)
                self.line_select_e_pin.value(row & 16)

                self.latch_pin.on()
                self.latch_pin.off()
                self.output_enable_pin.off() # enable
                sleep_us(self.config.illumination_time_microseconds)

                row_data = self.matrix_data.green_matrix_data[row]
                self.green2_spi.write(row_data)
                self.green2_mosi_pin.off()
                self.output_enable_pin.on() # disable
                self.latch_pin.on()
                self.latch_pin.off()
                self.output_enable_pin.off() # enable
                sleep_us(self.config.illumination_time_microseconds)

                row_data = self.matrix_data.blue_matrix_data[row]
                self.blue2_spi.write(row_data)
                self.blue2_mosi_pin.off()
                self.output_enable_pin.on() # disable
                self.latch_pin.on()
                self.latch_pin.off()
                self.output_enable_pin.off() # enable
                sleep_us(self.config.illumination_time_microseconds)

        #Flush out last blue line
        self.blue2_spi.write(bytearray(8))
        self.output_enable_pin.on()
        self.latch_pin.on()
        self.latch_pin.off()

