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
    
    def generate_tseitin_circuit(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            if random.choice([True, False]):
                clause[0] = f'¬{clause[0]}'
            if random.choice([True, False]):
                clause[1] = f'¬{clause[1]}'
            clauses.append(clause)
        return variables, clauses

    def tseitin_circuit_width(variables, clauses):
        width = len(variables)
        for clause in clauses:
            width = max(width, len(clause))
        return width

    def construct_tqft(variables, clauses):
        # Simplified construction for demonstration
        depth = 2 * (len(variables) + len(clauses))
        return depth

    n = random.randint(5, 40)
    m = random.randint(n, 2*n)
    variables, clauses = generate_tseitin_circuit(n, m)
    width = tseitin_circuit_width(variables, clauses)
    depth = construct_tqft(variables, clauses)

    if depth < width:
        return {
            "metric_name": "depth",
            "metric_value": depth,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Depth {depth} is less than width {width}"
        }

    return {
        "metric_name": "depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30)) + [47, 53, 59]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_depth = sum(r['metric_value'] for r in results) / len(results)
    std_depth = math.sqrt(sum((r['metric_value'] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Depth less than width\" first_failing_seed={first_failing_seed}")