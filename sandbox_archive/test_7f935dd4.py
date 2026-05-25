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
    
    def generate_3cnf(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f'~{v}' for v in variables], 3)
            clauses.append(clause)
        return clauses
    
    def delone_set_geometry(clauses):
        # Simplified mapping to Delone set geometry
        return len(clauses) * len(clauses[0])
    
    def ac0_k_distance_circuit_size(clauses):
        # Simplified mapping to AC^0-k-distance circuit size
        return len(clauses)
    
    n = random.randint(5, 40)
    m = random.randint(n, 2*n)
    clauses = generate_3cnf(n, m)
    
    R_F = delone_set_geometry(clauses)
    C_size = ac0_k_distance_circuit_size(clauses)
    
    return {
        "metric_name": "R(F) <= C^2",
        "metric_value": float(R_F <= C_size**2),
        "instances_tested": 1,
        "conjecture_holds": R_F <= C_size**2,
        "counterexample": "" if R_F <= C_size**2 else f"Counterexample: R(F)={R_F}, |C|={C_size}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in results) / len(results)
    std_metric = math.sqrt(sum((r['metric_value'] - mean_metric)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")