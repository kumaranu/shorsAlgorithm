import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram
from math import gcd
from numpy.random import randint
import pandas as pd
from fractions import Fraction

def c_amod15(a, power):
    """Controlled multiplication by a mod 15"""
    if a not in [2, 7, 8, 11, 13]:
        raise ValueError("'a' must be 2,7,8,11 or 13")
    U = QuantumCircuit(4)
    for iteration in range(power):
        if a in [2, 13]:
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        if a in [7, 8]:
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        if a == 11:
            U.swap(1, 3)
            U.swap(0, 2)
        if a in [7, 11, 13]:
            for q in range(4):
                U.x(q)
    U = U.to_gate()
    U.name = "%i^%i mod 15" % (a, power)
    c_U = U.control()
    return c_U

def qft_dagger(n):
    """n-qubit QFTdagger the first n qubits in circ"""
    qc = QuantumCircuit(n)
    # Don't forget the Swaps!
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)
    qc.name = "QFT†"
    return qc

def a2jmodN(a, j, N):
    """Compute a^{2^j} (mod N) by repeated squaring"""
    for i in range(j):
        a = np.mod(a**2, N)
    return a

def qpe_amod15(a,n_count):
    qc = QuantumCircuit(4+n_count, n_count)
    for q in range(n_count):
        qc.h(q)     # Initialize counting qubits in state |+>
    qc.x(3+n_count) # And auxiliary register in state |1>
    for q in range(n_count): # Do controlled-U operations
        qc.append(c_amod15(a, 2**q),
                  [q] + [i+n_count for i in range(4)])
    qc.append(qft_dagger(n_count), range(n_count)) # Do inverse-QFT
    qc.measure(range(n_count), range(n_count))
    qc.draw(fold=-1, output='mpl')  # -1 means 'do not fold'
    #qc.draw(fold=-1, output='latex')  # -1 means 'do not fold'
    plt.show()
    #qc.draw(output='mpl', filename='shorsAlgoCircuit.png')  # -1 means 'do not fold'

    # Simulate Results
    aer_sim = Aer.get_backend('aer_simulator')
    # Setting memory=True below allows us to see a list of each sequential reading
    t_qc = transpile(qc, aer_sim)
    qobj = assemble(t_qc, shots=1)
    result = aer_sim.run(qobj, memory=True).result()
    readings = result.get_memory()
    print("Register Reading: " + readings[0])
    phase = int(readings[0], 2)/(2**n_count)
    print("Corresponding Phase: %f" % phase)
    counts = result.get_counts()
    plot_histogram(counts)
    plt.show()
    return phase

if __name__ == '__main__':
    ## Create QuantumCircuit with n_count counting qubits
    ## plus 4 qubits for U to act on
    #qc = QuantumCircuit(n_count + 4, n_count)

    ## Initialize counting qubits
    ## in state |+>
    #for q in range(n_count):
    #    qc.h(q)

    ## And auxiliary register in state |1>
    #qc.x(3+n_count)

    ## Do controlled-U operations
    #for q in range(n_count):
    #    qc.append(c_amod15(a, 2**q),
    #              [q] + [i+n_count for i in range(4)])

    ## Do inverse-QFT
    #qc.append(qft_dagger(n_count), range(n_count))

    ## Measure circuit
    #qc.measure(range(n_count), range(n_count))
    #qc.draw(fold=-1, output='mpl')  # -1 means 'do not fold'
    ##qc.draw(output='mpl', filename='shorsAlgoCircuit.png')  # -1 means 'do not fold'

    #aer_sim = Aer.get_backend('aer_simulator')
    #t_qc = transpile(qc, aer_sim)
    #qobj = assemble(t_qc)
    #results = aer_sim.run(qobj).result()
    #counts = results.get_counts()
    #plot_histogram(counts)
    #plt.show()

    #rows, measured_phases = [], []
    #for output in counts:
    #    decimal = int(output, 2)  # Convert (base 2) string to decimal
    #    phase = decimal/(2**n_count)  # Find corresponding eigenvalue
    #    measured_phases.append(phase)
    #    # Add these values to the rows in our table:
    #    rows.append([f"{output}(bin) = {decimal:>3}(dec)",
    #                 f"{decimal}/{2**n_count} = {phase:.2f}"])
    ## Print the rows in a table
    #headers=["Register Output", "Phase"]
    #df = pd.DataFrame(rows, columns=headers)
    #print(df)

    #rows = []
    #for phase in measured_phases:
    #    frac = Fraction(phase).limit_denominator(15)
    #    rows.append([phase, f"{frac.numerator}/{frac.denominator}", frac.denominator])
    ## Print as a table
    #headers=["Phase", "Fraction", "Guess for r"]
    #df = pd.DataFrame(rows, columns=headers)
    #print(df)

    N, a, n_count = 15, 7, 8
    factor_found = False
    attempt = 0
    while not factor_found:
        attempt += 1
        print("\nAttempt %i:" % attempt)
        phase = qpe_amod15(a, n_count) # Phase = s/r
        frac = Fraction(phase).limit_denominator(N) # Denominator should (hopefully!) tell us r
        r = frac.denominator
        print("Result: r = %i" % r)
        if phase != 0:
            # Guesses for factors are gcd(x^{r/2} ±1 , 15)
            guesses = [gcd(a**(r//2)-1, N), gcd(a**(r//2)+1, N)]
            print("Guessed Factors: %i and %i" % (guesses[0], guesses[1]))
            for guess in guesses:
                if guess not in [1,N] and (N % guess) == 0: # Check to see if guess is a factor
                    print("*** Non-trivial factor found: %i ***" % guess)
                    factor_found = True

