from bridge import *
'''
Input variables
'''
trace = bool(int(input()))
ob = Bridge(-1,[])
ob2 = Lan('', [])

n = int(input())
stop_flag = False
list_obs = [ob.__class__ for i in range(n)]
lan_bridge_dic = {}
bridge_links = []
lan_links = {}

'''
This loop takes all the bridges and their neighbouring Lans as inputs.
Then, these inputs are used to instantiate the Bridge and Lan objects for each Bridge and Lan.
'''
for i in range(n):
    inp = input().split()
    inp = inp[1:]
    inp.sort()
    bridge_links.append(list_obs[i](i,inp)) #Bridge objects are stored in the bridge_links list
    for j in inp:
        lan_bridge_dic[j] = lan_bridge_dic.get(j, []) + [i] #Dictionary containing lists of bridges connecting each Lan

lan_obs = [ob2.__class__ for i in lan_bridge_dic]
lans = list(lan_bridge_dic.keys())

for i in range(len(lans)):
    lan_links[lans[i]] = lan_obs[i](lans[i], lan_bridge_dic[lans[i]]) #Lan objects are stored in lan_links list

'''
Sending the first messages from each bridge, where each bridge thinks of itself to be the root bridge.
'''
for i in range(n):
    temp = bridge_links[i].send(trace,0)
    for j in list(temp.keys()):
        lan_links[j].receive(temp[j])

time=1
while not stop_flag:
    stop_flag = True
    '''
    This is the part where each bridge receives the message sent through the Lans.
    These messages are sent to the receive function of the Bridge class by the Lan objects holding the messages sent to them in the previous time instance.
    '''

    for i in range(n):
        message_dict = {}
        for j in bridge_links[i].neighbors:
            message_dict[j] = lan_links[j].messages
        bridge_links[i].receive(message_dict, trace, time) #This function is used to assign all the RPs
        if bridge_links[i].flag: #If the flag variable is False for all the bridges, then the while loop stops and no more messages are transferred.
            stop_flag = False

    for i in lans:
        lan_links[i].update(bridge_links) #This function is used to assign all the DPs
        lan_links[i].reset() #This function just resets the messages in each Lan.

    '''
    This is the sending part of simulation. The messages are sent from each bridge and the messages sent to each Lan are updated using the receive function in the Lan class
    '''
    for i in range(n):
        temp = bridge_links[i].send(trace,time)
        for j in list(temp.keys()):
            lan_links[j].receive(temp[j])
    time+=1
'''
This subroutine was added only to print and check if a bridge has no DPs.
If a bridge has no DPs, all of it's ports would become NPs
'''
for i in range(n):
    bridge_on = False
    for j in bridge_links[i].neighbors:
        bridge_on = bridge_on or (bridge_links[i].ports_type[j]=='DP')
    if not bridge_on:
        bridge_links[i].ports_type[bridge_links[i].rp] = 'NP'
    print('B'+str(i+1)+':',end=' ')
    for j in bridge_links[i].neighbors:
        print(j+'-'+bridge_links[i].ports_type[j],end=' ')
    print()
