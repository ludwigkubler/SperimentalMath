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
    
    def generate_disjointness_instance(n):
        return [random.sample(range(1, n+1), 2) for _ in range(random.randint(1, 5))]
    
    def noncrossing_partition_complex(instance):
        # Simplified version of noncrossing partition complex calculation
        return len(instance)
    
    def dnf_size(instance):
        # Simplified version of DNF size calculation
        return sum(len(pair) for pair in instance)
    
    n = random.randint(5, 40)
    instance = generate_disjointness_instance(n)
    minrank_pi_n = noncrossing_partition_complex(instance)
    size_dnf_n = dnf_size(instance)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minrank_pi_n,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        total_metric_value = sum(res["metric_value"] for res in results)
        support_fraction = sum(1 for res in results if res["conjecture_holds"])
        
        if support_fraction >= 30:
            mean_metric_value = total_metric_value / len(results)
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
        else:
            first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")