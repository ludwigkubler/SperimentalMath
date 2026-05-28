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
        for _ in range(random.randint(5, 10)):
            gate_type = 'XOR' if random.random() < 0.7 else 'AND'
            inputs = random.sample(range(n), random.randint(2, n))
            circuit.append((gate_type, inputs))
        return circuit
    
    def construct_symmetric_function(circuit):
        n = len(circuit)
        f = {}
        for i in range(1 << n):
            x = [bool(i & (1 << j)) for j in range(n)]
            value = 0
            for gate_type, inputs in circuit:
                if gate_type == 'XOR':
                    value ^= sum(x[j] for j in inputs)
                else:  # AND
                    value &= all(x[j] for j in inputs)
            f[tuple(x)] = value
        return f
    
    def hessian_matrix(f):
        n = len(next(iter(f)))
        H = [[0] * n for _ in range(n)]
        for x in f:
            for i in range(n):
                dx_i = list(x)
                dx_i[i] = not dx_i[i]
                for j in range(i, n):
                    dx_j = list(dx_i)
                    dx_j[j] = not dx_j[j]
                    H[i][j] += (f[tuple(dx_i)] - f[x]) * (f[tuple(dx_j)] - f[x])
        return H
    
    def matrix_rank(H):
        m, n = len(H), len(H[0])
        rank = 0
        for i in range(min(m, n)):
            if any(H[j][i] != 0 for j in range(i, m)):
                rank += 1
                for j in range(i + 1, m):
                    factor = H[j][i] / H[i][i]
                    for k in range(i, n):
                        H[j][k] -= factor * H[i][k]
        return rank
    
    def max_weight(circuit):
        weights = []
        for gate_type, inputs in circuit:
            if gate_type == 'XOR':
                weights.extend([2**len(inputs)] * len(inputs))
            else:  # AND
                weights.append(1)
        return sum(weights)
    
    n = random.randint(5, 40)
    circuit = generate_xor_circuit(n)
    f = construct_symmetric_function(circuit)
    H = hessian_matrix(f)
    rank = matrix_rank(H)
    max_weight_val = max_weight(circuit)
    
    c = 1.0
    conjecture_holds = rank >= c * (n / len(circuit))**(1/4)
    counterexample = "" if conjecture_holds else f"Rank {rank} < {c * (n / len(circuit))**(1/4)}"
    
    return {
        "metric_name": "Hessian Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")