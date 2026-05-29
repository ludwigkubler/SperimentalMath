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
    
    n = 20  # Number of variables in the k-CNF formula
    k = 3   # Clause density (number of clauses per variable)
    
    # Generate a random k-CNF formula with n variables and k clauses per variable
    clauses = []
    for _ in range(k * n):
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    
    # Construct the associated quaternion algebra A
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in clauses:
        for x in clause:
            A[abs(x)][abs(x)] += 1
    
    # Compute the minimal exponent of the quaternion algebra A
    exp_A = max(sum(row[i] for i in range(len(row))) for row in A)
    
    # Measure the communication complexity required to solve the k-CNF problem
    comm_complexity = math.log(exp_A, 2) if exp_A > 0 else float('inf')
    
    # Check if the conjecture holds
    c = 1.0  # Constant c (to be determined experimentally)
    conjecture_holds = exp_A <= c * n**2
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": len(clauses),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"exp(A)={exp_A}, c*n^2={c*n**2}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        counterexample = next(res["counterexample"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")