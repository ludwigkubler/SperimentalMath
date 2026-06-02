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
    
    def generate_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n * 2) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(instance):
        # Simplified SAT solver using backtracking
        assignment = {i: None for i in range(1, len(instance) * 2 + 1)}
        
        def backtrack(i):
            if i > len(instance):
                return True
            for val in [True, False]:
                assignment[instance[i-1][0]] = val
                if all(any(not (x < 0 and not assignment[-x]) for x in clause) for clause in instance):
                    if backtrack(i + 1):
                        return True
                assignment[instance[i-1][0]] = None
            return False
        
        return backtrack(1)
    
    def resolution_width(instance):
        # Simplified resolution width calculation
        clauses = set(tuple(sorted(clause)) for clause in instance)
        queue = list(clauses)
        while queue:
            clause = queue.pop()
            if len(clause) == 0:
                return float('inf')
            unit_clause = next((x for x in clause if abs(x) not in assignment), None)
            if unit_clause is None:
                continue
            unit_val = assignment[unit_clause]
            new_clauses = set()
            for c in queue:
                if any(abs(x) == abs(unit_clause) and (x > 0) != unit_val for x in c):
                    continue
                new_c = tuple(sorted(set(c) - {unit_clause, -unit_clause}))
                if len(new_c) == 1:
                    return float('inf')
                new_clauses.add(new_c)
            queue.extend(new_clauses)
        return max(len(clause) for clause in clauses)
    
    def noncrossing_partitions(n):
        # Simplified calculation of minimal number of noncrossing partitions
        if n <= 1:
            return 1
        count = 0
        for i in range(1, n):
            count += noncrossing_partitions(i) * noncrossing_partitions(n - i)
        return count
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instance = generate_instance(n)
        if is_satisfiable(instance):
            width = resolution_width(instance)
            partitions = noncrossing_partitions(n)
            results.append((width, partitions))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No satisfiable instances generated"
        }
    
    widths = [r[0] for r in results]
    partitions = [r[1] for r in results]
    
    n = len(widths)
    mean_width = sum(widths) / n
    mean_partitions = sum(partitions) / n
    
    covariance = sum((widths[i] - mean_width) * (partitions[i] - mean_partitions) for i in range(n)) / n
    width_variance = sum((widths[i] - mean_width) ** 2 for i in range(n)) / n
    partitions_variance = sum((partitions[i] - mean_partitions) ** 2 for i in range(n)) / n
    
    correlation_coefficient = covariance / (math.sqrt(width_variance) * math.sqrt(partitions_variance))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(len(instance) for instance, _ in results),
        "conjecture_holds": correlation_coefficient > 0.9 and n >= 30,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] <= 0.6 or r["p_value"] >= 0.1 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"low correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")