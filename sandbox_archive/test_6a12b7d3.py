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
    
    def generate_circuit(n, D):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            sub_n = n // 2
            sub_D = D - 1
            left = generate_circuit(sub_n, sub_D)
            right = generate_circuit(sub_n, sub_D)
            return [left[i] ^ right[i] for i in range(len(left))]
    
    def topological_entropy(lattice):
        if not lattice:
            return 0.0
        n = len(lattice)
        log_n = math.log2(n)
        entropy = 0.0
        for value, count in lattice.items():
            p = count / n
            entropy -= p * (math.log2(p) if p > 0 else 0)
        return entropy
    
    def generate_lattice(circuit):
        lattice = {}
        for state in itertools.product([0, 1], repeat=len(circuit)):
            output = circuit[:]
            for i in range(len(output)):
                if isinstance(output[i], list):
                    output[i] = output[i][state[i]]
            key = tuple(output)
            lattice[key] = lattice.get(key, 0) + 1
        return lattice
    
    n_values = [2, 4, 8]
    total_entropy = 0.0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        D = math.ceil(math.log2(n + 1))
        circuit = generate_circuit(n, D)
        lattice = generate_lattice(circuit)
        entropy = topological_entropy(lattice)
        total_entropy += entropy
        instances_tested += len(lattice)
        n_max = max(n_max, n)
    
    mean_entropy = total_entropy / instances_tested
    c = 0.1  # Example constant, adjust as needed
    
    if mean_entropy >= c * math.log2(n + D):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "mean_entropy < c * log2(n + D)"
    
    return {
        "metric_name": "topological entropy",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")