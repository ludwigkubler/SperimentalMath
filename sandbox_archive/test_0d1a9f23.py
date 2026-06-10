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
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.random() < 0.5:
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def circuit_ranks(cnf):
        n = len(cnf[0])
        ranks = [0] * (2**n)
        for clause in cnf:
            mask = sum(1 << abs(lit) - 1 if lit > 0 else -(1 << abs(lit) - 1) for lit in clause)
            ranks[mask] += 1
        return max(ranks)
    
    def sat_complexity(cnf):
        n = len(cnf[0])
        clauses = [set(abs(lit) for lit in clause) for clause in cnf]
        variables = set(range(1, n + 1))
        
        def dfs(model):
            if not variables:
                return True
            var = next(iter(variables))
            model[var] = True
            if all(var in clause or -var not in clause for clause in clauses):
                if dfs(model):
                    return True
            model[var] = False
            if all(-var in clause or var not in clause for clause in clauses):
                if dfs(model):
                    return True
            variables.remove(var)
            return False
        
        model = {}
        return len(next(filter(dfs, [{}]), {}))
    
    n_values = [5, 10, 15, 20, 30, 40]
    mcrs = []
    sat_complexities = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        mcr = circuit_ranks(cnf)
        sat_complexity = sat_complexity(cnf)
        mcrs.append(mcr)
        sat_complexities.append(sat_complexity)
    
    if len(mcrs) < 30 or len(sat_complexities) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(mcrs),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation = sum((mcr - m_avg) * (sat_complexity - s_avg) for mcr, sat_complexity in zip(mcrs, sat_complexities)) / len(mcrs)
    m_avg = sum(mcrs) / len(mcrs)
    s_avg = sum(sat_complexities) / len(sat_complexities)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "correlation_coefficient < 0.7"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")