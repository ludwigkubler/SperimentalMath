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
    
    def communication_complexity_rank_variance(phi):
        n = int(math.log2(len(phi)))
        rank_var = sum(phi[i] != phi[j] for i in range(n) for j in range(i+1, n)) / (n * (n - 1))
        return rank_var
    
    def ehrhart_semigroup_growth_function(phi):
        n = int(math.log2(len(phi)))
        growth = [0] * (n + 1)
        growth[0] = 1
        for i in range(1, n + 1):
            growth[i] = sum(growth[j] for j in range(i))
        return growth
    
    def polynomial_degree(poly):
        return len(poly) - 1
    
    def is_polynomial_relationship(degree, rank_var):
        if degree > 2:
            return False
        if rank_var == 0:
            return True
        return abs(degree * rank_var**2 - 1) < 1e-6
    
    n_max = 40
    instances_tested = 0
    total_growth = 0
    total_rank_var = 0
    
    for n in range(5, 41):
        phi = generate_boolean_function(n)
        rank_var = communication_complexity_rank_variance(phi)
        growth = ehrhart_semigroup_growth_function(phi)
        degree = polynomial_degree(growth)
        
        instances_tested += 1
        total_growth += sum(growth)
        total_rank_var += rank_var
    
    mean_growth = total_growth / instances_tested
    mean_rank_var = total_rank_var / instances_tested
    conjecture_holds = is_polynomial_relationship(degree, mean_rank_var)
    
    return {
        "metric_name": "Ehrhart Semigroup Growth",
        "metric_value": mean_growth,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_growth = sum(r["metric_value"] for r in results) / len(results)
    std_growth = math.sqrt(sum((r["metric_value"] - mean_growth)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_growth} std={std_growth} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")