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

KP = 1.2
KI = 0.001
KD = 0.00001

Vpred = 0
ZatackaL = 0
ZatackaR = 0
Krizovatka = 0

previouserrorsum = 0
previouserror = []


def MotorPID(Sens,KoresMotor,previouserrorsum):
    
    Threshold = 64000
    error = 0
    
    
    error = Threshold - Sens.read_u16()
    previouserrorsum = previouserrorsum + error
    
    
    P = KP * error
    I = KI * previouserrorsum
    D = KD * (error - previouserror[0])
    
    previouserror[0] = error
    
    PIDsum = P + I + D
    
    
    KoresMotorValue = 30000 + round(PIDsum)
    if KoresMotorValue >= 65535:
        KoresMotorValue = 40000
        KoresMotor.duty_u16(KoresMotorValue)
    elif KoresMotorValue <= 3000:
        KoresMotorValue = 20000
    else:
        KoresMotor.duty_u16(KoresMotorValue)
   
    return KoresMotorValue
    

        
        
    
    #levej a pravej nevidí a střed vidí = rovně
    #levej a pravej vidí -- // -- = křižovatka
    #levej vidí pravej nevidí  -- // -- = vlevo
    #levej nevidí pravej vidí -- // -- = vpravo
    
    #pro přesnější switch z PID na zatáčky potřebuje více exitů z loopy


while True:
    
    if button.value() == 1:
        MotorF1.duty_u16(0)
        MotorF2.duty_u16(0)
        MotorB1.duty_u16(0)
        MotorB2.duty_u16(0)
        break
    elif Sens8.read_u16() > 55000 and Sens1.read_u16() > 55000 and Sens4.read_u16() > 55000:
        if button.value() == 1:
            MotorF1.duty_u16(0)
            MotorF2.duty_u16(0)
            MotorB1.duty_u16(0)
            MotorB2.duty_u16(0)
            break
        else:
            while True:
                if button.value() == 1:
                    MotorF1.duty_u16(0)
                    MotorF2.duty_u16(0)
                    MotorB1.duty_u16(0)
                    MotorB2.duty_u16(0)
                    break
                elif Sens8.read_u16() < 25000 and Sens1.read_u16() < 25000 and Sens4.read_u16() > 48000:
                    MotorF1.duty_u16(0)
                    MotorF2.duty_u16(0)
                    MotorB1.duty_u16(0)
                    MotorB2.duty_u16(0)
                    print("změna z krizovatka1")
                    break
                elif Sens8.read_u16() > 50000 and Sens1.read_u16() < 25000 and Sens4.read_u16() > 52500:
                    MotorF1.duty_u16(0)
                    MotorF2.duty_u16(0)
                    MotorB1.duty_u16(0)
                    MotorB2.duty_u16(0)
                    print("změna z krizovatkA2")
                    break
                elif Sens8.read_u16() < 25000 and Sens1.read_u16() > 50000 and Sens4.read_u16() > 52500:
                    MotorF1.duty_u16(0)
                    MotorF2.duty_u16(0)
                    MotorB1.duty_u16(0)
                    MotorB2.duty_u16(0)
                    print("změna z krizovatka3")
                    break
                MotorPID(Sens4,MotorF2,previouserrorsum)
                MotorPID(Sens5,MotorF1,previouserrorsum)
                
    elif Sens8.read_u16() > 55000 and Sens1.read_u16() < 22000 and Sens4.read_u16() > 52500:
        if button.value() == 1:
            MotorF1.duty_u16(0)
            MotorF2.duty_u16(0)
            MotorB1.duty_u16(0)
            MotorB2.duty_u16(0)
            break
        else:
            while True:
                if button.value() == 1:
                    MotorF1.duty_u16(0)
                    MotorF2.duty_u16(0)
                    MotorB1.duty_u16(0)
                    MotorB2.duty_u16(0)
                    break
                else:
                    MotorF1.duty_u16(65535)
                    MotorF2.duty_u16(0)
                    MotorB1.duty_u16(0)
                    MotorB2.duty_u16(65535)
                    sleep(0.7)
                    if Sens8.read_u16() < 25000 and Sens1.read_u16() < 25000 or Sens4.read_u16() > 48000:
                        MotorF1.duty_u16(0)
                        MotorF2.duty_u16(0)
                        MotorB1.duty_u16(0)
                        MotorB2.duty_u16(0)
                        break
