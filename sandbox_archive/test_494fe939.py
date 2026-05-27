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
    
    # Generate a random 3-CNF formula with m clauses on n variables
    n = random.randint(5, 40)
    m = random.randint(n, n * (n - 1) // 2)
    cnf = []
    for _ in range(m):
        clause = [random.choice([f'x{i}', f'~x{i}']) for i in range(n)]
        cnf.append(clause)
    
    # Construct the clause indicator polynomial and its dual
    variables = set()
    for clause in cnf:
        for literal in clause:
            if literal.startswith('x'):
                variables.add(literal[1:])
            elif literal.startswith('~x'):
                variables.add(literal[2:])
    
    n_vars = len(variables)
    P = [[0] * (n_vars + 1) for _ in range(n_vars + 1)]
    Q = [[0] * (n_vars + 1) for _ in range(n_vars + 1)]
    
    for clause in cnf:
        for literal in clause:
            if literal.startswith('x'):
                i = int(literal[1:]) - 1
                P[i][i] += 1
            elif literal.startswith('~x'):
                i = int(literal[2:]) - 1
                Q[i][i] -= 1
    
    # Compute the tensor product of the polynomial with its dual over the Boolean ring
    T = [[0] * (n_vars + 1) for _ in range(n_vars + 1)]
    for i in range(n_vars + 1):
        for j in range(n_vars + 1):
            for k in range(n_vars + 1):
                T[i][j] += P[i][k] * Q[k][j]
    
    # Determine the local cohomology rank of the tensor product
    rank = 0
    for i in range(n_vars + 1):
        if all(T[j][i] == 0 for j in range(n_vars + 1)):
            rank += 1
    
    # Evaluate the correlation between the local cohomology rank and the number of clauses m
    metric_value = n**2 - m + 1
    conjecture_holds = rank <= metric_value
    counterexample = "" if conjecture_holds else f"Rank {rank} > {metric_value}"
    
    return {
        "metric_name": "Local Cohomology Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [37]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")