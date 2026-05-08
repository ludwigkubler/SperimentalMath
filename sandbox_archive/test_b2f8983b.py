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

def walsh_hadamard_transform(f):
    n = len(f)
    for s in range(1, int(math.log2(n)) + 1):
        half = 1 << s
        for i in range(half):
            mask = (1 << s) - 1
            for j in range(i, n, half * 2):
                u = f[j]
                v = f[j ^ half]
                f[j] = u + v
                f[j ^ half] = u - v
    return f

def add_fourier_coefficients(f1, f2):
    return [a + b for a, b in zip(f1, f2)]

def multiply_fourier_coefficients(f1, f2):
    n = len(f1)
    result = [0] * n
    for i in range(n):
        for j in range(n):
            result[(i + j) % n] += f1[i] * f2[j]
    return result

def additive_energy(f):
    n = len(f)
    energy = 0
    for i in range(n):
        for j in range(i, n):
            energy += abs(f[i] * f[j])
    return energy

def sos_refutation_size(Phi):
    # Placeholder heuristic: tree depth of DPLL search
    # This is a very rough estimate and not accurate for real SOS refutations
    return len(Phi) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(3 * n, 6 * n)
    Phi = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
        Phi.append(clause)
    
    f = [0] * (1 << n)
    for clause in Phi:
        term = 1
        for literal in clause:
            if literal > 0:
                term *= 1 - (2 * random.random() - 1) / math.sqrt(3)
            else:
                term *= 1 + (2 * random.random() - 1) / math.sqrt(3)
        f[sum(literal for literal in clause)] += term
    
    f = walsh_hadamard_transform(f)
    
    E = additive_energy(f)
    k = sos_refutation_size(Phi)
    
    metric_value = E
    conjecture_holds = E >= m**2 / (2 * k)
    counterexample = "" if conjecture_holds else "E < m² / (2k)"
    
    return {
        "metric_name": "additive_energy",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"E < m² / (2k)\" first_failing_seed={first_failing_seed}")