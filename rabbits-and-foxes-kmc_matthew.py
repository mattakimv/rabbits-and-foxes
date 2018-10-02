
# coding: utf-8

# # Rabbits and foxes
# 
# There are initially 400 rabbits and 200 foxes on a farm (but it could be two cell types in a 96 well plate or something, if you prefer bio-engineering analogies). Plot the concentration of foxes and rabbits as a function of time for a period of up to 600 days. The predator-prey relationships are given by the following set of coupled ordinary differential equations:
# 
# \begin{align}
# \frac{dR}{dt} &= k_1 R - k_2 R F \tag{1}\\
# \frac{dF}{dt} &= k_3 R F - k_4 F \tag{2}\\
# \end{align}
# 
# * Constant for growth of rabbits $k_1 = 0.015$ day<sup>-1</sup>
# * Constant for death of rabbits being eaten by foxes $k_2 = 0.00004$ day<sup>-1</sup> foxes<sup>-1</sup>
# * Constant for growth of foxes after eating rabbits $k_3 = 0.0004$ day<sup>-1</sup> rabbits<sup>-1</sup>
# * Constant for death of foxes $k_4 = 0.04$ day<sup>-1</sup>
# 
# *This problem is based on one from Chapter 1 of H. Scott Fogler's textbook "Essentials of Chemical Reaction Engineering".*
# 

# In[358]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
from matplotlib import pyplot as plt

import random


# # Now let's try some Kinetic Monte Carlo

# We wish to implement a Kinetic Monte Carlo algorithm to simulate the same situation. See https://en.wikipedia.org/wiki/Kinetic_Monte_Carlo for details.
# 
# We'll assume the numbers of rabbits and foxes (starting at 400 and 200) are actual rabbits and foxes, not "rabbit densities" for example, and so must always remain integers: you can't have half a rabbit or half a fox.
# 
# There are four events, with rates that are straightforward to calculate, so the rejection-free algorithm is suitable:
# * `rabbit_birth = k1 * rabbits`
# * `rabbit_death = k2 * rabbits * foxes`
# * `fox_birth = k3 * rabbits * foxes`
# * `fox_death = k4 * foxes`
# 
# 
# Use a Kinetic Monte Carlo simulation(s) running for 600 days to determine
# 1. The expected location of the second peak in foxes (eg. 425 days, 2800 foxes), on occasions that there is one (eg. if there's a peak that's  >200 days and >100 foxes)
# 2. The interquartile range of the second peak in foxes (eg. 411-443 days, 2700-3120 foxes).
# 3. The probability that the foxes die out before 600 days are complete
# 
# Make sure you've done enough simulations to be suitably confident in your answers (given the precision you think appropriate).

# # Your turn!

# In[411]:


random.seed(1) # so results don't change every time I execute
np.random.seed(1) # same thing for numpy

final_time = 600
k1 = 0.015   ### day^-1
k2 = 0.00004 ### day^-1 foxes^-1
k3 = 0.0004  ### day^-1 rabbit^-1
k4 = 0.04    ### day^-1

runs = 100
dead_zorros = 0
peak_t=[]
peak_F=[]

mean_t=[]
mean_F=[]

upper_quartile_t=[]
lower_quartile_t=[]
upper_quartile_F=[]
lower_quartile_F=[]





k=0
for i in range(runs):
    print(i)
    ### step 1
    to = 0
    t =[]
    t.append(to)

    ### step 2
    Ro = 400
    R=[]
    R.append(Ro)
    Fo = 200
    F=[]
    F.append(Fo)




    ###step 10
    while t[-1] < final_time:
        ###step 3
        dRb_dt = k1*R[-1]
        dRd_dt = k2*R[-1]*F[-1]
        dFb_dt = k3*R[-1]*F[-1]
        dFd_dt = k4*F[-1]

        ###step 4
        #rates = np.stack((dRb_dt,dRd_dt,dFb_dt,dFd_dt))
        #Q = sum(rates)
        Q = dRb_dt + dRd_dt + dFb_dt + dFd_dt

        ###step 5
        uQk = random.uniform(0, Q)
        ###step 6
        Rb = dRb_dt
        Rd = dRb_dt + dRd_dt
        Fb = dRb_dt + dRd_dt + dFb_dt
        Fd = dRb_dt + dRd_dt + dFb_dt + dFd_dt


        ###step 7
        if uQk < Rb:
            R.append(R[-1]+1)
            F.append(F[-1])
            t.append(dt+t[-1])
        if uQk > Rb and uQk < Rd:
            R.append(R[-1]-1)
            F.append(F[-1])
            t.append(dt+t[-1])
        if uQk >Rd and uQk <  Fb:
            R.append(R[-1])
            F.append(F[-1]+1)
            t.append(dt+t[-1])
        if uQk >Fb:
            R.append(R[-1])
            F.append(F[-1]-1)
            t.append(dt+t[-1])

        ###step 8 and 9
        dt = random.expovariate(Q)
        
    t = np.array(t)
    R = np.array(R)
    F = np.array(F)
    
    if F[-1]==0:
        dead_zorros = dead_zorros +1


    plt.figure(0)
    plt.plot(t,F*(t>200)*(F>100))
    i = np.argmax(F*(t>200)*(F>100))
    if i:
        peak_t.append(t[i])
        peak_F.append(F[i])
        
    if len(peak_t)>0:
        mean_t.append(np.mean(peak_t))
        mean_F.append(np.mean(peak_F))
        upper_quartile_t.append(np.percentile(peak_t,75))
        lower_quartile_t.append(np.percentile(peak_t,25))
        upper_quartile_F.append(np.percentile(peak_F,75))
        lower_quartile_F.append(np.percentile(peak_F,25))       
        
        

zorros = dead_zorros/runs
zorros = zorros*100
print('The probability all foxes die is %.2f' %zorros) 


# In[416]:


plt.semilogx(mean_t,'-r')
plt.semilogx(upper_quartile_t,':r')
plt.semilogx(lower_quartile_t,':r')
plt.ylabel('Second peak time (days)')
plt.xlim(10)
plt.ylabel('Runs')


# In[417]:


plt.semilogx(mean_F,'-k')
plt.semilogx(upper_quartile_F,':k')
plt.semilogx(lower_quartile_F,':k')
plt.ylabel('Second peak foxes')
plt.xlim(10)
plt.xlabel('Runs')


# In[418]:


from matplotlib.colors import LogNorm
plt.hist2d(peak_t,peak_F, bins=40, norm=LogNorm())
plt.xlim(0,600)
plt.ylim(0)
plt.colorbar()
plt.axvline(200,linestyle=':')
plt.axvline(mean_t[-1],color='r')
plt.axhline(100,linestyle=':')
plt.axhline(mean_F[-1],color='k')
plt.show()

