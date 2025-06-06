import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

distances = np.array([0.05,0.26,0.49,0.71,0.96])
wx = np.array([0.000692708,0.0005625,0.0005,0.000458333,0.000372396])
wx_err = np.full(len(wx),0.00002)
distance_err = np.full(len(distances),0.01)
print(distance_err)
def w(z,z0,w0):
    w_z = w0*np.sqrt(1+(z-z0)**2/(np.pi*w0**2/650e-9)**2)
    return w_z

popt, pcov = curve_fit(w,xdata=distances,ydata=wx,p0=[1,1],sigma=wx_err)
print(popt)
print(pcov)
print(np.sqrt(pcov[1][1]))

x = np.arange(0,2.5,0.01)
y = w(x,*popt)

plt.plot(x,y,'r')
plt.errorbar(distances,wx,fmt='bo',xerr=distance_err,yerr=wx_err)
plt.show()