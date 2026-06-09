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

def generate_circuit(n, m):
    if n == 1 and m == 1:
        return [0]
    subcircuits = []
    for _ in range(2):
        subcircuit = []
        for i in range(n // 2):
            subcircuit.append(random.randint(0, 1))
        subcircuits.append(subcircuit)
    circuit = []
    for i in range(m):
        circuit.append(subcircuits[1][i] ^ subcircuits[0][i])
    return circuit

def compute_braid_relations(circuit):
    relations = set()
    n = len(circuit)
    for i in range(n - 1):
        if circuit[i] != circuit[i + 1]:
            relations.add((i, i + 1))
    return len(relations)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    n_max = 0
    for n in [5, 10, 15, 20, 30, 40]:
        for m in [5, 10, 15, 20, 30, 40]:
            if n > n_max:
                n_max = n
            circuit = generate_circuit(n, m)
            relations = compute_braid_relations(circuit)
            results.append((n, m, relations))
    metric_value = sum(relations for _, _, relations in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(abs(relations - math.log(n) * math.log(m)) < 0.1 * (math.log(n) * math.log(m))
                           for n, m, relations in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Braid Relations",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["metric_value"] - mean_value) < 0.1 * std_value) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")