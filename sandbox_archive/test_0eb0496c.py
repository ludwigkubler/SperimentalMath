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
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def count_satisfying_assignments(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        assignments = [i for i in range(-n, n + 1) if all((lit > 0 and i & lit) or (lit < 0 and not i & -lit) for clause in cnf)]
        return len(assignments)
    
    def p_adic_log_order(n):
        if n == 0:
            return 0
        order = 0
        while n % 2 == 0:
            n //= 2
            order += 1
        return order
    
    def communication_complexity_rank(cnf):
        m, n = len(cnf), max(abs(lit) for clause in cnf for lit in clause)
        rank = 0
        for i in range(n):
            if any(i & lit > 0 or -i & lit < 0 for clause in cnf):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = int(1.5 * n)  # Varying clause-to-variable ratio
        cnf = generate_cnf(n, m)
        num_satisfying_assignments = count_satisfying_assignments(cnf)
        p_log_order = p_adic_log_order(num_satisfying_assignments)
        rank = communication_complexity_rank(cnf)
        
        results.append({
            "n": n,
            "m": m,
            "num_satisfying_assignments": num_satisfying_assignments,
            "p_log_order": p_log_order,
            "rank": rank
        })
    
    if not results:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    p_log_orders = [result["p_log_order"] for result in results]
    ranks = [result["rank"] for result in results]
    
    mean_p_log_order = sum(p_log_orders) / len(p_log_orders)
    mean_rank = sum(ranks) / len(ranks)
    
    correlation_coefficient = (sum((p_log_orders[i] - mean_p_log_order) * (ranks[i] - mean_rank) for i in range(len(p_log_orders))) /
                               math.sqrt(sum((p_log_orders[i] - mean_p_log_order) ** 2 for i in range(len(p_log_orders))) *
                                         sum((ranks[i] - mean_rank) ** 2 for i in range(len(ranks)))))
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": "" if correlation_coefficient >= 0.5 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")