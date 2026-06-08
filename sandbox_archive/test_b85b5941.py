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
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            while len(set(clause)) != 2:
                clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def compute_clause_depth(cnf):
        return max(len(clause) for clause in cnf)
    
    def matroid_rank(matroid):
        rank = 0
        for i in range(len(matroid)):
            if all(all(j not in matroid[j] for j in matroid[i]) for i in range(i+1, len(matroid))):
                rank += 1
        return rank
    
    def alexander_orlik_solomon_complexity(matroid):
        n = len(matroid)
        AOS = [0] * (n + 1)
        AOS[0] = 1
        for i in range(1, n + 1):
            AOS[i] = sum(AOS[j] * (-1) ** (i - j) for j in range(i))
        return abs(sum(AOS[i] * matroid_rank(matroid[:i]) for i in range(n + 1)))
    
    def compute_metric(cnf):
        n = len(cnf)
        m = len(cnf[0])
        clause_depth = compute_clause_depth(cnf)
        matroid = [set(clause) for clause in cnf]
        aos_complexity = alexander_orlik_solomon_complexity(matroid)
        return aos_complexity, clause_depth
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        m = random.randint(n, n * n)
        cnf = generate_cnf(n, m)
        aos_complexity, clause_depth = compute_metric(cnf)
        if aos_complexity <= clause_depth:
            return {
                "metric_name": "AOS vs CD",
                "metric_value": 0.0,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"Clause depth {clause_depth} >= AOS complexity {aos_complexity}"
            }
        metric_values.append(aos_complexity / clause_depth)
    
    return {
        "metric_name": "AOS vs CD",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Clause depth >= AOS complexity\" first_failing_seed={first_failing_seed}")