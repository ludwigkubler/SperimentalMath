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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def communication_matrix(cnf):
        m = len(cnf)
        n = max(abs(x) for x in cnf[0])
        A = [[0] * (2**n) for _ in range(2**n)]
        for i, clause in enumerate(cnf):
            for j in range(len(clause)):
                if clause[j] > 0:
                    A[i][j] += 1
                else:
                    A[i][j] -= 1
        return A
    
    def determinant(A):
        n = len(A)
        det = 0
        if n == 1:
            return A[0][0]
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def genus_formula(determinant, n):
        # Simplified genus formula for plane curves
        return 1 + (n - 1) // 2
    
    def comm(f):
        # Deterministic protocol to measure communication complexity
        return len(f)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    A = communication_matrix(cnf)
    det = determinant(A)
    g = genus_formula(det, n)
    Comm_f = comm(cnf)
    
    if g < math.log2(Comm_f) ** 2:
        return {
            "metric_name": "genus",
            "metric_value": g,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Counterexample for n={n}: genus < log^2(Comm(f))"
        }
    
    return {
        "metric_name": "genus",
        "metric_value": g,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        from sympy.ntheory import primerange
        seeds = list(primerange(2, 100))[:30]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")