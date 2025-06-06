import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

z_0_0 = 1.08686031e+00
w_0 = 3.81104773e-04
z_r = np.pi*w_0**2/650e-9



wl = 650e-9

# focal length of first 2 and third lens
f = 0.15
f_2 = 0.5

# curvature of mirrors
radius = 1

# distance to lenses
d1 = 0.56
d2 = 0.86
d3 = 0.9
d4 = 1.30

# distance to mirrors
d_m1 = 1.5
d_m2 = 2

z01 = np.arange(0,d1,0.01)
z12 = np.arange(d1,d2+0.01,0.01)
z23 = np.arange(d2,d3,0.01)
z34 = np.arange(d3,d4,0.01)

q0 = complex(-z_0_0,z_r)
q1 = q0+d1
q2 = q1/(-q1/f+1)
q3 = q2+d2-d1
q4 = q3/(-q3/f+1)
q5 = q4+d3-d2
q6 = q5/(-q5/f_2+1)

# reflection at m2
q7 = q6 + d_m1 - d4
q8 = q7/(-q5/radius+1)


w0_2 = np.sqrt(q2.imag*wl/np.pi)
w0_3 = np.sqrt(q4.imag*wl/np.pi)
w0_4 = np.sqrt(q6.imag*wl/np.pi)

w0 = w_0*np.sqrt(1+((z01-z_0_0)**2/z_r**2))
w1 = w0_2*np.sqrt(1+((z12-d1+q2.real)**2/q2.imag**2))
w2 = w0_3*np.sqrt(1+((z23-d2+q4.real)**2/q4.imag**2))
w3 = w0_4*np.sqrt(1+((z34-d3+q6.real)**2/q6.imag**2))

print(min(w3))


plt.plot(z01,w0,'r')
plt.plot(z01,-w0,'r')
plt.fill_between(z01,w0,-w0,alpha=0.4,color='r')
plt.plot(z12,w1,'r')
plt.plot(z12,-w1,'r')
plt.fill_between(z12,w1,-w1,color='r',alpha=0.4)
plt.plot(z23,w2,'r')
plt.plot(z23,-w2,'r')
plt.fill_between(z23,w2,-w2,color='r',alpha=0.4)
plt.plot(z34,w3,'r')
plt.plot(z34,-w3,'r')
plt.fill_between(z34,w3,-w3,color='r',alpha=0.4)

plt.ylim(-0.00090,0.00090)
plt.xlim(0,1.50)

plt.xlabel("distance from fiber (m)")
plt.ylabel("beam size (m)")
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

z_0_0 = 1.08686031e+00
w_0 = 3.81104773e-04
z_r = np.pi*w_0**2/650e-9

f = 0.15
f_2 = 0.5

wl = 650e-9

d1 = 0.56
d2 = 0.86
d3 = 0.9
d4 = 1.30

z01 = np.arange(0,d1,0.01)
z12 = np.arange(d1,d2+0.01,0.01)
z23 = np.arange(d2,d3,0.01)
z34 = np.arange(d3,d4,0.01)

q0 = complex(-z_0_0,z_r)
q1 = q0+d1
q2 = q1/(-q1/f+1)
q3 = q2+d2-d1
q4 = q3/(-q3/f+1)
q5 = q4+d3-d2
q6 = q5/(-q5/f_2+1)

w0_2 = np.sqrt(q2.imag*wl/np.pi)
w0_3 = np.sqrt(q4.imag*wl/np.pi)
w0_4 = np.sqrt(q6.imag*wl/np.pi)

w0 = w_0*np.sqrt(1+((z01-z_0_0)**2/z_r**2))
w1 = w0_2*np.sqrt(1+((z12-d1+q2.real)**2/q2.imag**2))
w2 = w0_3*np.sqrt(1+((z23-d2+q4.real)**2/q4.imag**2))
w3 = w0_4*np.sqrt(1+((z34-d3+q6.real)**2/q6.imag**2))

print(min(w3))


plt.plot(z01,w0,'r')
plt.plot(z01,-w0,'r')
plt.fill_between(z01,w0,-w0,alpha=0.4,color='r')
plt.plot(z12,w1,'r')
plt.plot(z12,-w1,'r')
plt.fill_between(z12,w1,-w1,color='r',alpha=0.4)
plt.plot(z23,w2,'r')
plt.plot(z23,-w2,'r')
plt.fill_between(z23,w2,-w2,color='r',alpha=0.4)
plt.plot(z34,w3,'r')
plt.plot(z34,-w3,'r')
plt.fill_between(z34,w3,-w3,color='r',alpha=0.4)

plt.ylim(-0.00090,0.00090)
plt.xlim(0,1.50)

plt.xlabel("distance from fiber (m)")
plt.ylabel("beam size (m)")
plt.show()