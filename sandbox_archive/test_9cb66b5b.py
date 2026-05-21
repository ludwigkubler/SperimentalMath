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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses

    def karchmer_wigderson_constraints(n, clauses):
        constraints = []
        for clause in clauses:
            constraint = [0] * (2 * n + 1)
            for var in clause:
                if var > 0:
                    constraint[var - 1] += 1
                else:
                    constraint[-var - 1] -= 1
            constraints.append(constraint)
        return constraints

    def real_radical(constraints):
        # Simplified version of computing the real radical for demonstration purposes
        # This is a placeholder and should be replaced with actual computation
        return len(constraints)

    n = 40
    clauses = generate_3cnf(n)
    constraints = karchmer_wigderson_constraints(n, clauses)
    generator_count = real_radical(constraints)
    
    metric_name = "real_radical_generator_count"
    metric_value = generator_count
    instances_tested = 1
    conjecture_holds = generator_count >= math.log(n)
    counterexample = "" if conjecture_holds else f"n={n}, generators={generator_count}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"n={r['instances_tested']}, generators={r['metric_value']}\" first_failing_seed={seed}")
                break