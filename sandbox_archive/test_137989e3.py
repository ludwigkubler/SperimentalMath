# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict, deque

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(n):
            A[i][j] /= A[i][i]
        for k in range(m):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    rank = sum(1 for row in A if any(row))
    return rank

def resolution_depth(clauses):
    n = len(clauses)
    variables = set()
    for clause in clauses:
        for literal in clause:
            variables.add(abs(literal))
    
    variable_to_clauses = defaultdict(list)
    for i, clause in enumerate(clauses):
        for literal in clause:
            variable_to_clauses[abs(literal)].append(i)
    
    queue = deque(variables)
    resolved = set()
    
    while queue:
        var = queue.popleft()
        if var in resolved:
            continue
        resolved.add(var)
        
        for clause_index in variable_to_clauses[var]:
            clause = clauses[clause_index]
            new_clause = []
            for literal in clause:
                if abs(literal) != var:
                    new_clause.append(literal)
            if not new_clause:
                return math.inf
            queue.append(abs(new_clause[0]))
    
    return len(resolved)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables = list(range(1, n + 1))
    clauses = []
    
    for _ in range(n):
        clause = [random.choice([1, -1]) * random.choice(variables) for _ in range(random.randint(1, n))]
        if not any(literal == -var for literal, var in zip(clause, variables)):
            clauses.append(clause)
    
    d = resolution_depth(clauses)
    r = gaussian_elimination([[int(lit > 0), int(lit < 0)] for clause in clauses for lit in clause])
    
    return {
        "metric_name": "minimal_representation_rank",
        "metric_value": r,
        "instances_tested": len(clauses),
        "conjecture_holds": d <= math.log2(r) if r > 0 else False,
        "counterexample": "" if d <= math.log2(r) else f"Counterexample: resolution_depth={d}, minimal_representation_rank={r}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_r = sum(result["metric_value"] for result in results) / len(results)
    std_r = math.sqrt(sum((result["metric_value"] - mean_r) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")