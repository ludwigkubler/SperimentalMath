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

def generate_cnf(m, n):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def count_satisfying_assignments(cnf):
    n = len(cnf[0])
    assignments = [i for i in range(-2**n + 1, 2**n)]
    valid_assignments = []
    for assignment in assignments:
        if all(any((lit > 0 and assignment & lit) or (lit < 0 and not assignment & -lit) for clause in cnf) for lit in range(1, n + 1)):
            valid_assignments.append(assignment)
    return len(valid_assignments)

def p_adic_log_order(x):
    if x == 0:
        return float('-inf')
    order = 0
    while x % 2 == 0:
        x //= 2
        order += 1
    return order

def communication_complexity_rank(cnf):
    m, n = len(cnf), len(cnf[0])
    rank = 0
    for i in range(m):
        rank = max(rank, sum(1 for lit in cnf[i] if abs(lit) <= n))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    m_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for m in m_values:
        cnf = generate_cnf(m, m)
        num_satisfying_assignments = count_satisfying_assignments(cnf)
        p_adic_order_value = p_adic_log_order(num_satisfying_assignments)
        rank_value = communication_complexity_rank(cnf)
        
        results.append({
            "m": m,
            "num_satisfying_assignments": num_satisfying_assignments,
            "p_adic_order_value": p_adic_order_value,
            "rank_value": rank_value
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
    
    p_adic_order_values = [r["p_adic_order_value"] for r in results]
    rank_values = [r["rank_value"] for r in results]
    
    mean_p_adic_order = sum(p_adic_order_values) / len(p_adic_order_values)
    std_p_adic_order = math.sqrt(sum((x - mean_p_adic_order) ** 2 for x in p_adic_order_values) / len(p_adic_order_values))
    mean_rank = sum(rank_values) / len(rank_values)
    
    correlation_coefficient = (sum((p_adic_order_values[i] - mean_p_adic_order) * (rank_values[i] - mean_rank) for i in range(len(results))) /
                               (len(results) * std_p_adic_order * math.sqrt(sum((x - mean_rank) ** 2 for x in rank_values))))
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(m_values),
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": "" if correlation_coefficient >= 0.5 else f"correlation_coefficient={correlation_coefficient:.2f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if result['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction:.2f}")