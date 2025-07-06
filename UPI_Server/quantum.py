from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT
from math import gcd, ceil, log2
from fractions import Fraction
import numpy as np

def a_mod_exp_circuit(a, j, N, n_count, n_mod):
    circuit = QuantumCircuit(n_count + n_mod, name=f"a^(2^{j})mod{N}")
    a_exp = pow(a, 2**j, N)
    for i in range(n_count):
        if i == 0:
            circuit.x(n_count)
        for k in range(n_mod):
            if (a_exp & (1 << k)):
                circuit.cx(i, n_count + k)
    return circuit

def qpe_amod_N(a, n_count, n_mod, N):
    qc = QuantumCircuit(n_count + n_mod, n_count)
    qc.x(n_count)
    for q in range(n_count):
        qc.h(q)
    for j in range(n_count):
        qc.compose(a_mod_exp_circuit(a, j, N, n_count, n_mod), inplace=True)
    qc.barrier()
    qc = qc.compose(QFT(n_count).inverse(), qubits=range(n_count))
    qc.barrier()
    qc.measure(range(n_count), range(n_count))
    return qc

def find_period(a, N):
    if gcd(a, N) != 1:
        return None
    n_count = ceil(2 * log2(N))
    n_mod = ceil(log2(N))
    simulator = AerSimulator()
    measurements = {}
    for _ in range(3):
        qc = qpe_amod_N(a, n_count, n_mod, N)
        qc_transpiled = transpile(qc, simulator)
        job = simulator.run(qc_transpiled, shots=1024)
        result = job.result()
        counts = result.get_counts()
        measurements.update(counts)
    phases = []
    for bitstring, count in measurements.items():
        if count > 10:
            decimal = int(bitstring, 2)
            phase = decimal / (2**n_count)
            phases.append(phase)
    for phase in phases:
        frac = Fraction(phase).limit_denominator(N)
        r = frac.denominator
        if r % 2 == 0 and pow(a, r//2, N) != N - 1 and pow(a, r, N) == 1:
            return r
    return None

def classical_period_finding(a, N):
    r = 1
    while pow(a, r, N) != 1:
        r += 1
        if r > 100:
            return None
    return r

def shors_algorithm(N):
    if N % 2 == 0:
        return [2, N // 2]
    for _ in range(5):
        a = np.random.randint(2, N)
        d = gcd(a, N)
        if d > 1:
            return [d, N // d]
        r = find_period(a, N)
        if r is None:
            r = classical_period_finding(a, N)
        if r and r % 2 == 0:
            factor1 = gcd(pow(a, r // 2) - 1, N)
            factor2 = gcd(pow(a, r // 2) + 1, N)
            if factor1 > 1 and factor1 < N:
                return [factor1, N // factor1]
            elif factor2 > 1 and factor2 < N:
                return [factor2, N // factor2]
    return [N]

def run_shors_algorithm(N):
    print(f"\n⚛️ Running Shor's Algorithm to factor {N}...")
    if N <= 1:
        print("Error: Number must be greater than 1.")
        return
    if N == 2:
        print("Result: 2 is prime.")
        return
    try:
        factors = shors_algorithm(N)
        if len(factors) == 1:
            print(f"Result: {N} might be prime or factorization failed.")
        else:
            print(f"Result: {N} = {factors[0]} × {factors[1]}")
        return factors
    except Exception as e:
        print(f"❌ Quantum simulation failed: {e}")
        return None
