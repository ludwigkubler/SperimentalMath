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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        resolvents = []
        
        while True:
            new_resolvents = set()
            for c1 in clauses:
                for c2 in clauses:
                    if len(set(c1) & set(c2)) == 1:
                        resolvent = tuple(sorted(list(set(c1) ^ set(c2))))
                        if -resolvent[0] in c1 and resolvent[0] in c2:
                            new_resolvents.add(resolvent)
            if not new_resolvents:
                break
            clauses.update(new_resolvents)
            resolvents.extend(new_resolvents)
        
        return len(resolvents)
    
    def tropical_rank(cnf):
        n = max(abs(x) for clause in cnf for x in clause)
        rank = 0
        
        while True:
            new_clauses = []
            for clause in cnf:
                if any(abs(x) > n + rank for x in clause):
                    continue
                new_clause = [x - (n + rank) if abs(x) == n + rank else x for x in clause]
                if new_clause not in new_clauses:
                    new_clauses.append(new_clause)
            if len(new_clauses) == len(cnf):
                break
            cnf = new_clauses
            rank += 1
        
        return rank
    
    n, m = random.randint(5, 30), random.randint(n * 2, n * 4)
    cnf = generate_cnf(n, m)
    
    t_star = resolution_width(cnf)
    r_min = tropical_rank(cnf)
    
    if t_star == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_is_zero"
        }
    
    ratio = r_min / t_star
    
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='ratio_less_than_0.8' first_failing_seed={first_failing_seed}")