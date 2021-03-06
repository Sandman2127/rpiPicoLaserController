from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
import math
import framebuf
# import framebuf

# Pin definitions
# repl_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
# repl_led = machine.Pin(5, machine.Pin.OUT)
adc_pin = machine.Pin(28)  #31 & 32 & 34 (GPs 26,27,28) are the only pins for ADC ones

#TODO: setup ADC and oled
adc = machine.ADC(adc_pin)
i2c = I2C(0,sda=Pin(0), scl=Pin(1), freq=400000) # pin 1 & 2, GP0, GP1
oled = SSD1306_I2C(128, 32, i2c)
adcDepth = 65536
#inputMilliVoltage = 3300
#inputMilliVoltBias = 16
inputVoltage = 3.300
inputVoltageBias = 0.016
resistorVal = 0.25
maxOutput = 1200 # uW
gammaSymbol = bytearray('\u03B3')

def checkInputCurrent():
    #TODO: take ADC reading int 0 - 4096
    adcRawReading = adc.read_u16()
    #TODO: map and remove 16 mV bias, comes out as 0.0010257...
    mappedVoltage = round((mapVal(adcRawReading,0,adcDepth,0,inputVoltage) - inputVoltageBias),6)
    #TODO: V=IR, thus: I = V/R
    #print(adcRawReading,mappedVoltage)
    #TODO: true value of current across 0.25 ohm resistor assuming no voltage boosting 
    #mAtoLaserOutput = int(1000 * (mappedVoltage/resistorVal))
    #TODO: LM358 boosted value needs to be divided by 10 to get the true result:
    mAtoLaserOutput = round((1000 * ((mappedVoltage/10)/resistorVal)),1)
    #TODO: empirically determined 05/14/22 the system is ~5 mA high from it's actual output throughout the entire range, this is the correction for it
    adjustedmAtoLaserOutput = mAtoLaserOutput - 5
    print(adcRawReading,mappedVoltage,mAtoLaserOutput,adjustedmAtoLaserOutput)
    return adjustedmAtoLaserOutput

def mapVal(value, istart, istop, ostart, ostop):
  return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

def calculateLaserOutput(mAtoLaser):
    #TODO: deprecating linear method
    # 50 mA == 1.2 mW or 1200 uW
    # uW = int(mAtoLaser*(1200/50))
    
    #TODO: setup new exponential output model based on empirical laser results
    # formula: 0.00438e ^ 0.116x     R=0.933, so its not bad...
    uW = (0.00438 * math.exp(0.116 * mAtoLaser)) * 1000 
    # mW = 1000 * uW
    outputStr = 'output: ' + str(uW) + ' uW'
    return outputStr

if __name__ == '__main__':
    while True:
        #TODO: Title
        oled.fill(0)
        #gammastr = '\u03B3'
        #gamma = bytearray(gammastr.encode())
        #fb = framebuf.FrameBuffer(gamma,128,32, framebuf.MONO_HLSB)
        #oled.blit(fb,16,64)
        oled.text("Photon Cannon", 13, 0)
        #TODO: Input (current)
        mAtoLaser = checkInputCurrent()
        mAScreenVal = 'input: ' + str(mAtoLaser) + ' mA'
        oled.text(mAScreenVal, 0, 12, 1)
        print(mAScreenVal)
        #TODO: Output (??)
        uWScreenVal = calculateLaserOutput(mAtoLaser)
        oled.text(uWScreenVal, 0, 24, 1)
        #print(uWScreenVal)
        #TODO: ??
        #oled.text('\u03BB: 635 nm', 0, 24, 1)
        oled.show()
        time.sleep(0.5)




# >>> print("\u03BB")
# ??


