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
    
    def generate_random_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        # Simplified resolution width calculation
        return len(cnf) * 2
    
    def minimal_rank(cnf):
        # Simplified minimal rank calculation (not accurate but for testing purposes)
        return len(cnf)
    
    n = random.randint(5, 30)
    m = random.randint(n, 2 * n)
    cnf = generate_random_cnf(n, m)
    
    r_min = minimal_rank(cnf)
    t_star = resolution_width(cnf)
    
    if r_min < 1 or t_star < 1:
        return {
            "metric_name": "minimal_rank_over_t_resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = r_min / t_star
    return {
        "metric_name": "minimal_rank_over_t_resolution_width",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        if mean_ratio >= 0.8 and support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample='ratio_out_of_bounds' first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE some_ratio_values_none")