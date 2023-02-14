import numpy as np

def Question(fclass: np.array, fc_freq: np.array, wquadrat: float, lquadrat: float) -> None:
    
    """
    A function that takes in two one dimensional numpy arrays for fc_frequency classes and fc_frequencies, and two floats for
    length & width of quardat (in meters) and:
        - prints out the frequency & density of the given species
        - prints out the chi squared value
        - prints out the v/m value.
    """
    
    assert len(fclass) == len(fc_freq), "Argument arrays must be of equal lengths!."
    
    # area of the quadrat
    qarea = wquadrat * lquadrat
    
    # get the number of quadrats where the spcies was present and divide by the total number of quadrats
    _frequency = fc_freq[fclass != 0].sum() / fc_freq.sum() * 100
    print(f"Frequency: {_frequency}%.")
    print()
    
    # multiply the fc_frequency calss by fc_frequency and get the total of individuals, divide that number by the product of number of quadrats
    # and the area of the quadrat
    _density = (fclass * fc_freq).sum() / (qarea * fc_freq.sum())
    print(f"Density: {_density} individuals per square meter.")
    print()
    
    # chi square logic
    
    # population mean
    _mean = (fclass* fc_freq).sum() / fc_freq.sum()
    
    # probabilities for frequency classes
    prob = dict.fromkeys(fclass)
    
    # P = (e^(-m) * (m^n)) / n!
    for fc in prob.keys():
        prob[fc] = (np.power(np.e, (-1 * _mean)) * np.power(_mean, fc)) / np.math.factorial(fc)
    print("Probabilities")
    print("----------------------------------------------")
    for fc, _pr in prob.items():
        print(f"Frequency class {fc}: {_pr}.")
    print()
    
    # total number of quadrats
    N = fc_freq.sum()
    
    # (O - E)^2 / E value dict
    # O = P * N
    O_Esq_by_E = dict.fromkeys(fclass)
    
    for key in O_Esq_by_E.keys():
        O = fc_freq[key]
        E = (N * prob.get(key))
        O_Esq_by_E[key] = np.square(O - E) / E
    
    print("(O - E)^2 / E values")
    print("----------------------------------------------")
    for fc, val in O_Esq_by_E.items():
        print(f"Frequency class {fc}: {val}.")
    print()
    
    print(f"Chi squared value: {sum(O_Esq_by_E.values())}.")
    print()
    
    # v/m logic
    
    # variance v = {Sum(x^2) - {(Sum(x))^2 / N} / (N - 1)}
    raw_freq = np.repeat(fclass, fc_freq)  # x
    raw_freq_sq = np.square(raw_freq)  # x^2
    variance = (raw_freq_sq.sum() - (np.square(raw_freq.sum()) / N)) / (N - 1)
    voverm = variance / _mean
    print(f"v/m value: {voverm}.")
    print()
    
    # t statistics
    
    # standard error
    se = np.sqrt(2 / (N - 1))
    tcalc = (voverm - 1) / se
    print(f"Calculated t value: {tcalc}.")
    print()
    print()
   
# print("Test") 
# Question(fclass = np.arange(0, 4), fc_freq = np.array([28, 18, 3, 1]), lquadrat = 1.5, wquadrat = 1.5)

print("2018 ICA")
Question(fclass = np.arange(0, 3), fc_freq = np.array([25, 19, 6]), lquadrat = 0.5, wquadrat = 0.5)
print("2019 ECE")
Question(fclass = np.arange(0, 4), fc_freq = np.array([15, 9, 5, 1]), lquadrat = 0.5, wquadrat = 0.5)
print("2017 ECE")
Question(fclass = np.arange(0, 4), fc_freq = np.array([46, 34, 14, 6]), lquadrat = 0.3, wquadrat = 0.3)
print("2015 ECE")
Question(fclass = np.arange(0, 4), fc_freq = np.array([25, 19, 5, 1]), lquadrat = 0.5, wquadrat = 0.5)