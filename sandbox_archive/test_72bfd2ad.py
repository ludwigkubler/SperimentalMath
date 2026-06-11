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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            cnf.append(clause)
        return cnf
    
    def qsi(cnf):
        # Constructive mapping to quasi-symmetric space index (simplified example)
        unique_clauses = set(tuple(sorted(clause)) for clause in cnf)
        return len(unique_clauses)
    
    def resolution_width(cnf):
        # Simplified resolution width calculation
        max_level = 0
        levels = [set()]
        while True:
            new_levels = set()
            for level in levels:
                for clause1 in cnf:
                    for clause2 in cnf:
                        if len(set(clause1) & set(clause2)) == 1:
                            new_clause = list(set(clause1) ^ set(clause2))
                            new_level = {tuple(sorted(new_clause))}
                            if not any(new_level.issubset(l) for l in levels):
                                new_levels.update(new_level)
            if not new_levels:
                break
            levels.append(new_levels)
            max_level += 1
        return max_level
    
    instances_tested = 0
    total_qsi = 0
    total_width = 0
    n_max = 5
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n, int(1.5 * n))
            qsi_value = qsi(cnf)
            width = resolution_width(cnf)
            
            instances_tested += 1
            total_qsi += qsi_value
            total_width += width
            
            if n > n_max:
                n_max = n
    
    mean_qsi = Fraction(total_qsi, instances_tested)
    mean_width = Fraction(total_width, instances_tested)
    
    correlation_coefficient = (total_qsi - instances_tested * mean_qsi) / math.sqrt(instances_tested * (1 - instances_tested / n_max))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else f"qsi={mean_qsi}, width={mean_width}"
    
    return {
        "metric_name": "correlation",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")