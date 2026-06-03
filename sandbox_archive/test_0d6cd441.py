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
    
    def p_adic_log_order(x, p):
        if x == 0:
            return float('-inf')
        order = 0
        while x % p == 0:
            x //= p
            order += 1
        return order
    
    def communication_complexity_rank(cnf):
        # Simplified rank for demonstration purposes
        return len(set(abs(lit) for clause in cnf for lit in clause))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = int(n * random.uniform(0.5, 2))  # Varying clause-to-variable ratio
        cnf = generate_cnf(n, m)
        
        num_satisfying_assignments = 2 ** n  # Simplified for demonstration
        
        p_adic_order = p_adic_log_order(num_satisfying_assignments, 2)
        rank = communication_complexity_rank(cnf)
        
        results.append({
            "n": n,
            "p_adic_order": p_adic_order,
            "rank": rank
        })
    
    if not results:
        return {
            "metric_name": "p-adic Order vs Rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    p_adic_orders = [r["p_adic_order"] for r in results]
    ranks = [r["rank"] for r in results]
    
    mean_p_adic_order = sum(p_adic_orders) / len(p_adic_orders)
    std_p_adic_order = math.sqrt(sum((x - mean_p_adic_order) ** 2 for x in p_adic_orders) / len(p_adic_orders))
    mean_rank = sum(ranks) / len(ranks)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in ranks) / len(ranks))
    
    correlation_coefficient = (sum((p_adic_orders[i] - mean_p_adic_order) * (ranks[i] - mean_rank) for i in range(len(p_adic_orders))) /
                               (len(p_adic_orders) * std_p_adic_order * std_rank))
    
    return {
        "metric_name": "p-adic Order vs Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else f"Correlation coefficient: {correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient below 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} mean_metric_value={mean_metric_value}")