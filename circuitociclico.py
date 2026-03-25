import numpy as np
!pip install qiskit qiskit-aer pylatexenc
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from IPython.display import display

# Parâmetros Analíticos calculados
theta_95 = 2.690565
theta_05 = 0.451027
qc = QuantumCircuit(5, 5)
qc.ry(theta_05, 0)
qc.cry(theta_05, 0, 1)
qc.cry(theta_05, 1, 2)
qc.cry(theta_05, 2, 3)
qc.cry(theta_95, 3, 4)

qc.barrier()

# Medição
qc.measure([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])

display(qc.draw('mpl', fold=-1))

# Simulação
shots_totais = 10_000_000
simulador = AerSimulator()
circuito_transpilado = transpile(qc, simulador)
job = simulador.run(circuito_transpilado, shots=shots_totais)
contagens = job.result().get_counts()

# Pós-processamento (Ordem q4q3q2q1q0)
saida_1   = contagens.get('00000', 0) / shots_totais
saida_2   = contagens.get('00001', 0) / shots_totais
saida_3   = contagens.get('00011', 0) / shots_totais
saida_4   = contagens.get('00111', 0) / shots_totais
saida_11  = contagens.get('11111', 0) / shots_totais
saida_12  = contagens.get('01111', 0) / shots_totais


# resultados da simulação
print(f" Primeira saida: {saida_1:.8f}  (Esperado: 0.95000000)")
print(f" Segunda saida:  {saida_2:.8f}  (Esperado: 0.04750000)")
print(f" Terceira saida: {saida_3:.8f}  (Esperado: 0.00237500)")
print(f" Quarta saida:   {saida_4:.8f}  (Esperado: 0.00011875)")
print(f" Quinta saida:   {saida_11:.8f} (Esperado: 0.00000593)")
print(f" Sexta saida:    {saida_12:.8f} (Esperado: 0.00000031)")
