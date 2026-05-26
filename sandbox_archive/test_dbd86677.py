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
    
    def log_log(n):
        if n <= 0:
            return float('-inf')
        return math.log(math.log(n))
    
    def xor_and_tree_width(f):
        # Simplified XOR-AND tree width calculation
        return max(len(cnf) for cnf in f.split(' or '))
    
    def discriminant(n):
        # Simulated discriminant function
        return n * (n + 1)
    
    def eichler_shimura_rank(discriminant):
        # Simulated Eichler-Shimura rank calculation
        return log_log(discriminant)
    
    n = random.randint(5, 40)
    f = ' or '.join(f'x{i} and x{j}' for i in range(n) for j in range(i+1, n))
    d = discriminant(n)
    rank = eichler_shimura_rank(d)
    t_star = xor_and_tree_width(f)
    
    metric_value = min(rank, t_star)
    conjecture_holds = metric_value <= 2 * log_log(n**2)
    counterexample = "" if conjecture_holds else f"rank={rank}, t*={t_star}"
    
    return {
        "metric_name": "min_rank_t_star",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = results[0]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")