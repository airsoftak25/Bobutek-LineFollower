from machine import Pin, PWM,ADC
from time import sleep


Sens8 = ADC(36)
Sens7 = ADC(39)
Sens6 = ADC(34)
Sens5 = ADC(35)
Sens4 = ADC(32)
Sens3 = ADC(33)
Sens2 = ADC(25)
Sens1 = ADC(26)

MotorB1 = PWM(23)
MotorF1 = PWM(22)

MotorF1.freq(500)
MotorF1.duty_u16(0)
MotorB1.freq(500)
MotorB1.duty_u16(0)

MotorB2 = PWM(19)
MotorF2 = PWM(18)

MotorF2.freq(500)
MotorF2.duty_u16(0)
MotorB2.freq(500)
MotorB2.duty_u16(0)

KonecSens1 = Pin(13)
KonecSens2 = Pin(14)

button = Pin(4,Pin.IN)
button.value(0)

KP = 2.3
KI = 0.000078
KD = 0.0001

Vpred = 0
ZatackaL = 0
ZatackaR = 0
Krizovatka = 0

previouserrorsum = 0
previouserror = [0]


def MotorPID(Sens1,Sens2,KoresMotor1,KoresMotor2,previouserrorsum,previouserror):
    
    
    Threshold = 50000
    error = 0
    
    error =  Threshold - round((100000 * Sens2.read_u16() / ( Sens1.read_u16() + Sens2.read_u16())))
    previouserrorsum = previouserrorsum + error
    
    
    P = KP * error
    I = KI * previouserrorsum
    D = KD * (error - previouserror[0])
    
    previouserror[0] = error
    
    PIDsum = P + I + D
    
    
    if 30000 + round(PIDsum) > 65535 or 30000 + round(PIDsum) < 5000:
        KoresMotor1.duty_u16(65000)
        KoresMotor2.duty_u16(30000)
        
    elif 30000 - round(PIDsum) > 65535 or 30000 - round(PIDsum) < 5000:
        KoresMotor1.duty_u16(30000)
        KoresMotor2.duty_u16(65000)
    else:
        KoresMotor1.duty_u16(30000 + round(PIDsum))
        KoresMotor2.duty_u16(30000 - round(PIDsum))
    #levej a pravej nevidí a střed vidí = rovně
    #levej a pravej vidí -- // -- = křižovatka
    #levej vidí pravej nevidí  -- // -- = vlevo
    #levej nevidí pravej vidí -- // -- = vpravo
    
while True:
    
    if button.value() == 1:
        MotorF1.duty_u16(0)
        MotorF2.duty_u16(0)
        MotorB1.duty_u16(0)
        MotorB2.duty_u16(0)
        break
    else:
        MotorF1.duty_u16(0)
        MotorF2.duty_u16(0)
        MotorB1.duty_u16(0)
        MotorB2.duty_u16(0)
        while True:
            if button.value() == 1:
                MotorF1.duty_u16(0)
                MotorF2.duty_u16(0)
                MotorB1.duty_u16(0)
                MotorB2.duty_u16(0)
                break
            else:
                MotorPID(Sens3,Sens6,MotorF2,MotorF1,previouserrorsum,previouserror)
                
        
        





















































#     elif Sens1.read_u16() > 60000 and Sens8.read_u16() > 60000:
#         if button.value() == 1:
#             break
#         MotorPID(Sens4,MotorF1,previouserrorsum)
#         MotorPID(Sens5,MotorF2,previouserrorsum)
#     elif Sens1.read_u16() > 62000 and Sens8.read_u16() < 30000:#přidej opak senz8 do if
#         MotorF1.duty_u16(0) #taky dej MotorPID nahoru jako první podmínku tu s křižovatkama
#         MotorB1.duty_u16(0)
#         MotorF2.duty_u16(0)
#         MotorB2.duty_u16(0)
#         while True:
#             if button.value == 1:
#                 break
#             MotorF1.duty_u16(0)
#             MotorB1.duty_u16(0)
#             MotorF2.duty_u16(65535)
#             MotorB2.duty_u16(0)
#             if Sens1.read_u16() < 25000:
#                 MotorF1.duty_u16(0)
#                 MotorB1.duty_u16(0)
#                 MotorF2.duty_u16(0)
#                 MotorB2.duty_u16(0)
#                 break
#     elif Sens8.read_u16() > 62000 and Sens1.read_u16() < 30000:
#         MotorF1.duty_u16(0)
#         MotorB1.duty_u16(0)
#         MotorF2.duty_u16(0)
#         MotorB2.duty_u16(0)
#         while True:
#             if button.value == 1:
#                 break
#             MotorF1.duty_u16(65535)
#             MotorB1.duty_u16(0)
#             MotorF2.duty_u16(0)
#             MotorB2.duty_u16(0)
#             if Sens8.read_u16() < 25000:
#                 MotorF1.duty_u16(0)
#                 MotorB1.duty_u16(0)
#                 MotorF2.duty_u16(0)
#                 MotorB2.duty_u16(0)
#                 break
#     else:
#         if button.value() == 1:
#             break
#         
#         MotorPID(Sens4,MotorF1,previouserrorsum)
#         MotorPID(Sens5,MotorF2,previouserrorsum)
#        
    
        
    
    
    