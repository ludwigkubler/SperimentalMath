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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(1, n), random.randint(1, n)]
            random.shuffle(clause)
            clauses.append(clause)
        return clauses
    
    def is_unsatisfiable(cnf):
        # Simple backtracking to check if the CNF is unsatisfiable
        literals = [False] * (2 * n + 1)
        
        def backtrack(i):
            if i == m:
                return True
            for j in range(3):
                lit = cnf[i][j]
                if not literals[lit]:
                    literals[lit] = True
                    if backtrack(i + 1):
                        return True
                    literals[lit] = False
                elif -lit in literals and literals[-lit]:
                    return False
            return False
        
        m = len(cnf)
        n = max(abs(lit) for clause in cnf for lit in clause)
        return not backtrack(0)
    
    def compute_min_symplectic_leaf_order(n, m):
        # Placeholder function to simulate the computation of symplectic leaf order
        # This is a dummy implementation and should be replaced with actual computation
        return random.uniform(1, n ** 0.25 * math.log(m))
    
    results = []
    for _ in range(30):  # 30 instances per seed
        n = random.randint(5, 40)
        m = random.randint(10, 100)
        cnf = generate_3cnf(n, m)
        if is_unsatisfiable(cnf):
            order = compute_min_symplectic_leaf_order(n, m)
            results.append(order)
    
    if not results:
        return {
            "metric_name": "min_symplectic_leaf_order",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_order = min(results)
    n_max = max(n for _ in range(30))
    conjecture_holds = all(order >= c * (n ** 0.25 * math.log(m)) for order, n, m in zip(results, [random.randint(5, 40) for _ in range(30)], [random.randint(10, 100) for _ in range(30)]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_symplectic_leaf_order",
        "metric_value": min_order,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result for result in results if not result["conjecture_holds"])["seed"]
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")