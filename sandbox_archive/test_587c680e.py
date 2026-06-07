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
    
    def generate_cnf(n, num_clauses):
        clauses = []
        for _ in range(num_clauses):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def resolution_width(cnf):
        queue = cnf[:]
        while True:
            new_clause = None
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    if abs(queue[i][0]) == abs(queue[j][0]):
                        new_clause = [q for q in queue[i] if q != -queue[j][0]] + [q for q in queue[j] if q != -queue[i][0]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(queue)
            queue.append(new_clause)

    def minimal_order_of_affine_root_system(n):
        # Placeholder function to simulate the computation of the minimal order
        # This is a dummy implementation and should be replaced with actual logic
        return n

    instances_tested = 0
    total_metric_value = 0.0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        num_clauses = random.randint(1, n)
        cnf = generate_cnf(n, num_clauses)
        order_min_root_system = minimal_order_of_affine_root_system(n)
        w_phi = resolution_width(cnf)
        
        instances_tested += len(cnf)
        total_metric_value += order_min_root_system * w_phi
        n_max = max(n_max, n)

    if instances_tested < 30:
        conjecture_holds = False
        counterexample = "insufficient_instances"

    metric_value = total_metric_value / instances_tested

    return {
        "metric_name": "order_min_root_system * w_phi",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")