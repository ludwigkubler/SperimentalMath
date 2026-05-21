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

def fourier_hat(f, U):
    n = int(math.log2(len(f)))
    return sum(f(x) * (-1)**sum(U[i] for i in range(n) if x & (1 << i)) / 2**n for x in range(2**n))

def gram_matrix(f, d):
    B_d = [set(range(i+1)) for i in range(d)]
    Q_d = [[0]*len(B_d) for _ in range(len(B_d))]
    for S in B_d:
        for T in B_d:
            Q_d[B_d.index(S)][B_d.index(T)] = fourier_hat(f, S ^ T)
    return Q_d

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 10]
    results = []
    
    for n in n_values:
        f = lambda x: (-1)**sum(x[i] for i in range(n))
        S_n = {i for i in range(n) if i % 2 == 0}
        
        Q_2_S_n = gram_matrix(S_n, 2)
        eigenvalues_S_n = sorted(math.sqrt(-x) for x in math.eigvalsh(Q_2_S_n) if x <= 0)
        NG_2_S_n = -eigenvalues_S_n[0] if eigenvalues_S_n else float('inf')
        
        max_ng_2_circuit = 0
        for _ in range(30):
            circuit = [random.choice(['AND', 'OR', 'MOD3']) for _ in range(n * int(math.log2(n)))]
            NG_2_circuit = -min([fourier_hat(lambda x: sum(circuit[i] == 'AND' and x[i] == 1 or circuit[i] == 'OR' and (x[i] + x[j]) % 3 == 0 for i in range(n) for j in range(i+1, n)), S_n ^ T) for T in B_d])
            max_ng_2_circuit = max(max_ng_2_circuit, NG_2_circuit)
        
        random_truth_tables = [set(random.sample(range(n), k)) for _ in range(30) for k in range(1, n+1)]
        max_ng_2_random = 0
        for truth_table in random_truth_tables:
            NG_2_random = -min([fourier_hat(lambda x: sum(x[i] == 1 for i in truth_table), S_n ^ T) for T in B_d])
            max_ng_2_random = max(max_ng_2_random, NG_2_random)
        
        results.append({
            "metric_name": "NG_2",
            "metric_value": NG_2_S_n,
            "instances_tested": 31,
            "conjecture_holds": NG_2_S_n >= 1/(8*n) and NG_2_S_n - max_ng_2_circuit >= 1/(8*n),
            "counterexample": "" if NG_2_S_n >= 1/(8*n) and NG_2_S_n - max_ng_2_circuit >= 1/(8*n) else f"NG_2(S_n) = {NG_2_S_n}, max(NG_2(circuits)) = {max_ng_2_circuit}"
        })
    
    return {
        "seed": seed,
        "metric_name": "NG_2",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": 3 * len(n_values) * 31,
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": "" if all(result["conjecture_holds"] for result in results) else next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    for seed in seeds:
        print(f"TRIAL: {run_trial(seed)}")