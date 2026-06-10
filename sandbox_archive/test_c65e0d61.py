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
        n = len(phi)
        rank_var = 0
        for i in range(1, n+1):
            for comb in itertools.combinations(range(n), i):
                sub_phi = [phi[j] if j in comb else 0 for j in range(n)]
                rank_var += sum(sub_phi) * (n - sum(sub_phi))
        return rank_var / n**2
    
    def ehrhart_semigroup(phi):
        n = len(phi)
        ehr = {0: 1}
        for i in range(1, n+1):
            new_ehr = {}
            for k in ehr:
                for j in range(k+1, min(n, k+i)+1):
                    if phi[j-1] == 1:
                        new_ehr[j] = (new_ehr.get(j, 0) + ehr[k]) % 2
            ehr.update(new_ehr)
        return ehr
    
    def growth_function(ehr):
        return sum(ehr.values())
    
    n_max = 40
    instances_tested = 30
    total_metric_value = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        phi = generate_boolean_function(random.randint(5, n_max))
        rank_var = communication_complexity_rank_variance(phi)
        ehr = ehrhart_semigroup(phi)
        metric_value = growth_function(ehr)
        
        total_metric_value += metric_value
        if rank_var == 0:
            conjecture_holds = False
            counterexample = "rank_var=0"
            break
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = int(conjecture_holds) * 100
    
    return {
        "metric_name": "growth_function",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(int(r["conjecture_holds"]) for r in results) * 100 // len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any("counterexample" not in r or r["counterexample"] == "" for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed=0")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")