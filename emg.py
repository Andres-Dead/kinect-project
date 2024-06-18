# Registro de EMG

from machine import Pin, ADC
import time

 # Configurar canales de lectura
CH1 = ADC(Pin(32))
CH1.atten(ADC.ATTN_11DB) # 3.3 V
CH1.width(ADC.WIDTH_12BIT)

CH2 = ADC(Pin(25))
CH2.atten(ADC.ATTN_11DB)
CH2.width(ADC.WIDTH_12BIT)

muestras = 2000

 # Guardar listas en un documento de texto
with open('REGISTRO 1.txt', 'w+') as reg:
     for x in range(muestras):
         val1 = CH1.read()
         val2 = CH2.read()
         R1 = val1 * 3300/4095
         R2 = val2 * 3300/4095
         registro = {'Muestra': x,\
        'Canal 1': R1, 'Canal 2': R2}
         print(registro)
     F0 = str(registro['Muestra'])
     F1 = str(registro['Canal 1'])
     F2 = str(registro['Canal 2'])
     lista = " ".join([F0, F1,\
     F2, '\n'])
     reg.write(lista)
     time.sleep_ms(2)

