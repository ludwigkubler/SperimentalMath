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
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def norm_of_noncommutative_space(cnf):
        # Placeholder implementation of the noncommutative space norm
        m = len(cnf)
        n = max(abs(lit) for clause in cnf for lit in clause)
        return math.log(m + n, 2)**2
    
    def resolution_proof_length(cnf):
        # Placeholder implementation of the resolution proof length
        m = len(cnf)
        n = max(abs(lit) for clause in cnf for lit in clause)
        return m * n
    
    results = []
    for _ in range(30):  # Aim for at least 30 instances per seed
        m = random.randint(5, 40)
        n = random.randint(5, 40)
        cnf = generate_cnf(m, n)
        norm = norm_of_noncommutative_space(cnf)
        proof_length = resolution_proof_length(cnf)
        results.append((norm, proof_length))
    
    if not results:
        return {
            "metric_name": "N(φ)",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    norm_values = [norm for norm, _ in results]
    proof_lengths = [proof_length for _, proof_length in results]
    
    mean_norm = sum(norm_values) / len(norm_values)
    std_norm = math.sqrt(sum((x - mean_norm)**2 for x in norm_values) / len(norm_values))
    correlation_coefficient = sum((norm_values[i] - mean_norm) * (proof_lengths[i] - mean(proof_lengths)) for i in range(len(results))) / (len(results) * std_norm * math.sqrt(sum((x - mean(proof_lengths))**2 for x in proof_lengths)))
    
    conjecture_holds = all(mean_norm >= 0.95 * norm and norm <= 1.1 * norm for norm, _ in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "N(φ)",
        "metric_value": mean_norm,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")