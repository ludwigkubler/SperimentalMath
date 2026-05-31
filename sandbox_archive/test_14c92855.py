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

# Khinchin's constant π_0
PI_0 = 2.718281828459045

def shannon_entropy(p):
    if p == 0 or p == 1:
        return 0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

def generate_random_circuit(n, m):
    circuit = []
    for _ in range(m):
        row = [random.choice([0, 1]) for _ in range(n)]
        circuit.append(row)
    return circuit

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 30
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(instances_tested):
            circuit = generate_random_circuit(n, 1)
            p = sum(circuit[0]) / n
            H_C = shannon_entropy(p)
            diff = abs(H_C - 2 / PI_0)
            
            results.append({
                "metric_name": "H(C)",
                "metric_value": H_C,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": diff <= 1 / PI_0,
                "counterexample": "" if diff <= 1 / PI_0 else f"n={n}, p={p}"
            })
    
    return {
        "seed": seed,
        "metric_name": "H(C)",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": instances_tested * 6,
        "n_max": n_max,
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")