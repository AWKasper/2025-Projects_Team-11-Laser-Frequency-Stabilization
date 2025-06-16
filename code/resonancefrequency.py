import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lmfit.model import Model

df = pd.read_csv("data/resonant_frequency_EOM.csv")
print(df)

plt.figure(figsize=(10, 6))
plt.plot(df["MHz"], df["mV"])
plt.ylabel(r"frequentie(MHz)")
plt.xlabel(r"Power(mV)")
plt.grid()
plt.ylim(8, 20)
plt.xlim(24.7, 25.8)
plt.legend()
plt.tight_layout()
plt.savefig("figures/frequency_plot.svg")

X = df["MHz"].values
y = df["mV"].values


# Inverted Gauss-functie definiëren
def inverted_gaussian(x, amplitude, center, sigma, offset):
    return -amplitude * np.exp(-((x - center) ** 2) / (2 * sigma**2)) + offset


model = Model(inverted_gaussian)

# Startwaarden voor de parameters schatten
params = model.make_params(
    amplitude=10,  # hoogte van de dip
    center=25.0,  # centrum van de dip
    sigma=0.1,  # breedte
    offset=np.max(y),  # basishoogte
)

result = model.fit(y, params, x=X)
print(result.fit_report())

# Fit-curve berekenen
x_fit = np.linspace(24, 27, 10000)
y_fit = result.eval(x=x_fit)

minimum_idx = np.where(y_fit == min(y_fit))

# Plot
plt.figure(figsize=(10, 6))
plt.plot(X, y, "bo", label="Data")
plt.plot(
    x_fit[minimum_idx],
    y_fit[minimum_idx],
    "ro",
    label=f"Minimum ({x_fit[minimum_idx]})",
)
plt.plot(x_fit, y_fit, "r-", label="Inverted Gauss Fit")
plt.xlabel("Frequentie (MHz)")
plt.ylabel("Signaal (mV)")
plt.title("Inverted Gaussian Fit")
plt.ylim(8, 28)
plt.xlim(24, 26.6)
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("figures/frequency_fit.svg")
