#Class containing the various entities represented within an individual Lan
class Lan: 
    def __init__(self, ch, bridges):
        '''
        Initializing all the entities of the Lan
        '''
        self.ch = ch #Character representing the Lan
        self.dp = -1 #Designated Port for the Lan (initialised to -1)
        self.bridges = bridges #List of Neighbouring bridges to the Lan
        self.bridges.sort() #Sorting the list just in case
        self.messages = [] #Messages stored in the 
        self.best_mess = [] #Best message stored in Lan
        if(len(bridges)>0):
            self.best_mess = [bridges[0], 0, bridges[0]] #Best message set to [n,0,n]
            self.dp = bridges[0] #DP set to the smallest bridge
    def reset(self):
        '''
        Function to discard the messages stored in Lan after each time step
        '''
        self.messages = []
    def receive(self, message):
        '''
        Receiving each message at a given time step
        '''
        self.messages.append(message)
    def update(self, bridge_links):
        '''
        Updates the type of ports connected to the Lan, by choosing one of the ports to be the DP for this Lan
        '''
        for i in self.messages:
            if not(i==[]) and (i < self.best_mess): #Here, i<self.best_mess solves Cases 1,2,3 in one step
                self.dp = i[2]
                self.best_mess = i #Finding best message received
        for i in self.bridges:
            if (bridge_links[i].ports_type[self.ch] == 'DP') and not(self.dp==i): #Setting all the non-DP ports to NP
                bridge_links[i].ports_copy[self.ch] = 'NP'
        return

#Class containing the various entities and functions in a given bridge
class Bridge:
    def __init__(self, n, ports):
        self.ports_type = {} #Type of ports (DP,NP,RP)
        self.message = {} #Message sent to each of the neighboring Lans
        self.ports_copy = {} #Copy of ports_type (used during receiving)
        self.n = n #Index of bridge
        self.rp = '' #Location of Root Port
        self.neighbors = ports #Neighboring Lans
        for i in self.neighbors:
            self.ports_type[i] = 'DP' #Initializing all neighboring ports to DP
            self.message[i] = [n,0,n] #Initializing Message to be sent on each Lan
        self.ports_copy = self.ports_type.copy()
        self.flag = True
        self.best_sent = [n,0,n] #Best message to send
        self.best_received = [n,0,n] #Best message received
    
    def send(self,trace,time):
        '''
        Used for sending the message from the current bridge to each respective Lan, according to the best message to be sent
        and the type of ports connecting the Lan to the bridge (DP,NP,RP)
        '''
        self.ports_type = self.ports_copy.copy() #Make copy of ports_type
        for i in self.neighbors:
            if(not(self.flag) or (self.ports_type[i]!='DP')): #If the port is not DP, don't send message
                self.message[i] = []
            else:
                if trace:
                    print(str(time)+' s B'+str(self.n+1)+' (B'+str(self.best_sent[0]+1)+','+str(self.best_sent[1])+',B'+str(self.best_sent[2]+1)+')')
                self.message[i] = self.best_sent
        return self.message
        
    def receive(self, message_dict,trace,time):
        self.flag = False #This variable checks if there is any new message arriving at the bridge
        self.ports_copy = self.ports_type.copy()
        for i in self.neighbors:
            if ((self.ports_type[i]=='DP') or (self.ports_type[i]=='RP')): #If the port is not DP or RP, don't check it
                for j in message_dict[i]: 
                    if ((j!=[]) and (j!=self.best_sent)): #If the message is sent by the current bridge (the best_sent message), don't receive it
                        self.flag = True
                        if(j < self.best_received): #RP is just the best message which is received
                            self.rp = i
                            self.best_received = j
                        if trace:
                            print(str(time)+' r B'+str(self.n+1)+' (B'+str(j[0]+1)+','+str(j[1])+',B'+str(j[2]+1)+')')
        if(self.best_sent is not self.best_received): #Best sent is now updated according to the best received message
            self.best_sent = [self.best_received[0], self.best_received[1]+1, self.n]
        if(self.rp != ''):
            self.ports_copy[self.rp] = 'RP' #RP is also updated
        return