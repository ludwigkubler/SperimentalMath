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
    
    def generate_ac0_circuit(n):
        # Simplified AC⁰ circuit for PARITY using XOR gates
        return [[i ^ (i >> 1) for i in range(2**n)]]
    
    def tropicalize(state):
        # Simplified tropicalization of a state vector
        return max(abs(x) for x in state)
    
    def compute_tee(circuit, n):
        state = circuit[0]
        tee = tropicalize(state)
        return tee
    
    def log_n(n):
        if n <= 1:
            return 0
        return math.log2(n)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        circuit = generate_ac0_circuit(n)
        tee = compute_tee(circuit, n)
        normalized_tee = tee / math.sqrt(len(circuit))
        results.append((n, normalized_tee, log_n(n)))
    
    if len(results) < 24:
        return {
            "metric_name": "TEE(C)/√w(C)",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    n_values, tee_values, log_n_values = zip(*results)
    correlation = 0
    for i in range(len(n_values)):
        for j in range(i + 1, len(n_values)):
            correlation += (n_values[i] - sum(n_values) / len(n_values)) * (log_n_values[j] - sum(log_n_values) / len(log_n_values))
    correlation /= math.sqrt(sum((x - sum(n_values) / len(n_values)) ** 2 for x in n_values)) * math.sqrt(sum((y - sum(log_n_values) / len(log_n_values)) ** 2 for y in log_n_values))
    
    return {
        "metric_name": "TEE(C)/√w(C)",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if "conjecture_holds" in r and r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")