#initialization
import matplotlib.pyplot as plt
import numpy as np
import math

# importing Qiskit
from qiskit import IBMQ, Aer, transpile, assemble
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

# import basic plot tools
from qiskit.visualization import plot_histogram

def qft_dagger(qc, n):
    """n-qubit QFTdagger the first n qubits in circ"""
    # Don't forget the Swaps!
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-math.pi/float(2**(j-m)), m, j)
        qc.h(j)
if __name__ == '__main__':
    qpe = QuantumCircuit(4, 3)
    qpe.x(3)
    #qpe.draw(fold=-1, output='mpl')
    #plt.show()

    for qubit in range(3):
        qpe.h(qubit)
    #qpe.draw(fold=-1, output='mpl')
    #plt.show()

    repetitions = 1
    for counting_qubit in range(3):
        for i in range(repetitions):
            qpe.cp(math.pi/4, counting_qubit, 3); # This is CU
        repetitions *= 2
    #qpe.draw(fold=-1, output='mpl')
    #plt.show()

    qpe.barrier()
    #qpe.draw(fold=-1, output='mpl')
    #plt.show()

    qft_dagger(qpe, 3)
    qpe.barrier()
    for n in range(3):
        qpe.measure(n, n)
    #qpe.draw(fold=-1, output='mpl')
    #plt.show()

    aer_sim = Aer.get_backend('aer_simulator')
    shots = 2048
    t_qpe = transpile(qpe, aer_sim)
    qobj = assemble(t_qpe, shots=shots)
    results = aer_sim.run(qobj).result()
    answer = results.get_counts()

    #plot_histogram(answer)
    #plt.show()

    # Create and set up circuit
    qpe2 = QuantumCircuit(4, 3)

    # Apply H-Gates to counting qubits:
    for qubit in range(3):
        qpe2.h(qubit)

    # Prepare our eigenstate |psi>:
    qpe2.x(3)

    # Do the controlled-U operations:
    angle = 2*math.pi/3
    repetitions = 1
    for counting_qubit in range(3):
        for i in range(repetitions):
            qpe2.cp(angle, counting_qubit, 3);
        repetitions *= 2

    # Do the inverse QFT:
    qft_dagger(qpe2, 3)

    # Measure of course!
    for n in range(3):
        qpe2.measure(n,n)

    #qpe2.draw(fold=-1, output='mpl')
    #plt.show()

    # Let's see the results!
    aer_sim = Aer.get_backend('aer_simulator')
    shots = 4096
    t_qpe2 = transpile(qpe2, aer_sim)
    qobj = assemble(t_qpe2, shots=shots)
    results = aer_sim.run(qobj).result()
    answer = results.get_counts()

    #plot_histogram(answer)
    #plt.show()

    # Create and set up circuit
    qpe3 = QuantumCircuit(6, 5)

    # Apply H-Gates to counting qubits:
    for qubit in range(5):
        qpe3.h(qubit)

    # Prepare our eigenstate |psi>:
    qpe3.x(5)

    # Do the controlled-U operations:
    angle = 2*math.pi/3
    repetitions = 1
    for counting_qubit in range(5):
        for i in range(repetitions):
            qpe3.cp(angle, counting_qubit, 5);
        repetitions *= 2

    # Do the inverse QFT:
    qft_dagger(qpe3, 5)

    # Measure of course!
    qpe3.barrier()
    for n in range(5):
        qpe3.measure(n,n)

    #qpe3.draw(fold=-1, output='mpl')
    #plt.show()

    # Let's see the results!
    aer_sim = Aer.get_backend('aer_simulator')
    shots = 4096
    t_qpe3 = transpile(qpe3, aer_sim)
    qobj = assemble(t_qpe3, shots=shots)
    results = aer_sim.run(qobj).result()
    answer = results.get_counts()

    #plot_histogram(answer)
    #plt.show()

    #A trial on real devices
    #qpe.draw(fold=-1, output='mpl')
    #plt.show()
    #IBMQ.load_account()
    #from qiskit.tools.monitor import job_monitor
    #provider = IBMQ.get_provider(hub='ibm-q')
    #santiago = provider.get_backend('ibmq_santiago')

    ## Run with 2048 shots
    #shots = 2048
    #t_qpe = transpile(qpe, santiago, optimization_level=3)
    #job = santiago.run(t_qpe, shots=shots)
    #job_monitor(job)


