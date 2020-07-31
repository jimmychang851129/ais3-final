import random
import time
import multiprocessing

waterlevel  = multiprocessing.Value("i",random.randint(1,100)) 
command_list = ["inc", "dec", "rep","stop"]

def msg(txt): # send back message
    print(txt)

ac = True # User Accessed or not from PLC

### waterlevel simulation

status = multiprocessing.Value("i", 0) # 0=default, 1=stop, 2=stop only inc part, 3=stop only dec part
smincrv = multiprocessing.Value("i", 0) # processing amount of inc sm
smdecrv = multiprocessing.Value("i", 0) # processing amount of dec sm
smlimit = multiprocessing.Value("i", 0) # sm limit for inc/dec

def sminc(waterlevel,status,smincrv,smlimit):
    while waterlevel.value < smlimit.value:
        if (status.value == 1) or (status.value == 2):
            status.value = 0
            break
        waterlevel.value += 1
        print(waterlevel.value)
        time.sleep(1)
    smincrv.value -= 1

def smdec(waterlevel,status,smdecrv,smlimit):
    while waterlevel.value > smlimit.value:
        if (status.value == 1) or (status.value == 3):
            status.value = 0
            break
        waterlevel.value -= 1
        print(waterlevel.value)
        time.sleep(1)
    smdecrv.value -= 1

###

if __name__ == '__main__':

    while True:
        pinc = multiprocessing.Process(name='pinc',target=sminc,args=(waterlevel,status,smincrv,smlimit,))
        pdec = multiprocessing.Process(name='pdec',target=smdec,args=(waterlevel,status,smdecrv,smlimit,))
        submit = input()  # command from PLC
        auth = True # User Accessed or not from PLC
        
        submit = submit.split(' ')

        if submit[0] == command_list[0]:  #inc
            if len(submit) > 2 :
                msg("Wrong parameter format!")
            elif len(submit) == 1:
                if smincrv.value == 0:
                    smincrv.value += 1
                    status.value = 3
                    smlimit.value = 100
                    pinc.start()
            elif not (submit[1].isnumeric()):
                msg("Wrong parameter format!")
            else:
                if waterlevel.value+int(submit[1]) <= 100:
                    if smincrv.value == 0:
                        smincrv.value += 1
                        status.value = 3
                        smlimit.value = waterlevel.value
                        smlimit.value += int(submit[1])
                        pinc.start()                    
                else:
                    msg("waterlevel achieved to maximum.")
        elif submit[0] == command_list[1]:  #dec
            if len(submit) > 2 :
                msg("Wrong parameter format!")
            elif len(submit) == 1:
                if smdecrv.value == 0:
                    smdecrv.value += 1
                    status.value = 2
                    smlimit.value = 0
                    pdec.start()
            elif not (submit[1].isnumeric()):
                msg("Wrong parameter format!")
            else:
                if waterlevel.value-int(submit[1]) >= 0:
                    if smdecrv.value == 0:
                        smdecrv.value += 1
                        status.value = 2
                        smlimit.value = waterlevel.value
                        smlimit.value -= int(submit[1])
                        pdec.start() 
                else:
                    msg("waterlevel achieved to minimum.")
        elif submit[0] == command_list[2]:  #rep
            msg(waterlevel.value)
        elif submit[0] == command_list[3]: # stop
            if (smincrv.value == 1) or (smdecrv.value == 1):
                status.value = 1
        else:
            msg("Unknown command!")

# command list:
# inc		-increase waterlevel to maximum
# inc <value>	-increase waterlevel by value
# dec		-decrease waterlevel to minimum
# dec <value>	-decrease waterlevel by value
# stop		-stop increasing or decreasing
# rep		-report current waterlevel