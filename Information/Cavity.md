We have to construct the desired cavity mode for the pound-drever-hall setup.

Steps to be taken:

-Model free space propogation and lens propogation in python
-Place first lens in setup at a fixed distance, and the second lens 30 cm further than that
-Find the location of the third lens with a simple optimization algorithm.
-Find the location of the mirrors with the same simple optimization algorithm
-Confirm that our setup is valid under the stability criterion: 0 < (1-R/L)^2 < 1. Where L is the cavity length and R is the radius of the mirrors. (Where does the stability criterion come from? Why can setups outside of these parameters not be stable?)



How big can the 'error' be in the distancing of our cavity?

What different modes can we have in our cavity?

Is a confocal setup desirable? Can we find a setup that works with a confocal setup?
- Confocal means the mirror are exactly one mirror radius apart (For our mirror this distance is 200mm)
- This is conform the stability criterion


Stability criterion:
![image](https://github.com/user-attachments/assets/acac4fb8-a303-4858-8b2e-53f7f03fd40c)
This image shows the possible stable setups and how they look in a cavity.


For cavities we also have two parameters: Finesse and FSR (Free spectral range)

We can calculate the Finesse with just the reflection coefficient of the mirror [formula](https://www.rp-photonics.com/finesse.html)

We can calculate the Free spectral range with only the length of the cavity [formula](https://www.rp-photonics.com/free_spectral_range.html)

(Why do we care about the finesse and the FSR? It tells us things about about our transimissivity peaks, a way to tell when you are in resonance, we want these to be spaced apart and thin. High finesse makes the transmissivity peaks thinner, and a high FSR makes them further apart.)


