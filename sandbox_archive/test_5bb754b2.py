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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.randint(0, 1) * 2 - 1 for _ in range(n)]
            clause = tuple(sorted(literals))
            if clause not in clauses:
                clauses.append(clause)
        return clauses
    
    def is_satisfied(clause, assignment):
        return any(assignment[abs(lit) - 1] == lit for lit in clause)
    
    def generate_algebra(clauses):
        n = len(clauses)
        algebra = {}
        for i in range(n):
            for j in range(i + 1, n):
                if is_satisfied((i + 1, j + 1), assignment) or is_satisfied((-i - 1, -j - 1), assignment):
                    algebra[(i, j)] = (j, i)
        return algebra
    
    def dimension(algebra, k):
        if k == 0:
            return 1
        dim = 1
        for i in range(k):
            dim *= len(set(algebra.get((j, i), None) for j in range(i)))
        return dim
    
    n = 40
    clauses = generate_3cnf(n)
    assignment = {i: random.choice([-1, 1]) for i in range(n)}
    
    algebra = generate_algebra(clauses)
    dims = [dimension(algebra, k) for k in range(1, 11)]
    
    tseitin_width = len(max([set(c) for c in clauses], key=len))
    
    metric_value = sum(dims) / len(dims)
    conjecture_holds = all(dim >= 2**(k/2) for k, dim in enumerate(dims, start=1)) and tseitin_width >= math.log(n, 2)
    counterexample = "" if conjecture_holds else f"Tseitin width {tseitin_width} < log n ({math.log(n, 2)}) or dim(A_Φ_k) < 2^{k/2}"
    
    return {
        "metric_name": "Average Dimension",
        "metric_value": metric_value,
        "instances_tested": len(dims),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")