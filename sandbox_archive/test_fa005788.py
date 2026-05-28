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
    
    def generate_k_cnf(n, density):
        num_clauses = int(density * n * (n - 1) / 2)
        variables = list(range(1, n + 1))
        clauses = set()
        while len(clauses) < num_clauses:
            clause = random.sample(variables, 2)
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clause.sort()
            clauses.add(tuple(clause))
        return clauses
    
    def algebraic_curve_rank(n):
        # Placeholder for actual computation of minimal rank
        # This is a dummy implementation for testing purposes
        return n + 1
    
    def communication_complexity(k_cnf):
        # Placeholder for actual computation of communication complexity
        # This is a dummy implementation for testing purposes
        return len(k_cnf)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    density = random.uniform(1.0, 1.5)
    k_cnf = generate_k_cnf(n, density)
    rank = algebraic_curve_rank(n)
    cc = communication_complexity(k_cnf)
    
    metric_name = "communication_complexity_bound"
    metric_value = cc
    instances_tested = 1
    conjecture_holds = cc <= math.log(rank)
    counterexample = "" if conjecture_holds else f"CC({n}, {density})={cc} > log({rank})"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or failure rate too low")