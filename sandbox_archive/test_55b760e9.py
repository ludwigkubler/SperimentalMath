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

def generate_xor_circuit(n, depth):
    if n == 1:
        return [random.randint(0, 1)]
    elif depth == 1:
        left = generate_xor_circuit(n // 2, 1)
        right = generate_xor_circuit(n - n // 2, 1)
        return [left[i] ^ right[i] for i in range(n)]
    else:
        left = generate_xor_circuit(n // 2, depth - 1)
        right = generate_xor_circuit(n - n // 2, depth - 1)
        return [left[i] ^ right[i] for i in range(n)]

def calculate_poincare_dual_complex(circuit):
    n = len(circuit)
    cycle_space = []
    for i in range(1 << n):
        subcircuit = [circuit[j] if (i >> j) & 1 else 0 for j in range(n)]
        if sum(subcircuit) % 2 == 1:
            cycle_space.append(subcircuit)
    return cycle_space

def calculate_minimal_index(cycle_space, d):
    n = len(cycle_space[0])
    indices = []
    for subcircuit in cycle_space:
        index = 0
        for i in range(n):
            if subcircuit[i] == 1:
                index += (i + 1) ** d
        indices.append(index)
    return min(indices)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        for _ in range(30 // (n_max - 4)):
            depth = random.randint(1, min(n, 40))
            circuit = generate_xor_circuit(n, depth)
            cycle_space = calculate_poincare_dual_complex(circuit)
            d = len(cycle_space[0])
            mu_K_C = calculate_minimal_index(cycle_space, d)
            instances_tested += 1

            if mu_K_C > (d ** n * math.log(n)).quantize(Fraction(1)):
                conjecture_holds = False
                counterexample = f"n={n}, depth={depth}, mu(K_C)={mu_K_C}, O(d^n log(n))={(d ** n * math.log(n)).quantize(Fraction(1))}"
                break

    return {
        "metric_name": "minimal_index",
        "metric_value": (sum(calculate_minimal_index(calculate_poincare_dual_complex(generate_xor_circuit(n, random.randint(1, min(n, 40)))), len(calculate_poincare_dual_complex(generate_xor_circuit(n, random.randint(1, min(n, 40))))[0]))) / instances_tested).quantize(Fraction(1)),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['conjecture_holds'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")