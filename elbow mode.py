import ckbot.logical as L
from time import sleep

# 43 43 34 cm
def move(l1,l2,l3,mod):
    pos1 = (l1 - 0.367)/0.060 * 3.14
    pos2 = (l2 - 0.440)/0.060 * 3.14
    pos3 = (l3 - 0.445)/0.060 * 3.14
    mod.at.MOD1.set_speed(1)
    mod.at.MOD2.set_speed(1)
    mod.at.MOD3.set_speed(1)
    mod.at.MOD1.set_pos(pos1)
    mod.at.MOD2.set_pos(pos2)
    mod.at.MOD3.set_pos(pos3)

# stop motor and go_slack on each module
def shut_down(c):
    print "shut down"
    for m in c.itermodules():
        m.go_slack()

def traj(step):
    Mat = [[0 for x in range(3)] for x in range(20)] 
    Mat[0] = [0.4450238758, 0.4404159965, 0.3671883032]
    Mat[1] = [0.4468355876, 0.4422465854, 0.3649146962]
    Mat[2] = [0.4486406263, 0.4440702777, 0.362632049]
    Mat[3] = [0.4504388927, 0.4458869768, 0.3603404201]
    Mat[4] = [0.4522302889, 0.4476965872, 0.3580398685]
    Mat[5] = [0.4540147181, 0.4494990147, 0.3557304534]
    Mat[6] = [0.4557920847, 0.4512941662, 0.3534122342]
    Mat[7] = [0.4575622943, 0.4530819497, 0.3510852706]
    Mat[8] = [0.4593252536, 0.4548622744, 0.3487496226]
    Mat[9] = [0.4610808707, 0.4566350504, 0.3464053506]
    Mat[10] = [0.4628290543, 0.4584001893, 0.3440525149]
    Mat[11] = [0.4645697147, 0.4601576032, 0.3416911765]
    Mat[12] = [0.466302763, 0.4619072058, 0.3393213965]
    Mat[13] = [0.4680281113, 0.4636489113, 0.3369432361]
    Mat[14] = [0.469745673, 0.4653826354, 0.3345567571]
    Mat[15] = [0.4714553624, 0.4671082944, 0.3321620214]
    Mat[16] = [0.4731570946, 0.4688258058, 0.3297590912]
    Mat[17] = [0.4748507861, 0.470535088, 0.3273480289]
    Mat[18] = [0.4765363541, 0.4722360604, 0.3249288973]
    Mat[19] = [0.4782137168, 0.4739286433, 0.3225017596]
    l3 = Mat[step][0]
    l2 = Mat[step][1]
    l1 = Mat[step][2]

    return (l1,l2,l3)
    

if __name__ == "__main__":
    modules = {0xE3: 'MOD1', 0xE6: 'MOD2', 0xDF: 'MOD3'}
    c = L.Cluster()
    c.populate(len(modules), modules)
    for i in range(0,18):
	sleep(0.2)  
        move(traj(i)[0], traj(i)[1], traj(i)[2], c)
    

    sleep(1)
    for i in range(17,-1,-1):
	sleep(0.2)
        move(traj(i)[0], traj(i)[1], traj(i)[2], c)
    sleep(3)    
    shut_down(c)

