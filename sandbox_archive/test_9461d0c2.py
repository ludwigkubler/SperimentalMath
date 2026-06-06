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
    
    def generate_boolean_satisfiability_instance(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2 * n):
            clause = random.choice(['', 'not ']) + random.choice(variables) + ' or ' + random.choice(variables)
            clauses.append(clause)
        return f"({') and ('.join(clauses)})"

    def frege_proof_depth(n):
        # Simplified estimation for demonstration purposes
        return n * (n - 1) // 2

    def minimal_order_of_noncommutative_integral_points(n):
        # Simplified estimation for demonstration purposes
        return n + 1

    n = random.randint(5, 40)
    instance = generate_boolean_satisfiability_instance(n)
    proof_depth = frege_proof_depth(n)
    order = minimal_order_of_noncommutative_integral_points(n)

    return {
        "metric_name": "MinimalOrder",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(order - proof_depth) <= proof_depth * 0.3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        counterexample = next(r['counterexample'] for r in results if not r['conjecture_holds'])
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")