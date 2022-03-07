import matplotlib.pyplot as plt
import numpy as np
from numpy import pi
# importing Qiskit
from qiskit import QuantumCircuit, transpile, assemble, Aer, IBMQ
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit_textbook.widgets import scalable_circuit

def qft_rotations(circuit, n):
    if n == 0: # Exit function if circuit is empty
        return circuit
    n -= 1 # Indexes start from 0
    circuit.h(n) # Apply the H-gate to the most significant qubit
    for qubit in range(n):
        # For each less significant qubit, we need to do a
        # smaller-angled controlled rotation:
        circuit.cp(pi/2**(n-qubit), qubit, n)
    qft_rotations(circuit, n)

def swap_registers(circuit, n):
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
    return circuit
def qft(circuit, n):
    """QFT on the first n qubits in circuit"""
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit

def inverse_qft(circuit, n):
    """Does the inverse QFT on the first n qubits in circuit"""
    # First we create a QFT circuit of the correct size:
    qft_circ = qft(QuantumCircuit(n), n)
    # Then we take the inverse of this circuit
    invqft_circ = qft_circ.inverse()
    # And add it to the first n qubits in our existing circuit
    circuit.append(invqft_circ, circuit.qubits[:n])
    return circuit.decompose() # .decompose() allows us to see the individual gates

if __name__ == '__main__':
    print('Attempting a 3-qubit case of quantum Fourier Transform')
    qc = QuantumCircuit(3)
    qc.h(2)
    #qc.draw(fold=-1, output='mpl')  # -1 means 'do not fold'
    #plt.show()

    qc.cp(pi/2, 1, 2) # CROT from qubit 1 to qubit 2. Rotate qubit-2 if qubit-1 is in |1>
    #qc.draw(fold=-1, output='mpl')
    #plt.show()

    qc.cp(pi/4, 0, 2) # CROT from qubit 0 to qubit 2. Rotate qubit-2 if qubit-0 is in |1>
    #qc.draw(fold=-1, output='mpl')
    #plt.show()

    qc.h(1)
    #qc.draw(fold=-1, output='mpl')
    #plt.show()

    qc.cp(pi/2, 0, 1) # CROT from qubit 0 to qubit 1. Rotate qubit-1 if qubit-0 is in |1>
    #qc.draw(fold=-1, output='mpl')
    #plt.show()

    qc.h(0)
    #qc.draw(fold=-1, output='mpl')
    #plt.show()

    qc.swap(0, 2)
    #qc.draw(fold=-1, output='mpl')
    #plt.show()

    qc = QuantumCircuit(4)
    qft_rotations(qc, 4)
    #qc.draw(fold=-1, output='mpl')
    #plt.show()

    #scalable_circuit(qft_rotations)

    # Let's see how it looks:
    qc = QuantumCircuit(4)
    qft(qc, 4)
    #qc.draw(fold=-1, output='mpl')
    #plt.show()

    #scalable_circuit(qft)

    #Below is an example where we implement a binary number 101 in the qubits as a statevector
    # Create the circuit
    qc = QuantumCircuit(3)

    # Encode the state 5
    qc.x(0)
    qc.x(2)
    #qc.draw(fold=-1, output='mpl')
    #plt.show()

    sim = Aer.get_backend("aer_simulator")
    qc_init = qc.copy()
    qc_init.save_statevector()
    statevector = sim.run(qc_init).result().get_statevector()
    #plot_bloch_multivector(statevector)
    #plt.show()

    qft(qc, 3)
    #qc.draw(fold=-1, output='mpl')
    #plt.show()

    qc.save_statevector()
    statevector = sim.run(qc).result().get_statevector()
    #plot_bloch_multivector(statevector)
    #plt.show()

    #Below is a visualization to look at the |+++> state
    #qc = QuantumCircuit(3)
    #qc.h(0)
    #qc.h(1)
    #qc.h(2)
    #plot_bloch_multivector(qc)
    #plt.show()

    #Putting |\widetilde(5) in three qubit statevector
    nqubits = 3
    number = 5
    qc = QuantumCircuit(nqubits)
    for qubit in range(nqubits):
        qc.h(qubit)
    qc.p(number*pi/4, 0)
    qc.p(number*pi/2, 1)
    qc.p(number*pi, 2)

    #qc.draw(fold=-1, output='mpl')
    #plt.show()

    qc_init = qc.copy()
    qc_init.save_statevector()
    sim = Aer.get_backend("aer_simulator")
    statevector = sim.run(qc_init).result().get_statevector()
    #plot_bloch_multivector(statevector)
    #plt.show()

    #Now applying inverse quantum Fourier transform to the statevector
    inverse_qft(qc, nqubits)
    qc.measure_all()
    qc.draw(fold=-1, output='mpl')
    plt.show()

    #shots = 2048
    #transpiled_qc = transpile(qc, backend, optimization_level=3)
    #counts = job.result().get_counts()
    #plot_histogram(counts)

    
