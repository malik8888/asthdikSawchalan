#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import time
import smbus2
adr=0x41
address = 0x68
powermgmt_1=0x6b
powermgmt_2=0x6c


class SHT31(object):

    def __init__(self, unit = 'celsius', bus = 1):
        self.bus = smbus2.SMBus(1)
        self.__unit = unit
        
        
    def read_byte(self):
        return self.bus.read_byte_data(address, adr)
    
    
    def read_word(self):
        high = self.bus.read_byte_data(address, adr)
        low = self.bus.read_byte_data(address, adr+1)
        val = (high << 8) + low
        return val
    
    def read_word_2c(self):
        val = self.read_word()
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val
        
        
    def write_byte(adr, value):
        self.bus.write_byte_data(address, adr, value)

        
    
    def __read_raw(self):
        try:
            #self.bus.write_i2c_block_data(0x44, 0x2C, [0x06])
            time.sleep(0.2)
            data = self.bus.read_i2c_block_data(0x44, 0x00, 6)
            return data
        except IOError:
            print("[SHT31][Error] No sensor found")
            return

    def c_to_f(self, c):
        return c * 9.0 / 5.0 + 32.0

    def get_temperature(self):
        #raw = self.__read_raw()
        #raw_temp = raw[0] * 256 + raw[1]
        #temp_c = round(-45 + (175 * raw_temp / 65535.0), 1)
        #temp_f = round(self.c_to_f(temp_c), 1)
        self.bus.write_byte_data(address,powermgmt_1,0)
        time.sleep(0.2)
        temp=self.read_word_2c()
        t=(temp/340)+36.53

        if self.__unit == 'fahrenheit':
            return temp_f
        else:
            return temp_c

    def get_temperature_string(self):
        return '{} {}'.format(self.get_temperature(), ('','fahrenheit')[self.__unit == 'fahrenheit'])

    def get_humidity(self):
        raw = self.__read_raw()
        humidity = round(100 * (raw[3] * 256 + raw[4]) / 65535.0, 1)

        return humidity

    def get_humidity_string(self):
        return '{}'.format(self.get_humidity())
