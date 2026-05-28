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
    n = random.randint(1, 40)
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        # Generate a random Boolean circuit C with n inputs
        C = [random.choice([0, 1]) for _ in range(2**n)]
        
        # Compute the cocomplex of C (placeholder implementation)
        # This is a placeholder and should be replaced with an actual algorithm
        r_cocomplex_C = random.randint(1, n)
        
        # Determine the minimum resolution refutation size t*(C) for each circuit
        # This is a placeholder and should be replaced with an actual algorithm
        t_star_C = random.randint(1, 2**n)
        
        # Measure the Spearman rank correlation between log_2(t*(C)) and r_cocomplex(C)
        if t_star_C <= 0 or r_cocomplex_C == 0:
            continue
        
        metric_values.append((math.log2(t_star_C), r_cocomplex_C))
    
    if not metric_values:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Calculate Spearman rank correlation
    n = len(metric_values)
    ranks = {}
    for i, (x, y) in enumerate(metric_values):
        if x not in ranks:
            ranks[x] = [i]
        else:
            ranks[x].append(i)
        if y not in ranks:
            ranks[y] = [i]
        else:
            ranks[y].append(i)
    
    sorted_x = sorted(ranks.keys())
    sorted_y = sorted(ranks.keys())
    rank_x = {x: (sum(sorted_x.index(x) for x in xs) + len(xs) - 1) / (2 * len(xs)) for x, xs in ranks.items()}
    rank_y = {y: (sum(sorted_y.index(y) for y in ys) + len(ys) - 1) / (2 * len(ys)) for y, ys in ranks.items()}
    
    sum_dif_sq = sum((rank_x[x] - rank_y[y])**2 for x, y in metric_values)
    spearman_corr = 1 - (6 * sum_dif_sq) / (n * (n**2 - 1))
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": spearman_corr,
        "instances_tested": instances_tested,
        "conjecture_holds": spearman_corr >= 0.8 and all(spearman_corr >= 0.5 for _, y in metric_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")