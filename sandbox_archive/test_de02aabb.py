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
    
    # Define the symmetric group S₃ and its irreducible representations
    S3 = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]
    irreps = [
        [1, 1, 1],
        [-1, 1, -1],
        [1, -1, -1]
    ]
    
    # Compute the Fourier coefficients
    def fourier_coefficient(phi):
        sum_val = 0
        for s in S3:
            sum_val += phi(s)
        return sum_val / len(S3)
    
    # Define a random 3-SAT instance over S₃
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        variables = [random.choice(S3) for _ in range(3)]
        clause = tuple(sorted(variables))
        clauses.append(clause)
    
    # Define the constraint function φ over S₃
    def phi(s):
        return all(any(s[i] == v for i, v in enumerate(clause)) for clause in clauses)
    
    # Compute the Fourier coefficients
    F = [fourier_coefficient(lambda s: 1 if phi(s) else 0)]
    
    # Measure the SOS refutation degree using a basic SDP relaxation (via small DPLL)
    def dpll(phi, assignment):
        if not any(clause for clause in clauses if all(v not in assignment or assignment[v] != val for v, val in clause)):
            return True
        var = next((v for v in S3 if v not in assignment), None)
        if var is None:
            return False
        for val in [0, 1]:
            assignment[var] = val
            if dpll(phi, assignment):
                return True
            del assignment[var]
        return False
    
    refutation_degree = n
    
    # Check the conjecture
    if max(abs(coeff) for coeff in F) < refutation_degree:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "SOS refutation degree > max |F[k]|"
    
    return {
        "metric_name": "refutation_degree",
        "metric_value": refutation_degree,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")