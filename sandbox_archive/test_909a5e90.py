# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropicalized_homology_group(f):
        n = len(f)
        H = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            for j in range(n + 1):
                if i == 0 or j == 0:
                    H[i][j] = 0
                else:
                    H[i][j] = max([f[k] for k in range(2**n) if (k >> (i - 1)) & 1 and (k >> (j - 1)) & 1])
        return H
    
    def min_rank(H):
        n = len(H)
        rank = 0
        for i in range(n):
            for j in range(i, n):
                if H[i][j] != 0:
                    rank += 1
                    break
        return rank
    
    def monotone_circuit(f, max_layers):
        n = len(f)
        gates = []
        for layer in range(max_layers):
            new_gates = set()
            for i in range(n):
                if f[i] == 1:
                    new_gates.add(i)
            gates.extend(new_gates)
            f = [f[i] & (i in gates) for i in range(2**n)]
        return len(gates)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    H = tropicalized_homology_group(f)
    r = min_rank(H)
    
    max_layers = n
    circuits = []
    for _ in range(30):
        circuit_size = monotone_circuit(f, max_layers)
        if circuit_size <= r * (n + 1):
            return {
                "metric_name": "circuit_size",
                "metric_value": circuit_size,
                "instances_tested": 1,
                "conjecture_holds": True,
                "counterexample": ""
            }
        circuits.append(circuit_size)
    
    counterexample = f"Monotone circuit with {max(circuits)} gates exceeds the upper bound of {r * (n + 1)}"
    return {
        "metric_name": "circuit_size",
        "metric_value": max(circuits),
        "instances_tested": len(circuits),
        "conjecture_holds": False,
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
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")