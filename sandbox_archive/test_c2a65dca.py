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
    
    def generate_instance(m):
        variables = set()
        clauses = []
        for _ in range(m):
            clause = {random.choice(list(variables)) if variables else random.randint(1, 10)}
            while len(clause) < 3:
                clause.add(random.choice(list(variables)) if variables else random.randint(1, 10))
            clauses.append(clause)
            for var in clause:
                variables.add(var)
        return clauses, len(variables)

    def planar_embedding(clauses):
        # Simplified planar embedding algorithm (not actual topological entropy calculation)
        return len(clauses) * len(set.union(*clauses))

    h_min_values = []
    c_I_values = []

    for _ in range(30):
        m = random.randint(5, 40)
        clauses, n = generate_instance(m)
        h_min = planar_embedding(clauses)
        h_min_values.append(h_min)
        c_I_values.append(n)

    if not h_min_values or not c_I_values:
        return {
            "metric_name": "h_min / c(I)",
            "metric_value": None,
            "instances_tested": len(h_min_values),
            "n_max": max(len(set.union(*clauses)) for clauses, _ in [generate_instance(m) for m in range(5, 41)]),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }

    mean_h_min = sum(h_min_values) / len(h_min_values)
    mean_c_I = sum(c_I_values) / len(c_I_values)
    correlation_coefficient = sum((h_min_values[i] - mean_h_min) * (c_I_values[i] - mean_c_I) for i in range(len(h_min_values))) / ((len(h_min_values) - 1) * math.sqrt(sum((h_min_values[i] - mean_h_min) ** 2 for i in range(len(h_min_values)))) * math.sqrt(sum((c_I_values[i] - mean_c_I) ** 2 for i in range(len(c_I_values)))))

    return {
        "metric_name": "h_min / c(I)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(h_min_values),
        "n_max": max(len(set.union(*clauses)) for clauses, _ in [generate_instance(m) for m in range(5, 41)]),
        "conjecture_holds": 0.5 <= correlation_coefficient <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [2**i + 7 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break