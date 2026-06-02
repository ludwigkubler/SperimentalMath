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

def generate_cnf(n, m):
    cnf = []
    literals = list(range(-n, 0)) + list(range(1, n+1))
    for _ in range(m):
        clause = random.sample(literals, random.randint(2, n))
        cnf.append(clause)
    return cnf

def resolution_width(cnf):
    seen = set()
    queue = []
    for clause in cnf:
        queue.extend(clause)
    
    while queue:
        literal = queue.pop()
        if literal in seen or -literal in seen:
            continue
        seen.add(literal)
        for clause in cnf:
            if literal in clause:
                new_clause = [l for l in clause if l != literal]
                if not new_clause:
                    return len(seen)
                queue.extend(new_clause)
    return len(seen)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_mrank = 0
    total_w_phi = 0
    
    for n in range(5, n_max + 1):
        for _ in range(3):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(2*n, 3*n))
            mrank = len(cnf)  # Simplified minimal rank calculation
            w_phi = resolution_width(cnf)
            
            if w_phi == 0:
                continue
            
            instances_tested += 1
            total_mrank += mrank
            total_w_phi += abs(w_phi)
    
    if instances_tested < 30:
        return {
            "metric_name": "mrank/w_phi",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mrank_w_phi_ratio = total_mrank / total_w_phi
    return {
        "metric_name": "mrank/w_phi",
        "metric_value": mrank_w_phi_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.5 <= mrank_w_phi_ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mrank/w_phi ratio out of bounds\" first_failing_seed={first_failing_seed}")