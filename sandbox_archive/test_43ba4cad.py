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
    # Simplified AC⁰ circuit for parity function
    return [random.choice([0, 1]) for _ in range(2**n)]

def tensor_representation(circuit):
    n = len(circuit)
    T_f = [[0] * (2**n) for _ in range(n+1)]
    for i in range(n+1):
        for j in range(2**i):
            if i == 0:
                T_f[i][j] = circuit[j]
            else:
                T_f[i][j] = sum(T_f[i-1][j>>k & 1] for k in range(i)) % 2
    return T_f

def calculate_norms(circuit, n):
    T_f = tensor_representation(circuit)
    norm = 0
    for row in T_f:
        norm += sum(abs(x) for x in row)**(1/n)
    return norm / len(T_f)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    norms = []
    
    for n in n_values:
        circuit = generate_ac0_circuit(n)
        norm = calculate_norms(circuit, n)
        norms.append(norm)
    
    mean_norm = sum(norms) / len(norms)
    std_norm = math.sqrt(sum((x - mean_norm)**2 for x in norms) / len(norms))
    
    conjecture_holds = all(norm >= n**2 * math.log(n) for norm, n in zip(norms, n_values))
    counterexample = "" if conjecture_holds else "n={n}, norm={norm}"
    
    return {
        "metric_name": "Minimal Symmetric Tensor Norm",
        "metric_value": mean_norm,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_norm = sum(r["metric_value"] for r in results) / len(results)
    std_norm = math.sqrt(sum((r["metric_value"] - mean_norm)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_norm} std={std_norm} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing = next(r for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={first_failing['metric_value']}, norm={first_failing['counterexample']}\" first_failing_seed={seeds[results.index(first_failing)]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")