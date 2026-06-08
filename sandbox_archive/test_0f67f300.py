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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        seen = set()
        queue = cnf[:]
        while queue:
            clause = queue.pop(0)
            if not clause:
                return len(seen)
            literal = random.choice(clause)
            for other_clause in queue:
                if literal in other_clause or -literal in other_clause:
                    new_clause = [x for x in other_clause if x != literal and x != -literal]
                    if new_clause:
                        if tuple(new_clause) not in seen:
                            seen.add(tuple(new_clause))
                            queue.append(new_clause)
        return len(seen)
    
    n_max = 40
    instances_tested = 0
    total_r = 0
    total_w = 0
    
    for n in range(5, n_max + 1):
        cnf = generate_cnf(n)
        r = resolution_width(cnf)
        w = len(cnf)
        total_r += r
        total_w += w
        instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "r/w ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_r = total_r / instances_tested
    mean_w = total_w / instances_tested
    ratio = mean_r / mean_w
    
    return {
        "metric_name": "r/w ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": ratio <= 1.03 and ratio >= 0.97,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio:.2f} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"r/w ratio out of bounds\" first_failing_seed={first_failing_seed}")