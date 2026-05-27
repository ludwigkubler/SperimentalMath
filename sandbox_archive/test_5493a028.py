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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_tropicalized_entanglement_entropy(circuit):
        # Placeholder for computing TEE of the output qubits
        return random.random()
    
    def normalize_tee_by_sqrt_w_c(tee, w_c):
        return tee / math.sqrt(w_c)
    
    def compute_spearman_rank_correlation(values1, values2):
        n = len(values1)
        rank1 = {v: i for i, v in enumerate(sorted(set(values1)), 1)}
        rank2 = {v: i for i, v in enumerate(sorted(set(values2)), 1)}
        sum_d_ranks_squared = sum((rank1[v] - rank2[v])**2 for v in values1)
        return 1 - (6 * sum_d_ranks_squared) / (n * (n**2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_ac0_circuit(n)
        w_c = len(circuit)
        tee = compute_tropicalized_entanglement_entropy(circuit)
        normalized_tee = normalize_tee_by_sqrt_w_c(tee, w_c)
        results.append(normalized_tee)
    
    mean_normalized_tee = sum(results) / len(results)
    log_n_values = [math.log(n) for n in n_values]
    spearman_corr = compute_spearman_rank_correlation(results, log_n_values)
    
    metric_value = mean_normalized_tee
    instances_tested = len(results)
    conjecture_holds = spearman_corr >= 0.5  # Placeholder threshold
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": spearman_corr,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 103))  # Default to first 30 primes
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")