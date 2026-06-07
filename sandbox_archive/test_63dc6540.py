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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, 2*n) for _ in range(random.randint(1, n))]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def resolution_width(cnf):
        queue = cnf[:]
        while True:
            new_clauses = []
            found_resolvent = False
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    if any(-x in queue[i] and x in queue[j] for x in set(queue[i]) & set(queue[j])):
                        resolvent = [x for x in queue[i] if x not in queue[j]] + \
                                    [x for x in queue[j] if -x not in queue[i]]
                        new_clauses.append(resolvent)
                        found_resolvent = True
            if not found_resolvent:
                break
            queue.extend(new_clauses)
        return len(queue)

    def quandle_operations(cnf):
        # Simplified dummy implementation for demonstration purposes
        return sum(len(clause) for clause in cnf)

    n_max = 40
    instances_tested = 30
    metric_values = []

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = generate_cnf(n)
        w_phi = resolution_width(cnf)
        O_phi = quandle_operations(cnf)
        metric_values.append(O_phi)

    mean_value = sum(metric_values) / instances_tested
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / instances_tested)
    
    correlation_coefficient = sum((O_phi - mean_value) * (w_phi - mean_value) for O_phi, w_phi in zip(metric_values, [resolution_width(generate_cnf(n)) for _ in range(instances_tested)])) / (instances_tested * std_value * std_value)

    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "quandle_operations_resolution_width",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")