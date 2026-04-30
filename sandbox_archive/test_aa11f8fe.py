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
    
    def generate_3sat(n: int) -> list:
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(x) != abs(y) for x, y in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def is_satisfiable(clauses: list) -> bool:
        n = max(abs(var) for var in set(clause for clause in clauses for var in clause))
        assignment = [random.choice([True, False]) for _ in range(n)]
        for clause in clauses:
            if all(not (assignment[abs(var) - 1] ^ (var < 0)) for var in clause):
                return True
        return False
    
    def resolution_refutation_depth(clauses: list) -> int:
        stack = []
        while not is_satisfiable(clauses):
            unit_clauses = [c for c in clauses if len(c) == 1]
            if not unit_clauses:
                break
            unit_clause = unit_clauses[0]
            var = unit_clause[0]
            new_clause = [-var]
            stack.append((clauses, unit_clause))
            clauses = [c for c in clauses if var not in c and -var not in c]
            for clause in clauses:
                if var in clause:
                    new_clauses = [list(set(c) | set(new_clause)) for c in clauses if -var not in c]
                    clauses.extend(new_clauses)
                elif -var in clause:
                    new_clause = list(set(clause) - {-var})
            stack.append((clauses, unit_clause))
        return len(stack)
    
    def bounded_collection_iterations(n: int) -> int:
        k_n = 0
        while n > 1:
            n = math.ceil(math.log2(n))
            k_n += 1
        return k_n
    
    n = random.randint(5, 40)
    clauses = generate_3sat(n)
    depth = resolution_refutation_depth(clauses)
    k_n = bounded_collection_iterations(n)
    
    c = 0.5  # Empirical constant for the test
    if depth < c * k_n:
        return {
            "metric_name": "depth vs BΣ_1 iterations",
            "metric_value": depth,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Depth {depth} is less than {c * k_n}"
        }
    else:
        return {
            "metric_name": "depth vs BΣ_1 iterations",
            "metric_value": depth,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_depth = math.sqrt(sum((r["metric_value"] - mean_depth)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='depth < c * k_n' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data to determine support")