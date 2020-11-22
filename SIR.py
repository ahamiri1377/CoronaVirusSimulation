from Classes import Group
from matplotlib import pyplot as plt
import numpy as np


res = []
depth, pr, pi, rate = 3, 0.03, 0.03, 3

for pr in range(1, 11):
    for pi in range(1, 11):
        infec_i = [0] * 1000
        rec_i = [0] * 1000
        t = [0] * 1000
        for counter in range(1):    
            g = Group(depth, pr / 50, pi / 50, 1, 0.01, 10)
            g.begin()
            g.first_child()
            size = g.size()
            print(str(pr) + '  ' + str(pi))
            for i in range(1000):
                g.pass_time(rate, False)
                g.update()
                t[i] = i + 1
                n = g.total_infected()
                # infec_i.append(n / size)
                infec_i[i] = (infec_i[i] * counter + n / size) / (counter + 1)
                n = g.total_recovered()
                # rec_i.append(n / size)
                rec_i[i] = (rec_i[i] * counter + n / size) / (counter + 1)
        res.append([pr, pi, max(infec_i), max(rec_i)])
        
np.savetxt("res_f.csv", np.asarray(res), delimiter=",")         


# infec_ii = [0] * 1000
# rec_ii = [0] * 1000

# for counter in range(1):    
#     g = Group(depth, pr, pi , 1, 0.01, 10)
#     g.begin()
#     g.first_child()
#     size = g.size()
#     print(str(pr) + '  ' + str(pi))
#     for i in range(1000):
#         # print(i + 1)
#         g.pass_time(rate, False)
#         # g.update_childs()
#         g.update()
#         # t.append(i + 1)
#         t[i] = i + 1
#         n = g.total_infected()
#         # infec_i.append(n / size)
#         infec_ii[i] = (infec_ii[i] * counter + n / size) / (counter + 1)
#         n = g.total_recovered()
#         # rec_i.append(n / size)
#         rec_ii[i] = (rec_ii[i] * counter + n / size) / (counter + 1)
        
        


    

# plt.plot(t, infec_i, '-', label='infected')
# plt.plot(t, rec_i, '-', label='recovered')
# plt.plot(t, infec_ii, '-', label='infected_p')
# plt.plot(t, rec_ii, '-', label='recovered_p')
# plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
# plt.title('Infected and Recovered')
# plt.xlabel('time')
# plt.ylabel('ratio')
# plt.text(800, 0.2, r'$P_I: $' + str(pi) + '\n' +r'$P_R:  $' + str(pr) + '\n' + r'$Depth:  $' + str(depth) + '\n' + r'$Size:  $' + str(size) + '\n' + r'$t-rate:  $' + str(rate))
# plt.show()

