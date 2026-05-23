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
    
    def generate_instance(n):
        return [random.randint(1, n) for _ in range(n)]
    
    def tensor_product(a, b):
        result = []
        for x in a:
            for y in b:
                result.append(x * y)
        return result
    
    def tropicalize(lst):
        return max(lst)
    
    def acc0_circuit_complexity(instance):
        # Placeholder function; actual implementation needed
        return 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance_a = generate_instance(n)
        instance_b = generate_instance(n)
        tensor_result = tensor_product(instance_a, instance_b)
        tropical_rank = tropicalize(tensor_result)
        complexity = acc0_circuit_complexity(tensor_result)
        
        results.append({
            "n": n,
            "tropical_rank": tropical_rank,
            "complexity": complexity
        })
    
    mean_tropical_rank = sum(result["tropical_rank"] for result in results) / len(results)
    mean_complexity = sum(result["complexity"] for result in results) / len(results)
    std_metric_value = (sum((result["tropical_rank"] - mean_tropical_rank) ** 2 for result in results) / len(results)) ** 0.5
    
    conjecture_holds = all(result["tropical_rank"] <= n**2 * math.log(n, 2) and result["complexity"] >= n**2 * math.log(n, 2) for result in results)
    
    return {
        "metric_name": "tropical_rank",
        "metric_value": mean_tropical_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={results[0]['n']}, tropical_rank={results[0]['tropical_rank']} > O(n^2 log n)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")