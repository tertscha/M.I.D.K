from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

#motordefiníciók
balmotor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
jobbmotor = Motor(Port.B )
elso_emelo = Motor(Port.D)
hatso_emelo = Motor(Port.E)

#robotunk definíciója
robotka = DriveBase(balmotor,jobbmotor,56,128)



#szinszenzor definíciója
szinszenzorfel = ColorSensor(Port.C)
szinszenzorle = ColorSensor(Port.F)

#előremenés 20 centit:
#elore(20)
def elore(centi):
    robotka.straight(centi * 10)

#forgás -45 fokot:
#forgas(-45)
def forgas(fokot):
    robotka.turn(fokot)

#bal gomb nyomására vár
#bal_gombra_var()
def bal_gombra_var():
    while not Button.LEFT in hub.buttons.pressed():
        wait(0)

#szin megjegyzése szin változóba
szin = Color.NONE
 #Azért kell, hogy kívülről is látszon



#folyamatos szindetektálás
#folyamatos_szindetektalas()
def folyamatos_szindetektalas():
    while True:
        szindetektalas()
        hub.light.on(szin)
#bal_gombra_var()

visszavert_feny = 0
def visszavertfeny_detektalas():
    bal_gombra_var()
    global visszavert_feny
    visszavert_feny = szinszenzor.reflection()
    print(visszavert_feny)

def folyamatos_visszavert_feny_detektalas():
    while True:
        visszavertfeny_detektalas()

#vonalkövetés beállításai
feher_vf = 99
fekete_vf = 16
atlag_vf = (feher_vf + fekete_vf) / 2
alapsebesseg = 300
szorzo = 3.0
reflection = 0

#baloldali_vonalkövetés
def vonal_kovetes_baloldalon():
    reflection = szinszenzor.reflection()
    hiba = reflection - atlag_vf

    elfordulas = szorzo * hiba

    balmotor.run(alapsebesseg + elfordulas)
    jobbmotor.run(alapsebesseg - elfordulas)

    wait(10)  # 10 ms ciklus

#baloldali_vonalkövetés
def vonal_kovetes_JOBBoldalon():
    reflection = szinszenzor.reflection()
    hiba = reflection - atlag_vf

    elfordulas = szorzo * hiba

    balmotor.run(alapsebesseg - elfordulas)
    jobbmotor.run(alapsebesseg + elfordulas)

    wait(10)  # 10 ms ciklus
#végtelen vonalkövetés
#while True:
#    vonal_kovetes_baloldalon()

def menj_feketeig(speed):
    robotka.drive(speed,0)
    while szinszenzor.reflection() > fekete_vf + 1:
        wait(10)
    robotka.stop()

#menj_feketeig()

def vonal_kovetes_baloldalon_feketeig():
    while szinszenzor.reflection() > fekete_vf + 1:
        vonal_kovetes_baloldalon()
    robotka.stop()    

def vonal_kovetes_baloldalon_feherig():
    print(szinszenzor.reflection())
    while szinszenzor.reflection() < feher_vf :
        vonal_kovetes_baloldalon()
    robotka.stop()       

def kinyitas():
    elso_emelo.run_target(900,-90)

def befogas():
    elso_emelo.run_target(900,-180)

def emeles():
    hatso_emelo.run_angle(500,60)

def falhozi():
    robotka.use_gyro(False)
    elore(- 10)
    robotka.use_gyro(True)

def leemeles():
    hatso_emelo.run_angle(500,-65)

def teljesenfel():
    hatso_emelo.run_angle(900,180)

def teljesenle():
    hatso_emelo.run_angle(900,-185)

def vonal_kovetes_JOBBoldalon_feketeig():
    while szinszenzor.reflection() > fekete_vf + 1:
        vonal_kovetes_JOBBoldalon()
    robotka.stop()    

def vonal_kovetes_JOBBoldalon_feherig():
    print(szinszenzor.reflection())
    while szinszenzor.reflection() < feher_vf :
        vonal_kovetes_JOBBoldalon()
    robotka.stop()      

#robot programja

'''
elore(30)
forgas(90)
'''

elore(-45)
falhozi()
elore(20)
forgas(-90)
elore(107)
forgas(-90)
elore(11)
befogas() #megfogja a mikrofont
elore(-20)
forgas(90)
elore(50)
forgas(90)
teljesenle()
elore(-18)
emeles()
elore(39) #megfogja a kábelt
forgas(87)
elore(-42)
leemeles() #lerakja a kábelt
elore(10)
forgas(-100)
elore(9)
kinyitas() #kiengedi a mikrofont
elore(-15)
forgas(93)
elore(30)
forgas(105)
elore(-37)
emeles() #megfogja a másik kábelt
elore(19)
forgas(-75)
elore(-46)
leemeles() #lerakja a másik kábelt
elore(172)
teljesenfel()
forgas(-100)
elore(-21)
falhozi()
elore(3)
forgas(-90)
elore(20)
befogas()
kinyitas()
elso_emelo.brake()
elore(160)
