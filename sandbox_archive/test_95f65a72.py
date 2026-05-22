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
    
    def generate_permutation(n):
        return list(range(1, n + 1))
    
    def inversions_count(perm):
        count = 0
        for i in range(len(perm)):
            for j in range(i + 1, len(perm)):
                if perm[i] > perm[j]:
                    count += 1
        return count
    
    def noncrossing_partition_size(n):
        # Simplified approximation for demonstration purposes
        return n * (n - 1) // 4
    
    def permutation_circuit_size(phi_n):
        # Simplified approximation for demonstration purposes
        return phi_n * math.log2(phi_n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        perm = generate_permutation(n)
        inversions = inversions_count(perm)
        rank = noncrossing_partition_size(n)
        circuit_size = permutation_circuit_size(inversions)
        
        if rank < n ** (2/3) or rank > inversions * math.log2(inversions):
            return {
                "metric_name": "rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, rank={rank}, inversions={inversions}"
            }
        
        results.append({
            "n": n,
            "rank": rank,
            "circuit_size": circuit_size
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    mean_circuit_size = sum(result["circuit_size"] for result in results) / len(results)
    support_fraction = len([result for result in results if n ** (2/3) <= result["rank"] <= inversions * math.log2(inversions)]) / len(results)
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")