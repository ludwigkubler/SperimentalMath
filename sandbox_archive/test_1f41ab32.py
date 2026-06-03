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

def gaussian_elimination(A, b):
    n = len(b)
    A_b = [A[i] + [b[i]] for i in range(n)]
    
    for i in range(n):
        if A_b[i][i] == 0:
            for j in range(i+1, n):
                if A_b[j][i] != 0:
                    A_b[i], A_b[j] = A_b[j], A_b[i]
                    break
            else:
                raise ValueError("No non-zero pivot found")
        
        for j in range(n):
            if i != j:
                factor = Fraction(A_b[j][i], A_b[i][i])
                A_b[j] = [A_b[j][k] - factor * A_b[i][k] for k in range(n+1)]
    
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(A_b[i][-1], A_b[i][i])
        for j in range(i-1, -1, -1):
            A_b[j][-1] -= A_b[j][i] * x[i]
    
    return x

def generate_cnf(n, m):
    cnf = []
    literals = list(range(1, n+1)) + [-x for x in range(1, n+1)]
    for _ in range(m):
        clause = random.sample(literals, 3)
        cnf.append(clause)
    return cnf

def dpll(cnf, assignment=[]):
    if not cnf:
        return True
    unit_clause = next((c for c in cnf if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        if literal < 0 and -literal in assignment:
            return False
        elif literal > 0 and literal not in assignment:
            assignment.append(literal)
            return dpll([c for c in cnf if literal not in c], assignment)
    p = random.choice([-1, 1])
    literal = p * (random.randint(1, len(cnf)))
    if literal < 0 and -literal in assignment:
        return False
    elif literal > 0 and literal not in assignment:
        assignment.append(literal)
        return dpll([c for c in cnf if literal not in c], assignment) or dpll([c for c in cnf if -literal not in c], assignment)
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    proof_depths = []
    
    for n in n_values:
        cnf = generate_cnf(n, 2*n)
        rank = len(gaussian_elimination([[random.randint(0, 1) for _ in range(n)] for _ in range(n)], [random.randint(0, 1) for _ in range(n)]))
        depth = dpll(cnf)
        
        min_ranks.append(rank)
        proof_depths.append(depth)
    
    correlation_coefficient = sum((min_ranks[i] - mean_min_ranks) * (proof_depths[i] - mean_proof_depths) for i in range(len(min_ranks))) / len(min_ranks)
    p_value = 2 * (1 - math.comb(30, int(abs(correlation_coefficient * math.sqrt(30)) + 1)))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_ranks),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value < 0.05,
        "counterexample": "" if correlation_coefficient >= 0.7 and p_value < 0.05 else "Correlation too low or p-value too high"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_min_ranks = sum(result["metric_value"] for result in results) / len(results)
    mean_proof_depths = sum(result["instances_tested"] * result["metric_value"] for result in results) / sum(result["instances_tested"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_min_ranks} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation too low or p-value too high\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason: All trials used n=1")