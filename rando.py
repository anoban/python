import numpy as np

np.set_printoptions(
    precision=5,
    floatmode="fixed",
    threshold=np.inf,
    formatter={"float": lambda value: f"{value:3.6f}"},
)
x = np.random.normal(loc=15.0, scale=25.0, size=5000)

x

np.flip(np.sort(x))
