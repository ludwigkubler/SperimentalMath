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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(1, n), random.randint(1, n)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses
    
    def noncrossing_partition(clauses):
        partition = {}
        for clause in clauses:
            for var in clause:
                if var not in partition:
                    partition[var] = []
                partition[var].append(clause)
        return partition
    
    def complexity(partition, n):
        max_clauses_per_var = max(len(partition[var]) for var in range(1, n+1))
        return max_clauses_per_var * n
    
    n = random.randint(5, 40)
    m = random.randint(n, n*3)
    clauses = generate_3cnf(n, m)
    partition = noncrossing_partition(clauses)
    metric_value = complexity(partition, n)
    
    conjecture_holds = metric_value >= (m ** (1/4)) * (n ** (5/12))
    counterexample = f"Complexity {metric_value} < {(m ** (1/4)) * (n ** (5/12))}" if not conjecture_holds else ""
    
    return {
        "metric_name": "complexity",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")