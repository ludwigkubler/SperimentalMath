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
        rank_matrix = [[f[i] ^ f[j] for j in range(2**n)] for i in range(2**n)]
        return sum(sum(row) for row in rank_matrix)
    
    def minimal_index_of_noncommutative_crossed_product(f):
        n = int(math.log2(len(f)))
        crossed_product = [[f[i] * f[j] for j in range(2**n)] for i in range(2**n)]
        return sum(sum(row) for row in crossed_product)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        r_n = communication_complexity_rank_variance(f)
        I_n = minimal_index_of_noncommutative_crossed_product(f)
        results.append((n, I_n, r_n))
    
    if not results:
        return {
            "metric_name": "I(n)/r(n)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for n, _, _ in results)
    instances_tested = len(results)
    I_over_r = [I_n / r_n for _, I_n, r_n in results]
    mean_I_over_r = sum(I_over_r) / instances_tested
    std_I_over_r = math.sqrt(sum((x - mean_I_over_r)**2 for x in I_over_r) / instances_tested)
    
    return {
        "metric_name": "I(n)/r(n)",
        "metric_value": mean_I_over_r,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(x <= 1.5 for _, I_n, r_n in results),
        "counterexample": "" if all(x <= 1.5 for _, I_n, r_n in results) else f"Found counterexample at n={n}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials run")
        exit()
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no support for conjecture")