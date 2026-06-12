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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = -clause[0], -clause[1]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        queue = cnf[:]
        added = set()
        while True:
            new_clause = None
            for clause in queue:
                if len(clause) == 1:
                    literal = clause[0]
                    if -literal in added:
                        return len(added)
                    else:
                        added.add(literal)
                elif any(abs(lit) not in added for lit in clause):
                    new_clause = clause
                    break
            if new_clause is None:
                return 0
            queue.remove(new_clause)
            for other in queue:
                if any(abs(lit) == abs(new_clause[0]) and (lit > 0) != (new_clause[0] > 0) for lit in other):
                    new_other = [l for l in other if l != -new_clause[0]]
                    if len(new_other) == 1:
                        return len(added)
                    queue.remove(other)
                    queue.append(new_other)
    
    def symplectic_rank(n):
        # Placeholder function to simulate the computation of symplectic rank
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        rank = symplectic_rank(n)
        width = resolution_width(cnf)
        results.append({"n": n, "rank": rank, "width": width})
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    ranks = [result["rank"] for result in results]
    widths = [result["width"] for result in results]
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = (sum((x[i] - mean_x)**2 for i in range(n)) * sum((y[i] - mean_y)**2 for i in range(n)))**0.5
        return numerator / denominator if denominator != 0 else None
    
    correlation = pearson_correlation(ranks, widths)
    
    if correlation is None or abs(correlation) < 0.8:
        return {
            "metric_name": "correlation",
            "metric_value": correlation,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": f"low_correlation={correlation}"
        }
    
    if any(abs(rank - width) > 3 for rank, width in zip(ranks, widths)):
        return {
            "metric_name": "correlation",
            "metric_value": correlation,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": f"large_deviation"
        }
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["metric_value"] is not None for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")