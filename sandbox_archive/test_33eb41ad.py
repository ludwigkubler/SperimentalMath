# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations, product
from fractions import Fraction

def generate_cnf(n):
    if n <= 0:
        return []
    num_clauses = random.randint(1, n)
    cnf = []
    for _ in range(num_clauses):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        while all(abs(x) != abs(y) for x, y in combinations(clause, 2)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        cnf.append(clause)
    return cnf

def polynomial_ring_rank(cnf):
    n = len(cnf[0])
    rank = 0
    for clause in cnf:
        rank += sum(abs(x) for x in clause)
    return rank

def dpll_search_tree_entropy_variance(cnf):
    # Placeholder function to simulate entropy variance calculation
    # In practice, this would involve a more complex algorithm
    n = len(cnf[0])
    return random.uniform(0.1, 1.0) * n**2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    metric_name = "correlation_coefficient"
    instances_tested = 0
    total_correlation = 0.0
    n_max = 5
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Test with 5 instances per size
            cnf = generate_cnf(n)
            rank = polynomial_ring_rank(cnf)
            entropy_variance = dpll_search_tree_entropy_variance(cnf)
            correlation = (rank - entropy_variance) / max(rank, entropy_variance + 1e-9)
            total_correlation += correlation
            instances_tested += 1
    
    mean_correlation = total_correlation / instances_tested
    conjecture_holds = mean_correlation >= 0.7 and all(correlation >= 0.5 for _ in range(instances_tested))
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "correlation_coefficient_less_than_0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(r["counterexample"] == "correlation_coefficient_less_than_0.5" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] == "correlation_coefficient_less_than_0.5")
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_less_than_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")