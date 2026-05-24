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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def ac0_parity_circuit_size(f):
    n = int(math.log2(len(f)))
    if 2**n != len(f):
        raise ValueError("Invalid function length")
    circuit_size = 0
    for i in range(n):
        circuit_size += (1 << i)
    return circuit_size

def minimal_rank(L):
    # Implement Gaussian elimination to find the rank of L
    n = len(L)
    rank = 0
    for i in range(n):
        if all(row[i] == 0 for row in L[i:]):
            continue
        rank += 1
        for j in range(i + 1, n):
            if L[j][i] != 0:
                L[j], L[i] = L[i], L[j]
                break
        for j in range(n):
            if j == i:
                continue
            factor = L[j][i] / L[i][i]
            for k in range(n):
                L[j][k] -= factor * L[i][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        ac0_parity_circuit_size_f = ac0_parity_circuit_size(f)
        L = [[f[i] if j == i else 0 for j in range(n)] for i in range(n)]
        minRank_L = minimal_rank(L)
        results.append((n, minRank_L, ac0_parity_circuit_size_f))
    
    conjecture_holds = all(minRank <= math.log2(ac0_parity_circuit_size_f) for _, minRank, ac0_parity_circuit_size_f in results)
    counterexample = ""
    if not conjecture_holds:
        for n, minRank, ac0_parity_circuit_size_f in results:
            if minRank > math.log2(ac0_parity_circuit_size_f):
                counterexample = f"n={n}, minRank(L)={minRank} > log2(size(C))={math.log2(ac0_parity_circuit_size_f)}"
                break
    
    return {
        "metric_name": "minRank(L)",
        "metric_value": sum(minRank for _, minRank, _ in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r, _, _ in results if all(r <= math.log2(ac0_parity_circuit_size(generate_boolean_function(n))) for n in [5, 10, 15, 20, 30, 40])) / len(results)
    
    if support_fraction == len(results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r > math.log2(ac0_parity_circuit_size(generate_boolean_function(n))) for r, _, _ in results for n in [5, 10, 15, 20, 30, 40]):
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=metric_saturation")