# while True:
#    TH = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00[P\x00\x00\x00\x00\x00\x03\xad\xec\x0f\x00\x00\x00\x00\rv\xb6\x1a\x80\x00\x00\x00\x16\xdb[m\x80\x00\x00\x00um\xb5\xb6\x80\x00\x00\x00[\xb5n\xdb\x00\x00\x00\x01\xadW\xb5m\x80\x00\x00\x01w\xed[\xb6\x80\x00\x00\x03\xa8\x1a\xec+\x00\x00\x00\x05@\x17P\x1d\x00\x00\x00\x0e\x00\r\xb0\x06\x80\x00\x00\x08\x00\n\xd0\x00\x00\x00\x00\x08\x00\x17`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x1f\xa0\x00\x00\x00\x00\x00\x00\n\xd0\x00\x00\x00\x00\x00\x00\r`\x00\x00\x00\x00\x00\x00\x17\xb0\x00\x00\x00\x00\x00\x00\n\xd0\x00\x00\x00\x00\x00\x00\x1b`\x00\x00\x00\x00\x00\x00\r\xb0\x00\x00\x00\x00\x00\x00\x16\xa0\x00\x00\x00\x00\x00\x00\x0bp\x00\x00\x00\x00\x00\x00\x1d\xa0\x00\x00\x00\x00\x00\x00\n\xd0\x00\x00\x00\x00\x00\x00\x17p\x00\x00\x00\x00\x00\x00\x1a\xa0\x00\x00\x00\x00\x00\x00\r\xd0\x00\x00\x00\x00\x00\x00\x16\xb0\x00\x00\x00\x00\x00\x00\x1b`\x00\x00\x00\x00\x00\x00\r\xb0\x00\x00\x00\x00\x00\x00\x16\xd0\x00\x00\x00\x00\x00\x00\x1bp\x00\x00\x00\x00\x00\x00\r\xa8\x00\x00\x00\x00\x00\x00\x16\xb0\x00\x00\x00\x00\x00\x00\x1b`\x00\x00\x00\x00\x00\x00\x15\xb0\x00\x00\x00\x00\x00\x00\x1e\xd0\x00\x00\x00\x00\x00\x00\x13p\x00\x00\x00\x00\x00\x00\x1d\xa8\x00\x00\x00\x00\x00\x00\x16\xb0\x00\x00\x00\x00\x00\x00\x15\xd0\x00\x00\x00\x00\x00\x00\x1a\xb8\x00\x00\x00\x00\x00\x00\x17`\x00\x00\x00\x00\x00\x00\x1a\xd8\x00\x00\x00\x00\x00\x00\x17h\x00\x00\x00\x00\x00\x00\x1a\xb0\x00\x00\x00\x00\x00\x00\x1d\xd8\x00\x00\x00\x00\x00\x00+h\x00\x00\x00\x00\x00\x00\x16\xb0\x00\x00\x00\x00\x00\x00\x1b\xd8\x00\x00\x00\x00\x00\x00\x16`\x00\x00\x00\x00\x00\x00\x0b\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
#    fb = framebuf.FrameBuffer(TH,64,64, framebuf.MONO_HLSB)
#    oled.fill(0)
#    for i in range(-64,128):
#        oled.blit(fb,i,0)
#        oled.show()
#    LOGO = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x800\xc0\xc7\xf8~0\xc3\x0c\x1f\x87\xf8\x0c\x00\x00\x01\x800\xc1\xcf\xec\x7f0\xc7\x1c\x1f\xc7\xf8\x0c\x00\x00\x01\x800\xc1\xc1\x8ec\x99\xc6\x1c\x18\xe6\x00\x0c\x0c&`\x180\xc3\xe0\x06a\x99\xe6\x1e\x18f\x00\x1f>\x7f\xf8~0\xc3a\x8ea\x99\xe66\x18f\x00\x0cws\x98d?\xc3a\xbca\x99\xee6\x1f\xc7\xf0\x0ccs\x98`?\xc61\xb8a\x8f<s\x1f\x87\xf0\x0ccs\x18~0\xc61\x98a\x8f<c\x19\x86\x00\x0ccs\x18\x1e0\xc7\xf1\x9ca\x8f<\x7f\x99\xc6\x00\x0ccs\x18\x060\xcf\xf9\x8cc\x8e8\xff\x98\xc6\x00\x0f\x7fs\x18~0\xcc\x19\x8e\x7f\x06\x18\xc1\x98\xe7\xf8\x07>s\x18|0\xcc\x1d\x86|\x06\x18\xc1\xd8g\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
#    fb = framebuf.FrameBuffer(LOGO,128,64, framebuf.MONO_HLSB)
#    oled.fill(0)
#    for i in range(-128,128):
#        oled.blit(fb,i,0)
#        oled.show()




