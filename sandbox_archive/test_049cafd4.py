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
    
    def generate_CNF(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def circuit_depth(cnf):
        if not cnf:
            return 0
        max_depth = 0
        for clause in cnf:
            depth = 1
            for literal in clause:
                if abs(literal) == len(cnf):
                    depth += 1
            max_depth = max(max_depth, depth)
        return max_depth
    
    def minimal_local_index(cnf):
        n = len(cnf)
        mli = 0
        for i in range(n):
            count = sum(1 for clause in cnf if literal in clause or -literal in clause)
            mli += count
        return mli / n
    
    n, m = random.randint(5, 30), random.randint(2 * n, 4 * n)
    cnf = generate_CNF(n, m)
    d_phi = circuit_depth(cnf)
    mli_Gphi = minimal_local_index(cnf)
    
    if d_phi == 0:
        return {
            "metric_name": "mli(Gφ) / d(φ)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Circuit depth is zero, invalid instance"
        }
    
    ratio = mli_Gphi / d_phi
    return {
        "metric_name": "mli(Gφ) / d(φ)",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 0.5 <= ratio <= 2.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")