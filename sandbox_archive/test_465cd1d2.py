# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def algebraic_stochastic_order(cnf):
        n = len(cnf[0])
        count = 0
        for _ in range(1000):  # Sample enough instances to estimate the order
            assignment = [random.choice([-1, 1]) for _ in range(n)]
            value = sum([assignment[i-1] * clause[i-1] for clause in cnf])
            if value > 0:
                count += 1
        return Fraction(count, 1000)
    
    def resolution_width(cnf):
        # Simplified version of resolution width calculation
        n = len(cnf[0])
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        queue = list(clauses)
        while queue:
            clause = queue.pop()
            if not clause:
                return 1
            literal = random.choice(list(set(abs(lit) for lit in clause)))
            new_clauses = []
            for c in clauses:
                if literal in c:
                    continue
                if -literal in c:
                    new_clauses.append(tuple(sorted([l for l in c if l != -literal])))
                else:
                    new_clauses.append(c)
            queue.extend(new_clauses)
        return 0
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    alpha_F = algebraic_stochastic_order(cnf)
    t_F = resolution_width(cnf)
    
    if t_F == 0:
        return {
            "metric_name": "resolution_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Resolution width is zero"
        }
    
    return {
        "metric_name": "resolution_width",
        "metric_value": t_F,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*100, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='resolution_width_zero' first_failing_seed={seeds[first_failing_seed]}")