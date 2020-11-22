import numpy as np

class Group():
    def __init__(self, depth, heal_prop, infection_prob, id, infected_perc, childs_numb):
        self.depth = depth
        self.childs_numb = childs_numb
        self.infected_perc = infected_perc
        self.S = 1
        self.I = 0
        self.R = 0
        self.next_S = 1
        self.next_I = 0
        self.next_R = 0
        self.heal_prob = heal_prop
        self.infection_prob = infection_prob
        self.id = id      
        if depth:
            self.child = []
            self.childs_in_touch = []
        else:
            self.S = np.random.binomial(1, 1 - infected_perc)
            self.next_S = self.S
            self.I = 1 - self.S
            self.next_I = self.I
            self.R = 0
            self.next_R = 0
        
    def state(self):
        if self.S >= self.I and self.S >= self.R:
            return 'S'
        elif self.I >= self.S and self.I >= self.R:
            return 'I'
        else:
            return 'R'

    def make_childs(self):
        for i in range(self.childs_numb):
            self.child.append(Group(self.depth - 1, self.heal_prob, self.infection_prob, i, self.infected_perc, self.childs_numb))

    def set_state(self):
        if self.depth:
            cous_S, cous_I, cous_R = 0, 0, 0
            for c in self.child:
                if c.state() == 'S':
                    cous_S += 1
                if c.state() == 'I':
                    cous_I += 1
                if c.state() == 'R':
                    cous_R += 1
            self.S = cous_S / self.childs_numb
            self.I = cous_I / self.childs_numb
            self.R = cous_R / self.childs_numb
                 

    def make_childs_in_touch(self):
        if self.depth:
            self.childs_in_touch = []
            for i in range(len(self.child)):
                for j in range(i + 1, len(self.child)):
                    self.childs_in_touch.append((self.child[i], self.child[j]))
            
    def total_recovered(self):
        if self.depth:
            con = 0
            for c in self.child:
                n = c.total_recovered()
                con += n
            return con
        else:
            if self.state() == 'R':
                return 1
            else:
                return 0

    def total_infected(self):
        if self.depth:
            con = 0
            for c in self.child:
                n = c.total_infected()
                con += n
            return con
        else:
            if self.state() == 'I':
                return 1
            else:
                return 0
    
    def size(self):
        if self.depth == 1:
            return len(self.child)
        elif self.depth > 1:
            con = 0
            for c in self.child:
                con += c.size()
            return con


    def update(self):
        if self.depth:
            if self.depth == 1:
                for c in self.child:
                    c.S = c.next_S
                    c.I = c.next_I
                    c.R = c.next_R
            else:            
                for c in self.child:
                    c.update()

    def begin(self):
        if self.depth:
            self.make_childs()
            self.make_childs_in_touch()
            self.set_state()
            for c in self.child:
                c.begin()
    
    def first_child(self):    
        if self.depth > 1:
            for c in self.child:
                c.first_child()
        elif self.depth == 1:
            if self.id == 1:
                # print('check')
                for c in self.child:
                    c.S, c.next_S = 0, 0
                    c.I, c.next_I = 1, 1
                    c.R, c.next_R = 0, 0
        
    
    def update_childs(self):
        if self.depth:
            self.make_childs_in_touch()
            self.set_state()
            for c in self.child:
                c.update_childs()

    def ret_nei(self, c, cs):
        rs = []
        for i in cs:
            if c == i[0]:
                rs += [i[1]]
            if c == i[1]:
                rs += [i[0]]
        return rs

    def nei_check(self, c, s, cs):
        for q in cs:
            if (c == q[0] and s == q[1]) or (c == q[1] and s == q[0]):
                return True
            else:
                return False 
    
    def pass_time(self, c_rate, is_transfer):
        if self.depth == 1:
            for c in range(len(self.child)):
                if self.child[c].S == 1:
                    rs = self.ret_nei(self.child[c], self.childs_in_touch)
                    for r in rs:
                        if r.I == 1:
                            if np.random.binomial(1, self.infection_prob):
                                self.child[c].next_S = 0
                                self.child[c].next_I = 1

            for c in range(len(self.child)):
                if self.child[c].I == 1:
                    if np.random.binomial(1, self.heal_prob):
                        self.child[c].next_I = 0
                        self.child[c].next_R = 1
                
        if self.depth > 1:
            for c in self.child:
                c.pass_time(c_rate, is_transfer)
        
                
        if is_transfer:
            if self.depth > 1:
                for c in range(len(self.child)):
                    for cc in range(len(self.child)):
                        if self.nei_check(self.child[c], self.child[cc], self.childs_in_touch) and c != cc:
                            if self.child[c].S > self.child[cc].S:
                                rate = (self.child[c].S - self.child[cc].S) * self.childs_numb * c_rate
                                counter = 0
                                qs = []
                                for q in range(len(self.child[c].child)):
                                    if self.child[c].child[q].state() == 'S' and rate > counter:
                                        counter += 1
                                        self.child[cc].child.append(self.child[c].child[q])
                                        qs += [q]
                                        # if counter > rate:
                                        #     break
                                qs.reverse()
                                for q in qs:
                                    del(self.child[c].child[q])
                                self.update_childs()
                            else:
                                rate = (self.child[cc].S - self.child[c].S) * self.childs_numb * c_rate
                                counter = 0
                                qs = []
                                for q in range(len(self.child[cc].child)):
                                    if self.child[cc].child[q].state() == 'S' and rate > counter:
                                        counter += 1
                                        self.child[c].child.append(self.child[cc].child[q])
                                        qs += [q]
                                        if counter > rate:
                                            break
                                qs.reverse()
                                for q in qs:
                                    del(self.child[cc].child[q])
                                self.update_childs()

                            if self.child[c].I > self.child[cc].I:
                                rate = (self.child[c].I - self.child[cc].I) * self.childs_numb * c_rate
                                counter = 0
                                qs = []
                                for q in range(len(self.child[c].child)):
                                    if self.child[c].child[q].state() == 'I' and rate > counter:
                                        counter += 1
                                        self.child[cc].child.append(self.child[c].child[q])
                                        qs += [q]
                                        if counter > rate:
                                            break
                                qs.reverse()
                                for q in qs:
                                    del(self.child[c].child[q])
                                self.update_childs()
                            else:
                                rate = (self.child[cc].I - self.child[c].I) * self.childs_numb * c_rate
                                counter = 0
                                qs = []
                                for q in range(len(self.child[cc].child)):
                                    if self.child[cc].child[q].state() == 'I' and rate > counter:
                                        counter += 1
                                        self.child[c].child.append(self.child[cc].child[q])
                                        qs += [q]
                                        if counter > rate:
                                            break
                                qs.reverse()
                                for q in qs:
                                    del(self.child[cc].child[q])
                                self.update_childs()
                            
                            if self.child[c].R > self.child[cc].R:
                                rate = (self.child[c].R - self.child[cc].R) * self.childs_numb * c_rate
                                counter = 0
                                qs = []
                                for q in range(len(self.child[c].child)):
                                    if self.child[c].child[q].state() == 'R' and rate > counter:
                                        counter += 1
                                        self.child[cc].child.append(self.child[c].child[q])
                                        qs += [q]
                                        if counter > rate:
                                            break
                                qs.reverse()
                                for q in qs:
                                    del(self.child[c].child[q])
                                self.update_childs()
                            else:
                                rate = (self.child[cc].R - self.child[c].R) * self.childs_numb * c_rate
                                counter = 0
                                qs = []
                                for q in range(len(self.child[cc].child)):
                                    if self.child[cc].child[q].state() == 'R' and rate > counter:
                                        counter += 1
                                        self.child[c].child.append(self.child[cc].child[q])
                                        qs += [q]
                                        if counter > rate:
                                            break
                                qs.reverse()
                                for q in qs:
                                    del(self.child[cc].child[q])          
                                self.update_childs()          

    def print_gp(self):
        if self.depth:
            print('Depth:  ' + str(self.depth) + '   parent id:  ' + str(self.id))
            for c in self.child:
                c.print_gp()
        else:
            print('id:  '  + str(self.id) + '  S:  ' + str(self.S))
