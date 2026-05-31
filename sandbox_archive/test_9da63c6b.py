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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            cnf.append(clause)
        return cnf
    
    def count_satisfying_assignments(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        assignments = [0] * (2 ** n)
        for assignment in range(2 ** n):
            satisfied = True
            for clause in cnf:
                if all((assignment >> abs(lit) - 1) & 1 != (lit > 0) for lit in clause):
                    satisfied = False
                    break
            if satisfied:
                assignments[assignment] = 1
        return sum(assignments)
    
    def second_betti_number(cnf, n):
        # Simplified approximation of the second Betti number
        m = len(cnf)
        return Fraction(m * (m - 1), 2 * n)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        m = random.randint(n, 2 * n)
        cnf = generate_cnf(n, m)
        t_F = count_satisfying_assignments(cnf)
        H2_F = second_betti_number(cnf, n)
        results.append((t_F, H2_F))
    
    if any(H2_F > 20 for _, H2_F in results):
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in results),
            "conjecture_holds": False,
            "counterexample": "H^2_F > 20"
        }
    
    t_F_values = [t_F for t_F, _ in results]
    H2_F_values = [H2_F for _, H2_F in results]
    
    mean_t_F = sum(t_F_values) / len(t_F_values)
    std_t_F = (sum((x - mean_t_F) ** 2 for x in t_F_values) / len(t_F_values)) ** 0.5
    
    correlation = sum((t_F - mean_t_F) * (H2_F - mean_H2_F) for t_F, H2_F in results)
    correlation /= std_t_F * (sum((H2_F - mean_H2_F) ** 2 for H2_F in H2_F_values) / len(H2_F_values)) ** 0.5
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and all(r["metric_value"] is not None for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data_or_invalid_metric")