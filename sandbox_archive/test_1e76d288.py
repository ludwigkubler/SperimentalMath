# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_ac0_circuit(n):
    circuit = []
    for _ in range(2**n):
        gate_type = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(n)]
        if gate_type == 'AND':
            output = all(inputs)
        else:
            output = any(inputs)
        circuit.append((gate_type, inputs, output))
    return circuit

def polynomial_representation(circuit):
    n = len(circuit[0][1])
    poly = [Fraction(0)] * (2**n)
    for gate in reversed(circuit):
        gate_type, inputs, output = gate
        if gate_type == 'AND':
            term = Fraction(1)
            for bit in inputs:
                term *= Fraction(bit)
            poly[output] += term
        else:
            term = Fraction(1)
            for bit in inputs:
                term *= 1 - Fraction(bit)
            poly[output] -= term
    return poly

def matrix_from_polynomial(poly, n):
    m = len(poly)
    matrix = [[Fraction(0)] * (m + 1) for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if i & (1 << j):
                matrix[i][j] += poly[i]
        matrix[i][-1] -= poly[i]
    return matrix

def qr_decomposition(matrix):
    m, n = len(matrix), len(matrix[0])
    Q = [[Fraction(0)] * n for _ in range(m)]
    R = [[Fraction(0)] * n for _ in range(n)]
    
    for k in range(n):
        norm = Fraction(0)
        for i in range(k, m):
            norm += matrix[i][k] ** 2
        norm = norm ** Fraction(1, 2)
        
        if norm == Fraction(0):
            raise ValueError("Matrix is singular")
        
        Q[k][k] = matrix[k][k] / norm
        R[0][k] = matrix[k][k]
        
        for j in range(k + 1, n):
            R[k][j] = Fraction(0)
            for i in range(k, m):
                R[k][j] += Q[i][k] * matrix[i][j]
            for i in range(k, m):
                matrix[i][j] -= Q[i][k] * R[k][j]
        
        for i in range(k + 1, m):
            Q[i][k] = -matrix[i][k] / norm
            for j in range(k + 1, n):
                Q[i][j] += Q[i][k] * R[k][j]
    
    return Q, R

def real_rank(matrix):
    _, R = qr_decomposition(matrix)
    rank = sum(1 for row in R if any(x != Fraction(0) for x in row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    circuit = generate_ac0_circuit(n)
    poly = polynomial_representation(circuit)
    matrix = matrix_from_polynomial(poly, n)
    rank = real_rank(matrix)
    
    metric_name = "real_rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= 0.3 * math.log2(n)
    counterexample = "" if conjecture_holds else f"rank={rank}, expected ≥{0.3 * math.log2(n)}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank too small\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")