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
    
    def generate_explicit_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def acc0_circuit_threshold(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            return None
        return n
    
    def tropicalized_boolean_algebra(f):
        n = len(f)
        TBA = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                TBA[i][j] = max(TBA[i-1][j], TBA[i][j-1])
                if f[j-1] == 1:
                    TBA[i][j] += 1
        return TBA
    
    def tensor_product_rank(TBA):
        n = len(TBA) - 1
        rank = 0
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                if TBA[i][j] > rank:
                    rank = TBA[i][j]
        return rank
    
    def constructive_mapping(f):
        n = len(f)
        TBA = tropicalized_boolean_algebra(f)
        return tensor_product_rank(TBA)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_explicit_function(n)
        t = acc0_circuit_threshold(f)
        if t is None:
            continue
        rank = constructive_mapping(f)
        if rank is not None:
            results.append((n, t, rank))
    
    if len(results) < 30:
        return {
            "metric_name": "tensor_product_rank_over_acc0",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    total_rank = sum(rank for _, _, rank in results)
    mean_rank = total_rank / len(results)
    std_rank = math.sqrt(sum((rank - mean_rank) ** 2 for _, _, rank in results) / len(results))
    
    support_count = sum(1 for _, t, rank in results if 0.8 <= rank / t <= 1.2)
    support_fraction = support_count / len(results)
    
    return {
        "metric_name": "tensor_product_rank_over_acc0",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"support_fraction={support_fraction:.2f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_rank = sum(result["metric_value"] for result in results if result["metric_value"] is not None)
    mean_rank = total_rank / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_count = sum(1 for result in results if result["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank:.2f} std={std_rank:.2f} support_fraction={support_fraction:.2f}")
    elif any(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction={support_fraction:.2f}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction:.2f}")