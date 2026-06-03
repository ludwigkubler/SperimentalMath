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
    for _ in range(m):
        clause = [random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n)
                  for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def count_satisfying_assignments(cnf):
    n = max(abs(lit) for clause in cnf for lit in clause)
    assignments = [i for i in range(-n, n + 1) if all((lit > 0 and i & lit) or (lit < 0 and not i & -lit) for clause in cnf)]
    return len(assignments)

def p_adic_log_order(n):
    if n == 0:
        return float('-inf')
    order = 0
    while n % 2 == 0:
        n //= 2
        order += 1
    return order

def communication_complexity_rank(cnf):
    # Placeholder function; actual implementation depends on the specific problem
    return len(cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        m = int(n * (n + 1) / 2)  # Example clause-to-variable ratio
        cnf = generate_cnf(n, m)
        
        num_satisfying_assignments = count_satisfying_assignments(cnf)
        p_adic_order_value = p_adic_log_order(num_satisfying_assignments)
        rank_value = communication_complexity_rank(cnf)
        
        results.append({
            "n": n,
            "p_adic_order": p_adic_order_value,
            "rank": rank_value
        })
    
    if not results:
        return {
            "metric_name": "p-adic Logarithmic Order vs Communication Complexity Rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    p_adic_orders = [r["p_adic_order"] for r in results]
    ranks = [r["rank"] for r in results]
    
    mean_p_adic_order = sum(p_adic_orders) / len(p_adic_orders)
    mean_rank = sum(ranks) / len(ranks)
    
    correlation_coefficient = sum((p - mean_p_adic_order) * (r - mean_rank) for p, r in zip(p_adic_orders, ranks)) / \
                              math.sqrt(sum((p - mean_p_adic_order) ** 2 for p in p_adic_orders) *
                                        sum((r - mean_rank) ** 2 for r in ranks))
    
    return {
        "metric_name": "p-adic Logarithmic Order vs Communication Complexity Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else f"Correlation coefficient: {correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='Correlation coefficient below 0.5' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")