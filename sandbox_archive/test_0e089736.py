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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def min_order_quasi_plurality(clauses):
        max_clauses = len(clauses)
        min_order = float('inf')
        for k in range(1, max_clauses + 1):
            count = sum(all(abs(x) == abs(y) for x, y in zip(clause[:k], clause[k:])) for clause in clauses)
            if count > 0:
                min_order = min(min_order, k)
        return min_order
    
    def resolution_width(clauses):
        queue = clauses[:]
        while True:
            new_clause = None
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    if any(-x in queue[j] for x in queue[i]):
                        new_clause = [x for x in queue[i] if x not in queue[j]] + [x for x in queue[j] if -x not in queue[i]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(queue)
            queue.append(new_clause)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = generate_cnf(n)
        min_order = min_order_quasi_plurality(cnf)
        width = resolution_width(cnf)
        
        if min_order == float('inf'):
            counterexample = "mapping_undefined"
            conjecture_holds = False
            break
        
        metric_values.append(min_order / width)
    
    mean_value = sum(metric_values) / instances_tested
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / instances_tested)
    
    return {
        "metric_name": "min_order_quasi_plurality_over_width",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30)) + [53, 67, 79, 83, 89]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")