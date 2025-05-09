#!/bin/false
# This file is part of Espruino, a JavaScript interpreter for Microcontrollers
#
# Copyright (C) 2013 Gordon Williams <gw@pur3.co.uk>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# ----------------------------------------------------------------------------------------
# This file contains information for a specific board - the available pins, and where LEDs,
# Buttons, and other in-built peripherals are. It is used to build documentation as well
# as various source and header files for Espruino.
# ----------------------------------------------------------------------------------------

# ###########################################################
# #      THIS IS BETA - C3/IDF4 SUPPORT IS NOT READY YET       #
# ###########################################################

# A Note about the 'variables' parameter on ESP32 Builds
# ------------------------------------------------------
#
# For the ESP32 build, the number of JsVars is governed by two factors:
#     * Available memory
#     * Maximum number of JsVars for the used JsVar format
#
# This setting will chose the optimum JsVar format for a given number
# of JsVars.

# If you add PSRAM to your ESP32 or compile with modules removed, you
# may wish to select a value using this table:
#
# Value |  Max JsVars  | Bytes per JsVar | Maximum References |
# ------+--------------+-----------------+--------------------+
# 4095  |         4095 |              13 |               255  |
# 8191  |         8191 |              13 |                15  |
# 16383 |        16383 |              14 |               255  |
# 65535 |        65535 |              16 |               255  |
# ------+--------------+-----------------+--------------------+

# CAUTION: Chosing 8191 only allows 15 references to a variable. This
# may be too restrictive to run some code.

# Using too large a JsVar format may limit how many JsVars can fit into
# available memory. Using too small a JsVar format will under utilise
# available memory.


import pinutils;
info = {
 'name'                     : "CURIO",
 'espruino_page_link'       : 'Curio',
 'default_console'          : "EV_SERIAL1",
 'default_console_baudrate' : "115200",
 'variables'                : 16383, # See note above
 'io_buffer_size'           : 4096, # How big is the input buffer (in bytes). Default on nRF52 is 1024
 'binary_name'              : 'espruino_%v_curio.bin',
 'build' : {
   'optimizeflags' : '-Og',
   'libraries' : [
     'ESP32',
     'NET',
     'GRAPHICS',
     'CRYPTO','SHA256','SHA512',
     'TLS',
#     'TELNET',
#     'FILESYSTEM',
     'BLUETOOTH',
     'NEOPIXEL'
   ],
   'makefile' : [
     'DEFINES+=-DESP_PLATFORM -DESP32=1',
     'DEFINES+=-DESP_STACK_SIZE=25000',
     'DEFINES+=-DJSVAR_MALLOC', # Allocate space for variables at jsvInit time
     'DEFINES+=-DUSE_FONT_6X8',
     'DEFINES+=-DUSB_CDC', # Because now we have to explicitly request it
     'ESP32_FLASH_MAX=1572864',
#     'DEFINES+=-DBLUETOOTH_NAME_PREFIX=\'\"Curio\"\'', # string passing in IDF4 makefile is broken
     'INCLUDE += -I$(ROOT)/libs/misc',
     'WRAPPERSOURCES += libs/misc/jswrap_curio.c',
     'WRAPPERSOURCES += libs/joltjs/jswrap_qwiic.c',
     'JSMODULESOURCES += _:libs/js/misc/curio.js'
   ]
 }
};

chip = {
  'part'    : "ESP32C3",
  'family'  : "ESP32_IDF4",
  'package' : "",
  'ram'     : 400,
  'flash'   : 0,
  'speed'   : 160,
  'usart'   : 2,
  'spi'     : 1,
  'i2c'     : 1,
  'adc'     : 2,
  'dac'     : 0,
  'saved_code' : {
    'address' : 0x320000,
    'page_size' : 4096,
    'pages' : 224, # 896kb - see partitions_espruino.csv
    'flash_available' : 1344, # firmware can be up to this size - see partitions_espruino.csv
  },
};
devices = {
  'LED1' : { 'pin' : 'D8', "inverted":1 },
  'BTN1' : { 'pin' : 'D9', "inverted":1, 'pinstate' : 'IN_PULLUP' }
};

# left-right, or top-bottom order
board_esp32 = {
   'top' : ['GND','D23','D22','D1','D3','D21','D20','D19','D18','D5','D17','D16','D4','D0'],
   'bottom' : ['D12','D14','D27','D26','D25','D33','D32','D35','D34','D39','D36','EN','3V3','GND'],
   'right' : [ 'GND','D13','D9','D10','D11','D6','D7','D8','D15','D2']
};
board_esp32["bottom"].reverse()
board_esp32["right"].reverse()
board_esp32["_css"] = """
#board {
  width:  600px;
  height: 435px;
  left: 50px;
  top: 170px;
  background-image: url(img/ESP32C3.jpg);
}
#boardcontainer {
  height: 700px;
}
#board #right {
  top: 80px;
  left: 600px;
}
#board #top {
  bottom: 440px;
  left: 155px;
}
#board #bottom  {
  top: 435px;
  left: 155px;
}
#board .rightpin {
  height: 28px;
}
#board .toppin, #board .bottompin {
  width: 24px;
}
""";

boards = [ board_esp32 ];

def get_pins():
  pins = pinutils.generate_pins(0,21) # 22 General Purpose I/O Pins.

  pinutils.findpin(pins, "PD0", True)["functions"]["ADC1_IN0"]=0;
  pinutils.findpin(pins, "PD1", True)["functions"]["ADC1_IN1"]=0;
  pinutils.findpin(pins, "PD2", True)["functions"]["ADC1_IN2"]=0;
  pinutils.findpin(pins, "PD3", True)["functions"]["ADC1_IN3"]=0;
  pinutils.findpin(pins, "PD4", True)["functions"]["ADC1_IN4"]=0;
  # pinutils.findpin(pins, "PD5", True)["functions"]["ADC2_IN0"]=0;
#  pinutils.findpin(pins, "PD8", True)["functions"]["NEGATED"]=0; # LED negated - but ESP32 port ignores negation
  # D12-D17 are SPI (internal SPI) - not sure they should even be exposed??

  pinutils.findpin(pins, "PD18", True)["functions"]["USB"]=0; # D-
  pinutils.findpin(pins, "PD19", True)["functions"]["USB"]=0; # D+
  pinutils.findpin(pins, "PD20", True)["functions"]["USART1_RX"]=0;
  pinutils.findpin(pins, "PD21", True)["functions"]["USART1_TX"]=0;
  pinutils.findpin(pins, "PD9", True)["functions"]["I2C1_SCL"]=0; # added for issue #2589 fix
  pinutils.findpin(pins, "PD8", True)["functions"]["I2C1_SDA"]=0; # added for issue #2589 fix

  # SPI added for issue #2601
  # See esp-idf-4 /components/soc/esp32c3/include/soc/soc_caps.h
  pinutils.findpin(pins, "PD6", True)["functions"]["SPI1_SCK"]=0;
  pinutils.findpin(pins, "PD2", True)["functions"]["SPI1_MISO"]=0;
  pinutils.findpin(pins, "PD7", True)["functions"]["SPI1_MOSI"]=0;



  # everything is non-5v tolerant
  for pin in pins:
    pin["functions"]["3.3"]=0;
  return pins
