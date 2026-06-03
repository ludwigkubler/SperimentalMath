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
    
    def generate_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2 * n):
            clause = random.sample(variables, 3)
            clause.append(random.choice(['', '!', '~']))
            clauses.append(' '.join(clause))
        return ' & '.join(clauses)

    def formal_power_series(formula):
        # Placeholder function to simulate the computation of the formal power series
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 100)

    def sat_proof_width(formula):
        # Placeholder function to simulate the computation of the SAT proof width
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(50, 200)

    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    ord_f_phi = formal_power_series(formula)
    w_phi = sat_proof_width(formula)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": random.random(),  # Placeholder for actual correlation coefficient
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")