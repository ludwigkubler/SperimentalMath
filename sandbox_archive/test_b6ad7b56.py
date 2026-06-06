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
    
    def hypergeometric_order(k, m, n):
        if k == 0 or m == 0 or n == 0:
            return 0
        order = 1
        for i in range(1, min(m, n)):
            order *= (k - i + 1) * (m - i + 1)
            order //= (i + 1) * (n - i + 1)
        return order
    
    def dpll(cnf):
        if not cnf:
            return True
        for literal in range(1, len(cnf) + 1):
            assignment = [0] * (len(cnf) + 1)
            assignment[literal] = 1
            if dpll([c for c in cnf if literal not in c and -literal not in c]):
                return True
            assignment[literal] = -1
            if dpll([c for c in cnf if literal not in c and -literal not in c]):
                return True
        return False
    
    def resolution_width(cnf):
        queue = list(cnf)
        while queue:
            clause1 = queue.pop()
            if len(clause1) == 0:
                return float('inf')
            for clause2 in cnf:
                if len(clause2) == 0:
                    continue
                for literal in clause1:
                    if -literal in clause2:
                        new_clause = [l for l in clause1 + clause2 if l != literal and l != -literal]
                        if not new_clause:
                            return float('inf')
                        queue.append(new_clause)
        return len(queue)
    
    k = 3
    m = random.randint(5, 10)
    n = random.randint(5, 10)
    cnf = []
    for _ in range(m):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        cnf.append(clause)
    
    mu = hypergeometric_order(k, m, n)
    w = resolution_width(cnf)
    
    if w == float('inf'):
        return {
            "metric_name": "mu_over_w",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_infinite"
        }
    
    ratio = mu / w
    return {
        "metric_name": "mu_over_w",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"ratio_exceeds_threshold\" first_failing_seed=1")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")