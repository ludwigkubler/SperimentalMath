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
        # Simplified AC⁰ circuit for n inputs
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def convert_to_symplectic_form(circuit):
        # Simplified conversion to symplectic form
        return [[circuit[i] ^ circuit[j] for j in range(len(circuit))] for i in range(len(circuit))]
    
    def minimal_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] == 1 for j in range(rank, n)):
                rank += 1
                for j in range(n):
                    if matrix[j][i] == 1:
                        for k in range(n):
                            matrix[j][k] ^= matrix[i][k]
        return rank
    
    def log_n(n):
        return math.log2(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_ac0_circuit(n)
        symplectic_form = convert_to_symplectic_form(circuit)
        rank = minimal_rank(symplectic_form)
        expected_log_n = log_n(n)
        
        results.append({
            "n": n,
            "rank": rank,
            "expected_log_n": expected_log_n
        })
    
    total_tests = len(results)
    supported_count = 0
    
    for result in results:
        if abs(result["rank"] - result["expected_log_n"]) <= 3:
            supported_count += 1
    
    conjecture_holds = supported_count / total_tests >= 0.9
    counterexample = "" if conjecture_holds else "n={n}, rank={rank}, expected_log_n={expected_log_n}"
    
    return {
        "metric_name": "Rank vs Log(n)",
        "metric_value": sum(result["rank"] for result in results) / total_tests,
        "instances_tested": total_tests,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: FALSIFIED counterexample=\"n={result['n']}, rank={result['rank']}, expected_log_n={result['expected_log_n']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")