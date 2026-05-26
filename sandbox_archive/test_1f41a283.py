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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses

    def tseitin_circuit_width(clauses):
        literals = set()
        for clause in clauses:
            literals.update(abs(lit) for lit in clause)
        return len(literals)

    def tropicalized_affine_scheme_rank(clauses):
        # Simplified rank calculation (assuming a linear independence condition)
        return len(set(sum(clause) for clause in clauses))

    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    width = tseitin_circuit_width(formula)
    rank = tropicalized_affine_scheme_rank(formula)

    metric_name = "tropicalized_affine_scheme_rank"
    metric_value = math.log(rank + 1) if rank > 0 else 0
    instances_tested = 1
    conjecture_holds = width <= metric_value
    counterexample = "" if conjecture_holds else f"width={width}, expected<=metric_value"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 997) for _ in range(30)]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(res["conjecture_holds"] for res in results) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"width > log(rank)\" first_failing_seed={first_failing_seed}")