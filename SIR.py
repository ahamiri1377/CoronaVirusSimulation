from Classes import Group
from matplotlib import pyplot as plt

# def check(pi, pr, city_number, iter):
#     cities = []
#     for i in range(city_number):
#         c = City(pi, pr, i)
#         c.begin()
#         cities.append(c)

#     #  make_country_in_touch
#     for city in cities:
#         for in_touch_city in cities:
#             if city != in_touch_city:
#                 city.in_touch_cities.append(in_touch_city)

#     s = 0
#     for q in cities:
#         s += q.size()
#     print(s)

#     it = []
#     numb = []
#     num = []

#     for i in range(iter):
#         for c in cities:
#             c.pass_time()
#         con ,conn = 0, 0
#         for cc in cities:
#             cc.update()
#             con += cc.total_recovered()
#             conn += cc.total_infection()
        
#     if con >= 0.9 * s:
#         return True
#     else:
#         return False

        


# city_number = 10
# tup1 = []
# tup2 = []
# for i in range(40):
#     beg = 0
#     end = 100
#     while(end - beg >= 1):
#         if check(i / 200, (end + beg) / 200, 5, 300):
#             beg = (beg + end) / 2
#         else:
#             end = (beg + end) / 2
#     print(str(i) + " , " + str(end))
#     tup1.append(i / 200)
#     tup2.append(end / 100)
    

infec_i = []
infec_t = []
rec_i = []
rec_t = []

depth = int(input())
pr = float(input())
pi = float(input())
g = Group(depth, pr, pi, 1)
g.begin()
size = g.size()
for i in range(2000):
    print(i + 1)
    g.pass_time(1, 0, 0)
    g.update()
    t.append(i + 1)
    n, m = g.total_infected()
    infec_i.append(n / size)
    infec_t.append(m / size)
    n, m = g.total_recovered()
    rec_i.append(n / size)
    rec_t.append(m / size)
    
    

plt.plot(t, infec_i, '-', label='infected')
plt.plot(t, rec_i, '-', label='recovered')
plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
plt.title('Infected and Recovered')
plt.xlabel('time')
plt.ylabel('ratio')
plt.text(1500, 0.5, r'$P_I: $' + str(pi) +r'$\ \  P_R:  $' + str(pr) + r'$\ \  Depth:  $' + str(depth) + r'$\ \  Size:  $' + str(size))
plt.show()

plt.plot(t, infec_t, '-', label='infected')
plt.plot(t, rec_t, '-', label='recovered')
plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
plt.title('Infected and Recovered')
plt.xlabel('time')
plt.ylabel('ratio')
plt.text(1500, 0.5, r'$P_I: $' + str(pi) +r'$\ \  P_R:  $' + str(pr) + r'$\ \  Depth:  $' + str(depth) + r'$\ \  Size:  $' + str(size))
plt.show()

plt.plot(t, infec_i, '-', label='infected-1')
plt.plot(t, rec_i, '-', label='recovered-1')
plt.plot(t, infec_t, '-', label='infected-2')
plt.plot(t, rec_t, '-', label='recovered-2')
plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
plt.title('Infected and Recovered')
plt.xlabel('time')
plt.ylabel('ratio')
plt.text(1500, 0.5, r'$P_I: $' + str(pi) +r'$\ \  P_R:  $' + str(pr) + r'$\ \  Depth:  $' + str(depth) + r'$\ \  Size:  $' + str(size))
plt.show()




