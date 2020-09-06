from Classes import City
from matplotlib import pyplot as plt

def check(pi, pr, city_number, iter):
    cities = []
    for i in range(city_number):
        c = City(pi, pr, i)
        c.begin()
        cities.append(c)

    #  make_country_in_touch
    for city in cities:
        for in_touch_city in cities:
            if city != in_touch_city:
                city.in_touch_cities.append(in_touch_city)

    s = 0
    for q in cities:
        s += q.size()
    print(s)

    it = []
    numb = []
    num = []

    for i in range(iter):
        for c in cities:
            c.pass_time()
        con ,conn = 0, 0
        for cc in cities:
            cc.update()
            con += cc.total_recovered()
            conn += cc.total_infection()
        
    if con >= 0.9 * s:
        return True
    else:
        return False

        


city_number = 10
tup1 = []
tup2 = []
for i in range(40):
    beg = 0
    end = 100
    while(end - beg >= 1):
        if check(i / 200, (end + beg) / 200, 5, 300):
            beg = (beg + end) / 2
        else:
            end = (beg + end) / 2
    print(str(i) + " , " + str(end))
    tup1.append(i / 200)
    tup2.append(end / 100)
    

plt.plot(tup1, tup2, '-')
plt.title('P_I vs P_R')
plt.xlabel('P_I')
plt.ylabel('P_R')
# plt.text(max(tup1) / 10, max(tup2) / 2, r'$P_I: $' + str(pi) +r'$\ \  P_R:  $' + str(pr))
plt.show()

# plt.plot(it, numb, '.')
# plt.title('Recovery')
# plt.xlabel('time')
# plt.ylabel('recovered ratio')
# plt.text(800, max(numb) / 2, r'$P_I: $' + str(pi) +r'$\ \  P_R:  $' + str(pr))
# plt.show()

# plt.plot(it, num, '.')
# plt.title('Infection')
# plt.xlabel('time')
# plt.ylabel('infected ratio')
# plt.text(800, max(num) / 2, r'$P_I: $' + str(pi) +r'$\ \  P_R:  $' + str(pr))

# plt.show()
