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
    
    def generate_group(n):
        if n == 1:
            return [0]
        elif n == 2:
            return [0, 1]
        else:
            g = [0, 1]
            for i in range(2, n):
                new_element = sum(g) % n
                if new_element not in g:
                    g.append(new_element)
            return g
    
    def adjoint_representation(group):
        n = len(group)
        rep = [[0] * n for _ in range(n)]
        for i in range(n):
            rep[i][group[i]] = 1
        return rep
    
    def communication_complexity_rank(rep, n):
        rank = 0
        for col in zip(*rep):
            if sum(col) > 0:
                rank += 1
        return rank
    
    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        group = generate_group(n)
        rep = adjoint_representation(group)
        rank = communication_complexity_rank(rep, n)
        results.append(rank)
    
    if not results:
        return {
            "metric_name": "Var_R(n)",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_var = variance(results)
    min_order = len(group) - 1
    
    return {
        "metric_name": "Var_R(n)",
        "metric_value": mean_var,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.4 <= (min_order / mean_var) <= 1.2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["instances_tested"] > 0 for result in results):
        print("RESULT: INCONCLUSIVE reason=insufficient_data")
    else:
        mean_var = sum(result["metric_value"] for result in results) / len(results)
        std_var = math.sqrt(sum((result["metric_value"] - mean_var) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if 0.8 <= (result["min_order"] / result["metric_value"]) <= 1.2) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_var} std={std_var} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not (0.4 <= (result["min_order"] / result["metric_value"]) <= 1.2))
            print(f"RESULT: FALSIFIED counterexample=\"seed {first_failing_seed}\" first_failing_seed={first_failing_seed}")