#                     elif Sens8.read_u16() < 25000 and Sens1.read_u16() > 50000 or Sens4.read_u16() > 52500:
#                         MotorF1.duty_u16(0)
#                         MotorF2.duty_u16(0)
#                         MotorB1.duty_u16(0)
#                         MotorB2.duty_u16(0)
#                         break
                    
    elif Sens8.read_u16() < 20000 and Sens1.read_u16() > 60000 and Sens4.read_u16() > 52500:
        if button.value() == 1:
            MotorF1.duty_u16(0)
            MotorF2.duty_u16(0)
            MotorB1.duty_u16(0)
            MotorB2.duty_u16(0)
            break
        else:
            while True:
                if button.value() == 1:
                    MotorF1.duty_u16(0)
                    MotorF2.duty_u16(0)
                    MotorB1.duty_u16(0)
                    MotorB2.duty_u16(0)
                    break
                else:
                    MotorF1.duty_u16(0)
                    MotorF2.duty_u16(65535)
                    MotorB1.duty_u16(65535)
                    MotorB2.duty_u16(0)
                    sleep(0.7)
                    if Sens8.read_u16() < 25000 and Sens1.read_u16() < 25000 or Sens4.read_u16() > 48000:
                        MotorF1.duty_u16(0)
                        MotorF2.duty_u16(0)
                        MotorB1.duty_u16(0)
                        MotorB2.duty_u16(0)
                        break
#                     elif Sens8.read_u16() > 50000 and Sens1.read_u16() < 25000 or Sens4.read_u16() > 48000:
#                         MotorF1.duty_u16(0)
#                         MotorF2.duty_u16(0)
#                         MotorB1.duty_u16(0)
#                         MotorB2.duty_u16(0)
#                         break
    elif Sens8.read_u16() < 20000 and Sens1.read_u16() < 20000 and Sens4.read_u16() > 48000:
        if button.value() == 1:
            MotorF1.duty_u16(0)
            MotorF2.duty_u16(0)
            MotorB1.duty_u16(0)
            MotorB2.duty_u16(0)
            break
        else:
            while True:
                if button.value() == 1:
                    MotorF1.duty_u16(0)
                    MotorF2.duty_u16(0)
                    MotorB1.duty_u16(0)
                    MotorB2.duty_u16(0)
                    break
                elif Sens8.read_u16() > 50000 or Sens1.read_u16() > 50000:
                    MotorF1.duty_u16(0)
                    MotorF2.duty_u16(0)
                    MotorB1.duty_u16(0)
                    MotorB2.duty_u16(0)
                    break
                elif Sens8.read_u16() > 50000 and Sens1.read_u16() < 25000 or Sens4.read_u16() > 52500:
                        MotorF1.duty_u16(0)
                        MotorF2.duty_u16(0)
                        MotorB1.duty_u16(0)
                        MotorB2.duty_u16(0)
                        break
                elif Sens8.read_u16() < 25000 and Sens1.read_u16() > 50000 or Sens4.read_u16() > 52500:
                        MotorF1.duty_u16(0)
                        MotorF2.duty_u16(0)
                        MotorB1.duty_u16(0)
                        MotorB2.duty_u16(0)
                        break
                MotorPID(Sens3,MotorF2,previouserrorsum)
                MotorPID(Sens6,MotorF1,previouserrorsum)
    else:
        if button.value() == 1:
            MotorF1.duty_u16(0)
            MotorF2.duty_u16(0)
            MotorB1.duty_u16(0)
            MotorB2.duty_u16(0)
            break
        else:
            while True:
                if button.value() == 1:
                    MotorF1.duty_u16(0)
                    MotorF2.duty_u16(0)
                    MotorB1.duty_u16(0)
                    MotorB2.duty_u16(0)
                    break
                elif Sens8.read_u16() > 50000 or Sens1.read_u16() > 50000:
                    MotorF1.duty_u16(0)
                    MotorF2.duty_u16(0)
                    MotorB1.duty_u16(0)
                    MotorB2.duty_u16(0)
                    break
                elif Sens8.read_u16() > 50000 and Sens1.read_u16() < 25000 or Sens4.read_u16() > 52500:
                        MotorF1.duty_u16(0)
                        MotorF2.duty_u16(0)
                        MotorB1.duty_u16(0)
                        MotorB2.duty_u16(0)
                        break
                elif Sens8.read_u16() < 25000 and Sens1.read_u16() > 50000 or Sens4.read_u16() > 52500:
                        MotorF1.duty_u16(0)
                        MotorF2.duty_u16(0)
                        MotorB1.duty_u16(0)
                        MotorB2.duty_u16(0)
                        break
                MotorPID(Sens3,MotorF2,previouserrorsum)
                MotorPID(Sens4,MotorF1,previouserrorsum)



















































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
    
        
    
    
    