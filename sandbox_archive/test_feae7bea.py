# auto-injected by SEC sandbox
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
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause.reverse()
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        seen = set()
        queue = cnf[:]
        while queue:
            clause1 = queue.pop()
            for clause2 in cnf:
                common_lits = [lit for lit in clause1 if -lit in clause2]
                if len(common_lits) == 1:
                    lit = next(lit for lit in clause1 if lit > 0 and -lit not in seen)
                    seen.add(lit)
                    new_clause = [l for l in clause2 if l != -lit] + [lit]
                    if new_clause not in queue:
                        queue.append(new_clause)
        return len(seen)

    def algebraic_coadjointness(n):
        # Placeholder function for algebraic coadjointness
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()

    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        proof_width = resolution_width(cnf)
        coadjointness = algebraic_coadjointness(n)
        metrics.append((proof_width, coadjointness))
    
    correlation_coefficient = calculate_correlation(metrics)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else "correlation_too_low"
    }

def calculate_correlation(data):
    n = len(data)
    if n < 2:
        return None
    
    x_sum = sum(x for x, _ in data)
    y_sum = sum(y for _, y in data)
    xy_sum = sum(x * y for x, y in data)
    x_square_sum = sum(x**2 for x, _ in data)
    y_square_sum = sum(y**2 for _, y in data)
    
    numerator = n * xy_sum - x_sum * y_sum
    denominator = math.sqrt((n * x_square_sum - x_sum**2) * (n * y_square_sum - y_sum**2))
    
    if denominator == 0:
        return None
    
    return numerator / denominator

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    mean = sum(metric_values) / len(metric_values) if metric_values else None
    std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values)) if mean is not None else None
    
    if support_fraction >= 0.8:
        result = f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample='correlation_too_low' first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE insufficient_data"
    
    print(result)