import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from lmfit import models

df = pd.read_csv("data/resonant_frequency_EOM.csv")
print(df)

plt.figure(figsize=(18, 10))
plt.plot(df["MHz"], df["mV"])
plt.ylabel(r'frequentie(MHz)')
plt.xlabel(r'Power(mV)')
plt.grid()
plt.tight_layout()
plt.show()