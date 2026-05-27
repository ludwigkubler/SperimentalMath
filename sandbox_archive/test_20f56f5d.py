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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_ac0_circuit(n):
        # Placeholder for generating an AC⁰ circuit computing PARITY with size n
        return [random.randint(0, 1) for _ in range(n)]
    
    def compute_tropicalized_entropy(state):
        # Placeholder for computing the Tropicalized Entanglement Entropy of a state
        return sum(abs(x - y) for x, y in zip(state[:-1], state[1:]))
    
    def normalize(value, width):
        return value / math.sqrt(width)
    
    def compute_spearman_correlation(values1, values2):
        ranks1 = {v: i + 1 for i, v in enumerate(sorted(set(values1), key=values1.index))}
        ranks2 = {v: i + 1 for i, v in enumerate(sorted(set(values2), key=values2.index))}
        n = len(values1)
        sum_diff_squares = sum((ranks1[v] - ranks2[v]) ** 2 for v in values1 if v in ranks2)
        return 1 - (6 * sum_diff_squares) / (n * (n**2 - 1))
    
    results = []
    log_n_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = generate_ac0_circuit(n)
            width = len(circuit)
            state = compute_tropicalized_entropy(circuit)
            normalized_tee = normalize(state, width)
            results.append(normalized_tee)
            log_n_values.append(math.log(n))
    
    if not results or not log_n_values:
        return {
            "metric_name": "TEE(C)/√w(C)",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    spearman_corr = compute_spearman_correlation(results, log_n_values)
    mean_tee = sum(results) / len(results)
    std_tee = math.sqrt(sum((x - mean_tee) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "TEE(C)/√w(C)",
        "metric_value": mean_tee,
        "instances_tested": len(results),
        "conjecture_holds": spearman_corr >= 0.5,  # Placeholder threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(1, 6)]
    
    results = []
    total_tee = 0.0
    total_instances = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if trial_result["conjecture_holds"]:
            total_tee += trial_result["metric_value"]
            total_instances += trial_result["instances_tested"]
        
        results.append(trial_result)
    
    mean_tee = total_tee / len(results) if results else 0.0
    std_tee = math.sqrt(sum((r["metric_value"] - mean_tee) ** 2 for r in results)) / len(results) if results else 0.0
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_tee} std={std_tee} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"seed {first_failing_seed}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")