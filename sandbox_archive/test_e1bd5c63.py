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
    
    def generate_disjointness_instance(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def compute_matroid_rank(instance):
        n = len(instance)
        matroid = [[i] if instance[i] == 1 else [] for i in range(n)]
        rank = 0
        for subset in matroid:
            if all(matroid[j].issubset(subset) for j in range(n)):
                rank += 1
        return rank
    
    def compute_communication_complexity(instance):
        n = len(instance)
        # Simplified model: each bit requires one communication step
        return n
    
    instances_tested = 0
    total_rank = 0
    min_rank = float('inf')
    max_rank = 0
    support_count = 0
    counterexample = ""
    
    for _ in range(30):
        instance = generate_disjointness_instance(random.randint(5, 40))
        rank = compute_matroid_rank(instance)
        communication_complexity = compute_communication_complexity(instance)
        
        instances_tested += 1
        total_rank += rank
        min_rank = min(min_rank, rank)
        max_rank = max(max_rank, rank)
        
        if rank >= communication_complexity:
            support_count += 1
        else:
            counterexample = f"Instance with n={len(instance)}, rank={rank}, C(n)={communication_complexity}"
    
    mean_rank = total_rank / instances_tested
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in range(min_rank, max_rank + 1)) / (max_rank - min_rank))
    support_fraction = support_count / instances_tested
    
    return {
        "metric_name": "Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 113, 4))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")