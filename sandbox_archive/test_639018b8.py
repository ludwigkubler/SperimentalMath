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
    
    def communication_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] != f[0]:
                rank += 1
        return rank
    
    def quaternionic_representation_size(rank):
        return 2 * rank - 1
    
    def approximate_function(f, representation):
        n = len(f)
        approximations = [sum(representation[i]) % 2 for i in range(n)]
        return approximations
    
    def communication_cost(approximation, f):
        return sum(1 for a, b in zip(approximation, f) if a != b)
    
    def mean(lst):
        return Fraction(sum(lst), len(lst))
    
    def std(lst, m):
        return (sum((x - m)**2 for x in lst) / len(lst))**0.5
    
    n = 10
    communication_rank_threshold = n
    max_instances_per_seed = 30
    instances_tested = 0
    total_k = 0
    total_communication_cost = 0
    total_approximation_error = 0
    counterexample = ""
    
    while instances_tested < max_instances_per_seed:
        f = generate_boolean_function(n)
        rank = communication_rank(f)
        
        if rank > communication_rank_threshold:
            k = quaternionic_representation_size(rank)
            approximation = approximate_function(f, [random.randint(0, 1) for _ in range(k)])
            communication_cost_value = communication_cost(approximation, f)
            approximation_error = sum(abs(a - b) for a, b in zip(approximation, f))
            
            total_k += k
            total_communication_cost += communication_cost_value
            total_approximation_error += approximation_error
            
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "communication_cost",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_k = total_k / instances_tested
    mean_communication_cost = total_communication_cost / instances_tested
    mean_approximation_error = total_approximation_error / instances_tested
    
    if mean_approximation_error > 3 * std([total_approximation_error] * instances_tested, mean_approximation_error):
        counterexample = "Approximation error too high"
    
    return {
        "metric_name": "communication_cost",
        "metric_value": mean_communication_cost,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": mean_k <= 4 * communication_rank_threshold**2 and counterexample == "",
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_k = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
    std_k = (sum((r["metric_value"] - mean_k)**2 for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"]))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_k} std={std_k} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no valid instances found")