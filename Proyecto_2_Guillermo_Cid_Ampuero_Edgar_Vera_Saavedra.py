import smbus #Se importa la libreria smbus para la comunicacion I2C
import time  #Se importa la libreria time para generar el tiempo en segundos en la grafica
import numpy as np #Se importa numpy que permite trabajar con arreglos
import time
import psycopg2

#-------Base de Datos---------

db = psycopg2.connect(host="192.168.1.100",database="guillermo",user="guillermo",password="memo123") #Se instancian los parametros para la base de datos
cur = db.cursor() #crea el cursor para las peticiones de la Base de Datos



#-----Acelerometro------

#Se instancian algunos registros y direcciones del Sensor MPU6050
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

#Se crea la funcion que permite iniciar el Sensor MPU6050
def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

#Se crea la funcion que permite leer los datos 
def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init() #Se inicia el Sensor

print (" Reading Data of Gyroscope and Accelerometer")



#Se define la funcion datos que permite obtener los datos de la Aceleracion para el Eje x, y y z

while True:
            
    #Read Accelerometer raw value
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
    Ax = acc_x/16384.0 
    Ay = acc_y/16384.0
    Az = acc_z/16384.0
    cur.execute('''INSERT INTO MPU6050(Ax,Ay,Az) VALUES(%s,%s,%s);''',(Ax,Ay,Az)) #Se añaden los datos a la base de datos
    db.commit()
    time.sleep(2)
        



