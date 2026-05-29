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
    
    def generate_xor_circuit(n, depth):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_xor_circuit(n // 2, depth - 1)
            right = generate_xor_circuit(n // 2, depth - 1)
            return [left[i] ^ right[i] for i in range(n)]
    
    def cycle_space(circuit):
        n = len(circuit)
        space = []
        for i in range(1 << n):
            subcircuit = [circuit[j] if (i & (1 << j)) else 0 for j in range(n)]
            if sum(subcircuit) % 2 == 1:
                space.append(subcircuit)
        return space
    
    def poincare_dual_complex(space):
        n = len(space[0])
        dual_complex = [[] for _ in range(n + 1)]
        for subcircuit in space:
            for i in range(n):
                if sum(subcircuit[j] & (1 << i) for j in range(len(subcircuit))) % 2 == 1:
                    dual_complex[i].append(subcircuit)
        return dual_complex
    
    def minimal_index(dual_complex):
        n = len(dual_complex)
        indices = [len(cycle) for cycle in dual_complex]
        return max(indices)
    
    def O_d_n_log_n(d, n):
        return d ** n * math.log(n)
    
    results = []
    for n in range(5, 41):
        depth = random.randint(1, min(40, n))
        circuit = generate_xor_circuit(n, depth)
        space = cycle_space(circuit)
        dual_complex = poincare_dual_complex(space)
        mu_K_C = minimal_index(dual_complex)
        O_d_n_log_n_value = O_d_n_log_n(depth, n)
        
        results.append({
            "n": n,
            "depth": depth,
            "mu_K_C": mu_K_C,
            "O_d_n_log_n": O_d_n_log_n_value
        })
    
    total_mu_K_C = sum(result["mu_K_C"] for result in results)
    total_O_d_n_log_n = sum(result["O_d_n_log_n"] for result in results)
    mean_mu_K_C = total_mu_K_C / len(results)
    mean_O_d_n_log_n = total_O_d_n_log_n / len(results)
    
    conjecture_holds = all(result["mu_K_C"] <= 2 * result["O_d_n_log_n"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_index",
        "metric_value": mean_mu_K_C,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")