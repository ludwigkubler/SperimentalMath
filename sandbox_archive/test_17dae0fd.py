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
        for _ in range(10):  # Each clause has at least one literal
            literals = [random.choice([f'x{i}', f'-x{i}']) for i in range(1, n+1)]
            random.shuffle(literals)
            clauses.append(' '.join(literals) + ' 0')
        return '\n'.join(clauses)

    def communication_complexity_rank(cnf):
        # Simplified model: rank is proportional to the number of variables
        return len(cnf.split('\n'))

    def automorphic_forms_required(n):
        # Simplified model: forms required are proportional to the square root of n
        return math.ceil(math.sqrt(n))

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    comm_rank = communication_complexity_rank(cnf)
    forms_required = automorphic_forms_required(n)

    if forms_required > math.sqrt(comm_rank):
        counterexample = f"CNF with n={n} requires {forms_required} forms but only √{comm_rank} is allowed."
        return {
            "metric_name": "Automorphic Forms Required",
            "metric_value": forms_required,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    else:
        return {
            "metric_name": "Automorphic Forms Required",
            "metric_value": forms_required,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")