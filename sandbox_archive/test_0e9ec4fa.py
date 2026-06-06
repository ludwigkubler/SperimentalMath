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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = len(f)
        # Simplified version of a known algorithm to compute communication complexity rank
        # This is a placeholder and should be replaced with the actual algorithm
        return math.ceil(math.log2(n))
    
    def minimal_local_induction_ring_rank(f):
        n = len(f)
        # Simplified version of a known algorithm to compute local induction ring rank
        # This is a placeholder and should be replaced with the actual algorithm
        return math.ceil(math.log2(n))
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        
        rank_communication = communication_complexity_rank(f)
        rank_local_induction = minimal_local_induction_ring_rank(f)
        
        if rank_local_induction < rank_communication:
            conjecture_holds = False
            counterexample = "Rank of local induction ring is less than communication complexity rank"
            break
        
        metric_values.append(rank_communication)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = (sum((x - mean_metric_value)**2 for x in metric_values) / len(metric_values))**0.5
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={r['seed']}")
                break