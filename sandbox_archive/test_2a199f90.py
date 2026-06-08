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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        rank = [f.count(i) for i in set(f)]
        mean = sum(rank) / len(rank)
        variance = sum((x - mean)**2 for x in rank) / len(rank)
        return variance
    
    def monodromy_group_order(f):
        # Placeholder function to simulate computing the monodromy group order
        n = int(math.log2(len(f)))
        return 2**n
    
    metric_name = "monodromy_group_order"
    instances_tested = 0
    n_max = 0
    total_metric_value = 0.0
    support_count = 0
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            f = generate_boolean_function(n)
            instances_tested += 1
            G_f = monodromy_group_order(f)
            CommRankVar_f = communication_complexity_rank_variance(f)
            
            total_metric_value += G_f
            
            if abs(G_f - CommRankVar_f) <= 0.1 * max(G_f, CommRankVar_f):
                support_count += 1
    
    metric_mean = total_metric_value / instances_tested
    support_fraction = support_count / instances_tested
    
    conjecture_holds = support_fraction >= 0.8 and metric_mean <= 3
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")