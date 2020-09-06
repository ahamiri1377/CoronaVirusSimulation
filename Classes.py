import numpy as np

class Person():
    def __init__(self, is_infected, id):
        self.is_infected = is_infected
        self.is_infected_next = is_infected
        self.id = id
        self.is_heal = False
        self.is_heal_next = False
        self.in_touch = []
        self.is_working = np.random.binomial(1, 0.5)

    def pass_time(self, heal_prob, infection_prob, family_infected):
        if not self.is_heal:
            if self.is_infected:
                if np.random.binomial(1, heal_prob):
                    self.is_heal_next = True
                    self.is_infected_next = False
            else:
                for i in self.in_touch:
                    if i.is_infected:
                        if np.random.binomial(1, infection_prob):
                            self.is_infected_next = True
        if family_infected:
            if not self.is_heal:
                if np.random.binomial(1, infection_prob):
                    self.is_infected_next = True

    def update(self):
        self.is_heal = self.is_heal_next
        self.is_infected = self.is_infected_next
    

class Family():
    def __init__(self, infection_prob, heal_prob, id):
        self.id = id
        self.is_infected = False
        self.is_infected_next = False
        self.is_heal = False
        self.is_heal_next = False
        self.infection_prob = infection_prob
        self.heal_prob = heal_prob
        self.persons = []
        self.in_touch_families = []

    def make_family(self, number):
        for i in range(number):
            self.persons.append(Person(np.random.binomial(1, 0.05), i + 1))
    
    def make_family_in_touch(self):
        for person in self.persons:
            for in_touch_person in self.persons:
                if person != in_touch_person:
                    person.in_touch.append(in_touch_person)

    def set_in_touch_families(self, families):
        self.in_touch_families = families

    def total_recovered(self):
        count = 0
        for p in self.persons:
            if p.is_heal:
                count += 1
        return count

    def total_infection(self):
        count = 0
        for p in self.persons:
            if p.is_infected:
                count += 1
        return count
    
    def size(self):
        return len(self.persons)


    def pass_time(self, neighborhood_infected):
        count = 0
        for p in self.persons:
            p.pass_time(self.heal_prob, self.infection_prob, self.is_infected)
            if p.is_infected:
                count += 1
        if count >= len(self.persons) / 2:
            self.is_infected_next = True
        else:
            self.is_infected_next = False
        
        for f in self.in_touch_families:
            if f.is_infected:
                if np.random.binomial(1, self.infection_prob):
                    self.is_infected_next = True

        if neighborhood_infected:
            if np.random.binomial(1, self.infection_prob):
                self.is_infected_next = True

    def update(self):
        self.is_infected = self.is_infected_next
        for p in self.persons:
            p.update()
    

    def begin(self):
        self.make_family(np.random.poisson(5))
        self.make_family_in_touch()
        
    

class Neighborhood():
    def __init__(self, infection_prob, heal_prob, id):
        self.infection_prob = infection_prob
        self.is_heal = False
        self.is_heal_next = False
        self.is_infected = False
        self.is_infected_next = False
        self.heal_prob = heal_prob
        self.families = []
        self.in_touch_neighborhoods = []
        self.id = id

    def make_neighborhood(self, family_number):
        for i in range(family_number):
            self.families.append(Family(self.infection_prob, self.heal_prob, i + 1))

    def make_neighborhood_in_touch(self):
        for family in self.families:
            for in_touch_family in self.families:
                if family != in_touch_family:
                    family.in_touch_families.append(in_touch_family)

    def set_in_touch_neighborhoods(self, neighborhoods):
        self.in_touch_neighborhoods = neighborhoods


    def total_recovered(self):
        count = 0
        for f in self.families:
            count += f.total_recovered()
        return count

    def total_infection(self):
        count = 0
        for f in self.families:
            count += f.total_infection()
        return count

    
    def pass_time(self, city_infected):
        count = 0
        for f in self.families:
            f.pass_time(self.is_infected)
            if f.is_infected:
                count += 1
        if count >= len(self.families) / 2:
            self.is_infected_next = True
        else:
            self.is_infected_next = False
        for n in self.in_touch_neighborhoods:
            if n.is_infected:
                if np.random.binomial(1, self.infection_prob):
                    self.is_infected_next = True

        if city_infected:
            if np.random.binomial(1, self.infection_prob):
                self.is_infected_next = True

    def update(self):
        self.is_infected = self.is_infected_next
        for f in self.families:
            f.update()
    
    def size(self):
        co = 0
        for i in self.families:
            co += i.size()
        return co

    def begin(self):
        self.make_neighborhood(np.random.poisson(10))
        self.make_neighborhood_in_touch()
        for f in self.families:
            f.begin()


class City():
    def __init__(self, infection_prob, heal_prob, id):
        self.infection_prob = infection_prob
        self.is_infected = False
        self.is_infected_next = False
        self.is_heal = False
        self.is_heal_next = False
        self.heal_prob = heal_prob
        self.neighborhoods = []
        self.in_touch_cities = []
        self.id = id

    def make_city(self, neighborhoods_number):
        for i in range(neighborhoods_number):
            self.neighborhoods.append(Neighborhood(self.infection_prob, self.heal_prob, i + 1))

    def make_city_in_touch(self):
        for neighbor in self.neighborhoods:
            for in_touch_neighbor in self.neighborhoods:
                if neighbor != in_touch_neighbor:
                    neighbor.in_touch_neighborhoods.append(in_touch_neighbor)

    def set_in_touch_cities(self, cities):
        self.in_touch_cities = cities


    def total_recovered(self):
        count = 0
        for n in self.neighborhoods:
            count += n.total_recovered()
        return count

    def total_infection(self):
        count = 0
        for n in self.neighborhoods:
            count += n.total_infection()
        return count

    
    def begin(self):
        self.make_city(np.random.poisson(10))
        self.make_city_in_touch()
        for n in self.neighborhoods:
            n.begin()

    def pass_time(self):
        count = 0
        for n in self.neighborhoods:
            n.pass_time(self.is_infected)
            if n.is_infected:
                count += 1
        if count >= len(self.neighborhoods) / 2:
            self.is_infected_next = True
        else:
            self.is_infected_next = False
        for c in self.in_touch_cities:
            if c.is_infected:
                if np.random.binomial(1, self.infection_prob):
                    self.is_infected_next = True

    def update(self):
        self.is_infected = self.is_infected_next
        for n in self.neighborhoods:
            n.update()
    

    def size(self):
        co = 0
        for i in self.neighborhoods:
            co += i.size()
        return co
    


# class Workplace():
#     def __init__(self, infection_prob, heal_prob, id):
#         self.infection_prob = infection_prob
#         self.heal_prob = heal_prob
#         self.persons = []
#         self.in_touch_workplaces = []
#         self.id = id

#     def make_workplaces(self, emp_number):
        