import numpy as np

class Group():
    def __init__(self, depth, heal_prop, infection_prob, id):
        self.depth = depth
        q = np.random.binomial(1, 0.9)
        self.S = q * np.random.uniform(0.8, 1, 1)[0] + (1 - q) * np.random.uniform(0, 0.2, 1)[0]
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
        elif self.I >= self.S and self.I >= self.R:
            return 'I'
        else:
            return 'R'

    def make_childs(self, n):
        for i in range(n):
            self.child.append(Group(self.depth - 1, self.heal_prob, self.infection_prob, i))

    def make_childs_in_touch(self):
        if self.depth:
            for c in self.child:
                for c_prime in self.child:
                    if c != c_prime:
                        c.in_touch_groups.append(c_prime)

    def total_recovered(self):
        if self.depth:
            con, cont = 0, 0
            for c in self.child:
                n, m = c.total_recovered()
                con += n
                cont += m
            return con, cont
        else:
            if self.state() == 'R':
                return 1, self.R
            else:
                return 0, self.R

    def total_infected(self):
        if self.depth:
            con, cont = 0, 0
            for c in self.child:
                n, m = c.total_infected()
                con += n
                cont += m
            return con, cont
        else:
            if self.state() == 'I':
                return 1, self.I
            else:
                return 0, self.I
    
    def size(self):
        if self.depth == 1:
            return len(self.child)
        elif self.depth > 1:
            con = 0
            for c in self.child:
                con += c.size()
            return con


    def update(self):
        self.S = self.next_S
        self.I = self.next_I
        self.R = self.next_R
        if self.depth:
            for c in self.child:
                c.update()

    def begin(self):
        if self.depth:
            self.make_childs(np.random.poisson(30))
            self.make_childs_in_touch()
            for c in self.child:
                c.begin()
    
    def pass_time(self, parent_S, parent_I, parent_R):
        if self.depth:
            count = 0
            for c in self.child:
                c.pass_time(self.S, self.I, self.R)
                if c.state() == 'I':
                    count += 1
            if not self.state() == 'R':
                if count / len(self.child) > self.I:
                    self.next_I = (count / len(self.child) + self.I) / 2
                    self.next_S = self.S - (self.next_I - self.I)

        if self.I < parent_I:
            if np.random.binomial(1, self.infection_prob):
                    self.next_S = (self.S + parent_S) / 2
                    self.next_I = (self.I + parent_I) / 2
                    self.next_R = (self.R + parent_R) / 2

        if not self.state() =='R':
            for i in self.in_touch_groups:
                if self.I < i.I:
                    if np.random.binomial(1, self.infection_prob):
                        self.next_S = (self.S + i.S) / 2
                        self.next_I = (i.I + self.I) / 2
                        self.next_R = (self.R + i.R) / 2
        if self.state() == 'I':
            if np.random.binomial(1, self.heal_prob):
                self.next_S = self.S / 2
                self.next_I = self.I / 2
                self.next_R = 1 - self.next_I - self.next_S
        if self.state() == 'R':
            if np.random.binomial(1, self.heal_prob):
                self.next_S = self.S / 2
                self.next_I = self.I / 2
                self.next_R = (self.R + 1) / 2
        
        