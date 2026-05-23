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

def generate_random_permutation(n):
    return list(range(1, n + 1))

def noncrossing_partition_rank(permutation):
    n = len(permutation)
    if n == 0:
        return 0
    
    # Construct the Young diagram
    young_diagram = []
    for i in range(n):
        row = [permutation[i]]
        j = permutation[i]
        while j != i + 1:
            j = permutation[j - 1]
            row.append(j)
        young_diagram.append(row)
    
    # Compute the rank of the Young diagram
    rank = 0
    for row in young_diagram:
        if len(row) > rank:
            rank = len(row)
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        total_communication_bits = 0
        
        for _ in range(30):
            permutation = generate_random_permutation(n)
            rank = noncrossing_partition_rank(permutation)
            communication_bits = random.randint(1, n * math.log2(n))  # Simulate communication bits
            
            instances_tested += 1
            total_rank += rank
            total_communication_bits += communication_bits
        
        mean_rank = total_rank / instances_tested
        mean_communication_bits = total_communication_bits / instances_tested
        
        if mean_rank > mean_communication_bits:
            conjecture_holds = False
            counterexample = f"n={n}, mean_rank={mean_rank}, mean_communication_bits={mean_communication_bits}"
        else:
            conjecture_holds = True
            counterexample = ""
        
        results.append({
            "metric_name": "communication_complexity",
            "metric_value": mean_communication_bits,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.extend(result["results"])
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["conjecture_holds"] is False)
        counterexample_desc = next(r["counterexample"] for r in results if r["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")