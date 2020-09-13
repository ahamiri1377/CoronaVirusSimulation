import numpy as np

class Group():
    def __init__(self, depth, heal_prop, infection_prob, id):
        self.depth = depth
        self.S = np.random.uniform(0, 1, 1)
        self.next_S = self.S
        self.I = 1 - self.S
        self.next_I = self.I
        self.R = 0
        self.next_R = self.R
        self.in_touch_groups = []       
        self.heal_prob = heal_prop
        self.infection_prob = infection_prob
        self.id = id 
        if depth:
            self.child = []
        
    def state(self):
        if self.S >= self.I and self.S >= self.R:
            return 'S'
        elif self.I >= self.S and self.I >= self.S:
            return 'I'
        else:
            return 'R'

    def make_childs(self, n):
        for i in range(n):
            self.child.append(Group(self.depth - 1, self.heal_prob, self.infection_prob, i))

    def make_childs_in_touch(self):
        for c in self.child:
            for c_prime in self.child:
                if c != c_prime:
                    c.in_touch_groups.append(c_prime)

    def total_recovered(self):
        if self.depth:
            con = 0
            for c in self.child:
                con += c.total_recovered()
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
                con += c.total_infected()
            return con
        else:
            if self.state() == 'I':
                return 1
            else:
                return 0

    def update(self):
        self.S = self.next_S
        self.I = self.next_I
        self.R = self.next_R
        if self.depth:
            for c in self.child:
                c.update()

    def begin(self):
        if self.depth:
            self.make_childs(np.random.poisson(10))
            self.make_childs_in_touch()
            for c in self.child:
                c.begin()
    
    def pass_time(self, parent_infected):
        if self.state() == 'I':
            if np.random.binomial(1, self.heal_prob):
                self.next_S = self.S / 2
                self.next_I = self.I / 2
                self.next_R = (self.R + 1) / 2
        elif self.state() == 'R':
            if np.random.binomial(1, self.heal_prob):
                self.next_S = self.S / 2
                self.next_I = self.I / 2
                self.next_R = (self.R + 1) / 2
        else:
            for i in self.in_touch_groups:
                if i.state() == 'I':
                    if np.random.binomial(1, self.infection_prob):
                        self.next_S = (self.S + i.S) / 2
                        self.next_I = (self.I + i.I) / 2
                        self.next_R = (self.R + i.R) / 2
        if parent_infected == 'I':
            if not self.state() == 'R':
                if np.random.binomial(1, self.infection_prob):
                    self.next_S = self.S / 2
                    self.next_I = (self.I + 1) / 2
                    self.next_R = self.R / 2
        if self.depth:
            count = 0
            for c in self.child:
                c.pass_time(self.state())
                if c.state() == 'I':
                    count += 1
            if count >= len(self.child) / 2:
                self.next_S = self.S / 2
                self.next_I = (self.I + 1) / 2
                self.next_R = self.R / 2

    

    
