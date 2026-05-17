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
    
    def generate_acc0_circuit(n, s):
        circuit = []
        for _ in range(s):
            gate = random.choice(['AND', 'MOD_6'])
            if gate == 'AND':
                circuit.append(('AND', [random.randint(0, n-1), random.randint(0, n-1)]))
            else:
                circuit.append(('MOD_6', [random.randint(0, n-1), random.randint(0, n-1)]))
        return circuit
    
    def evaluate_circuit(circuit, x):
        result = 1
        for gate, inputs in reversed(circuit):
            if gate == 'AND':
                result &= x[inputs[0]] & x[inputs[1]]
            else:
                result &= (x[inputs[0]] + x[inputs[1]]) % 2
        return result
    
    def walsh_hadamard_transform(f, n):
        f_hat = {}
        for alpha in product(range(3), repeat=n):
            value = evaluate_circuit(circuit, alpha)
            f_hat[tuple(alpha)] = value
        return f_hat
    
    def fraction_free_gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            pivot_row = -1
            for i in range(rank, m):
                if A[i][j] != 0:
                    pivot_row = i
                    break
            if pivot_row == -1:
                continue
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            rank += 1
            for i in range(rank, m):
                factor = A[i][j] / A[pivot_row][j]
                for k in range(j, n):
                    A[i][k] -= factor * A[pivot_row][k]
        return rank
    
    def compute_lie_stabilizer(f_hat, n):
        A = [[0] * (n**2) for _ in range(3**n)]
        for alpha in product(range(3), repeat=n):
            term = 0
            for i in range(n):
                for j in range(n):
                    new_alpha = tuple((alpha[k] + (1 if k == i or k == j else 0)) % 3 for k in range(n))
                    if new_alpha in f_hat:
                        term += f_hat[new_alpha]
            A[tuple(alpha)].append(term)
        return fraction_free_gaussian_elimination(A)
    
    def product(iterable):
        result = [()]
        for element in iterable:
            result = [prefix + (element,) for prefix in result]
        return result
    
    n = random.choice([4, 5, 6, 7])
    s = random.choice([3, 8, 20, 50])
    circuit = generate_acc0_circuit(n, s)
    
    f_hat = walsh_hadamard_transform(circuit, n)
    gamma = compute_lie_stabilizer(f_hat, n)
    
    slack = n**2 - gamma - 10 * s
    counterexample = "" if slack >= 0 else f"(n={n}, s={s}, circuit={circuit})"
    
    return {
        "metric_name": "slack",
        "metric_value": slack,
        "instances_tested": 1,
        "conjecture_holds": slack >= 0,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(3, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_slack = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_slack)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slack} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")