# import sys
# print("")
# Useful unicode symbols in engineering
# unicode	character	description
# \u0394	??	GREEK CAPITAL LETTER DELTA
# \u03A9	??	GREEK CAPITAL LETTER OMEGA
# \u03C0	??	GREEK SMALL LETTER PI
# \u03F4	??	GREEK CAPITAL THETA SYMBOL
# \u03BB	??	GREEK SMALL LETTER LAMDA
# \u03B8	??	GREEK SMALL LETTER THETA
# \u03B1	??	DEGREE SYMBOL
# i\u0302	i??	i HAT
# j\u0302	j??	j HAT
# k\u0302	k??	k HAT
# u\u0302	u??	u HAT
# Greek lower case letters
# unicode	character	description
# \u03B1	??	GREEK SMALL LETTER ALPHA
# \u03B2	??	GREEK SMALL LETTER BETA
# \u03B3	??	GREEK SMALL LETTER GAMMA
# \u03B4	??	GREEK SMALL LETTER DELTA
# \u03B5	??	GREEK SMALL LETTER EPSILON
# \u03B6	??	GREEK SMALL LETTER ZETA
# \u03B7	??	GREEK SMALL LETTER ETA
# \u03B8	??	GREEK SMALL LETTER THETA
# \u03B9	??	GREEK SMALL LETTER IOTA
# \u03BA	??	GREEK SMALL LETTER KAPPA
# \u03BB	??	GREEK SMALL LETTER LAMDA
# \u03BC	??	GREEK SMALL LETTER MU
# \u03BD	??	GREEK SMALL LETTER NU
# \u03BE	??	GREEK SMALL LETTER XI
# \u03BF	??	GREEK SMALL LETTER OMICRON
# \u03C0	??	GREEK SMALL LETTER PI
# \u03C1	??	GREEK SMALL LETTER RHO
# \u03C2	??	GREEK SMALL LETTER FINAL SIGMA
# \u03C3	??	GREEK SMALL LETTER SIGMA
# \u03C4	??	GREEK SMALL LETTER TAU
# \u03C5	??	GREEK SMALL LETTER UPSILON
# \u03C6	??	GREEK SMALL LETTER PHI
# \u03C7	??	GREEK SMALL LETTER CHI
# \u03C8	??	GREEK SMALL LETTER PSI
# \u03C9	??	GREEK SMALL LETTER OMEGA
# Greek upper case letters
# unicode	character	description
# \u0391	??	GREEK CAPITAL LETTER ALPHA
# \u0392	??	GREEK CAPITAL LETTER BETA
# \u0393	??	GREEK CAPITAL LETTER GAMMA
# \u0394	??	GREEK CAPITAL LETTER DELTA
# \u0395	??	GREEK CAPITAL LETTER EPSILON
# \u0396	??	GREEK CAPITAL LETTER ZETA
# \u0397	??	GREEK CAPITAL LETTER ETA
# \u0398	??	GREEK CAPITAL LETTER THETA
# \u0399	??	GREEK CAPITAL LETTER IOTA
# \u039A	??	GREEK CAPITAL LETTER KAPPA
# \u039B	??	GREEK CAPITAL LETTER LAMDA
# \u039C	??	GREEK CAPITAL LETTER MU
# \u039D	??	GREEK CAPITAL LETTER NU
# \u039E	??	GREEK CAPITAL LETTER XI
# \u039F	??	GREEK CAPITAL LETTER OMICRON
# \u03A0	??	GREEK CAPITAL LETTER PI
# \u03A1	??	GREEK CAPITAL LETTER RHO
# \u03A3	??	GREEK CAPITAL LETTER SIGMA
# \u03A4	??	GREEK CAPITAL LETTER TAU
# \u03A5	??	GREEK CAPITAL LETTER UPSILON
# \u03A6	??	GREEK CAPITAL LETTER PHI
# \u03A7	??	GREEK CAPITAL LETTER CHI
# \u03A8	??	GREEK CAPITAL LETTER PSI
# \u03A9	??	GREEK CAPITAL LETTER OMEGA
# \u03F4	??	GREEK CAPITAL THETA SYMBOL