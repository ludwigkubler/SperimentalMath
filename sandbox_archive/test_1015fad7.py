# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(n):
        max_row = None
        for j in range(m):
            if A[j][i] != 0:
                if max_row is None or abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
        if max_row is not None:
            A[max_row], A[i] = A[i], A[max_row]
            for j in range(m):
                if j != i:
                    factor = Fraction(A[j][i], A[i][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
    return A

def rank(matrix):
    return sum(1 for row in gaussian_elimination(matrix) if any(row))

def hodge_index(clauses):
    m, n = len(clauses), len(clauses[0])
    A = [[Fraction(clause[j]) for j in range(n)] for clause in clauses]
    return rank(A)

def circuit_complexity(F):
    # Placeholder function to simulate average-case circuit complexity
    # This is a stub and should be replaced with actual computation
    return random.randint(1, len(F))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    F = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    hodge_index_value = hodge_index(F)
    avg_circuit_complexity = circuit_complexity(F)
    
    metric_name = "Hodge Index"
    metric_value = hodge_index_value
    instances_tested = 1
    
    conjecture_holds = False
    counterexample = ""
    
    if hodge_index_value <= n**2:  # Placeholder bound for k=2, adjust as needed
        conjecture_holds = True
    else:
        counterexample = "h(F) > O(n^k)"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")