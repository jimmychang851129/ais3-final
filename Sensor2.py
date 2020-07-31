import random
import time
import multiprocessing

waterlevel  = multiprocessing.Value("i",random.randint(1,100)) 
command_list = ["inc", "dec", "rep","stop"]

def msg(txt): # send back message
    print(txt, flush=True)

def err(index): # send error message
    error=["Wrong parameter format!","waterlevel achieved to maximum.","waterlevel achieved to minimum.","Unknown command!"]
    #print(error[index])

### waterlevel simulation

status = multiprocessing.Value("i", 0) # 0=default, 1=stop, 2=only inc part stop, 3=only dec part stop
smincrv = multiprocessing.Value("i", 0) # processing amount of inc sm
smdecrv = multiprocessing.Value("i", 0) # processing amount of dec sm
smlimit = multiprocessing.Value("i", 0) # sm limit for inc/dec

def sminc(waterlevel,status,smincrv,smlimit):
    while waterlevel.value < smlimit.value:
        if (status.value == 1) or (status.value == 2):
            status.value = 0
            break
        waterlevel.value += 1
        msg(waterlevel.value)
        time.sleep(1)
    smincrv.value -= 1

def smdec(waterlevel,status,smdecrv,smlimit):
    while waterlevel.value > smlimit.value:
        if (status.value == 1) or (status.value == 3):
            status.value = 0
            break
        waterlevel.value -= 1
        msg(waterlevel.value)
        time.sleep(1)
    smdecrv.value -= 1

###

if __name__ == '__main__':
    msg(waterlevel.value)
    while True:
        pinc = multiprocessing.Process(name='pinc',target=sminc,args=(waterlevel,status,smincrv,smlimit,))
        pdec = multiprocessing.Process(name='pdec',target=smdec,args=(waterlevel,status,smdecrv,smlimit,))
        submit = input()  # command from PLC
        
        if submit.isnumeric():
            submit = int(submit)
            if submit <= 100 and submit >= 0:
                if submit > waterlevel.value:
                    if smincrv.value == 0:
                        smincrv.value += 1
                        status.value = 3
                        smlimit.value = submit
                        pinc.start()
                elif submit < waterlevel.value:
                    if smdecrv.value == 0:
                        smdecrv.value += 1
                        status.value = 2
                        smlimit.value = submit
                        pdec.start() 
                