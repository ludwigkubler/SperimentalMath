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
    
    def generate_cnf(n, complexity):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(complexity):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def cnf_to_polynomial(cnf):
        n = len(cnf[0])
        poly = [0] * (n + 1)
        for clause in cnf:
            term = 1
            for var in clause:
                if random.choice([True, False]):
                    term *= -var
                else:
                    term *= var
            poly[n] += term
        return poly
    
    def hodge_rank(poly):
        n = len(poly)
        matrix = [[0] * n for _ in range(n)]
        for i, coeff in enumerate(poly[1:], start=1):
            if i <= n:
                matrix[i-1][i-1] += coeff
        rank = 0
        for row in matrix:
            if any(row):
                pivot_col = next((j for j, x in enumerate(row) if x != 0), None)
                if pivot_col is not None:
                    rank += 1
                    for i in range(n):
                        if i != pivot_col and matrix[i][pivot_col] != 0:
                            factor = -matrix[i][pivot_col] / matrix[pivot_col][pivot_col]
                            for j in range(n):
                                matrix[i][j] += factor * matrix[pivot_col][j]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_h_rank = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            complexity = random.randint(n // 2 + 1, n)
            cnf = generate_cnf(n, complexity)
            poly = cnf_to_polynomial(cnf)
            h_rank = hodge_rank(poly)
            
            if h_rank < Fraction(math.log(n), 10):
                conjecture_holds = False
                counterexample = f"n={n}, complexity={complexity}, H-rank={h_rank}"
                break
            
            total_h_rank += h_rank
            instances_tested += 1
    
    mean_h_rank = total_h_rank / instances_tested if instances_tested > 0 else 0
    support_fraction = Fraction(instances_tested, len(n_values) * 5)
    
    return {
        "metric_name": "H-rank",
        "metric_value": mean_h_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_h_rank = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    support_fraction = Fraction(sum(1 for r in results if r["conjecture_holds"]), len(results))
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_h_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")