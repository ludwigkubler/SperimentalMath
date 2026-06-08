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
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def compute_clause_depth(cnf):
        max_depth = 0
        for clause in cnf:
            depth = sum(1 for lit in clause if lit > 0) + sum(1 for lit in clause if lit < 0)
            max_depth = max(max_depth, depth)
        return max_depth
    
    def compute_aos_complexity(cnf):
        n = len(set(abs(lit) for clause in cnf for lit in clause))
        matroid = [[i+1 for i in range(n)]]
        for clause in cnf:
            matroid.append([abs(lit) for lit in clause if abs(lit) not in matroid[0]])
        return len(matroid)
    
    n_max = 40
    instances_tested = 0
    total_aos = 0
    total_cd = 0
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(2 * n, 4 * n))
            cd = compute_clause_depth(cnf)
            aos = compute_aos_complexity(cnf)
            
            if aos <= cd:
                return {
                    "metric_name": "AOS vs CD",
                    "metric_value": aos,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": f"AOS({aos}) <= CD({cd})"
                }
            
            total_aos += aos
            total_cd += cd
            instances_tested += 1
    
    mean_aos = total_aos / instances_tested
    mean_cd = total_cd / instances_tested
    support_fraction = instances_tested / (n_max - 4) / 6
    
    return {
        "metric_name": "AOS vs CD",
        "metric_value": mean_aos,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_aos = sum(r["metric_value"] for r in results) / len(results)
    std_aos = math.sqrt(sum((r["metric_value"] - mean_aos) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_aos} std={std_aos:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"AOS <= CD\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")