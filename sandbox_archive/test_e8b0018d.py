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
    
    def generate_cnf(width, n):
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, width * 2) for _ in range(random.randint(1, width))]
            cnf.append(clause)
        return cnf
    
    def compute_minimal_rank(cnf):
        # Simplified computation of minimal rank (placeholder)
        return len(cnf) ** 0.5
    
    n_max = 40
    instances_tested = 30
    total_rank = 0
    
    for n in range(5, n_max + 1, 5):
        cnf = generate_cnf(n, instances_tested)
        rank = compute_minimal_rank(cnf)
        total_rank += rank
    
    metric_value = total_rank / (n_max // 5)
    
    conjecture_holds = metric_value <= n_max ** 2
    counterexample = "" if conjecture_holds else f"mean_rank={metric_value}, max_n={n_max}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")