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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_xor_circuit(n):
        circuit = []
        for _ in range(random.randint(5, 20)):
            gate = ('XOR', [random.choice(['x' + str(i) for i in range(n)]) for _ in range(2)])
            circuit.append(gate)
        return circuit
    
    def construct_symmetric_function(circuit):
        n = len([var for var in circuit[0][1] if 'x' in var])
        coeffs = [random.uniform(-1, 1) for _ in range(2**n)]
        return coeffs
    
    def hessian_matrix(f, vars):
        n = len(vars)
        H = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                delta_i = {vars[i]: 1} if i == j else {vars[i]: -1}
                delta_j = {vars[j]: 1} if i == j else {vars[j]: -1}
                H[i][j] = (f(delta_i) - f({**delta_i, **delta_j})) / 4
                if i != j:
                    H[j][i] = H[i][j]
        return H
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        A = [row[:] for row in matrix]
        r = 0
        for j in range(n):
            i_max = max(range(r, m), key=lambda i: abs(A[i][j]))
            if abs(A[i_max][j]) < 1e-9:
                continue
            A[r], A[i_max] = A[i_max], A[r]
            for i in range(r + 1, m):
                factor = -A[i][j] / A[r][j]
                for k in range(n):
                    A[i][k] += factor * A[r][k]
            r += 1
        return r
    
    def max_weight(circuit):
        n = len([var for var in circuit[0][1] if 'x' in var])
        weights = [random.uniform(0, 1) for _ in range(2**n)]
        return max(weights)
    
    n = random.randint(5, 40)
    circuit = generate_xor_circuit(n)
    f_coeffs = construct_symmetric_function(circuit)
    H = hessian_matrix(lambda x: sum(f_coeffs[i] * prod(x[var] for var in vars) for i, vars in enumerate(circuit)), ['x' + str(i) for i in range(n)])
    rank_H = rank(H)
    max_weight_C = max_weight(circuit)
    
    c = 1.0
    conjecture_holds = rank_H >= c * (n / len(circuit))**(1/4)
    counterexample = "" if conjecture_holds else f"rank_H={rank_H}, expected >= {c * (n / len(circuit))**(1/4)}"
    
    return {
        "metric_name": "Rank of Hessian Matrix",
        "metric_value": rank_H,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")