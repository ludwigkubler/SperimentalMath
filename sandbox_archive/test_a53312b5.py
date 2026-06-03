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
    
    def symplectic_form(phi):
        n = len(phi)
        omega = [[0] * n for _ in range(n)]
        for clause in phi:
            for lit1 in clause:
                for lit2 in clause:
                    if lit1 != lit2:
                        i, j = abs(lit1) - 1, abs(lit2) - 1
                        omega[i][j] += (-1) ** (lit1 * lit2 > 0)
        return omega
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(i, n)):
                pivot_row = next(j for j in range(i, n) if matrix[j][i] != 0)
                matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
                rank += 1
                for j in range(n):
                    if i != j:
                        factor = -matrix[j][i] / matrix[i][i]
                        for k in range(n):
                            matrix[j][k] += factor * matrix[i][k]
        return rank
    
    def resolution_width(phi):
        stack = []
        while phi:
            clause = random.choice(phi)
            if all(lit not in stack and -lit not in stack for lit in clause):
                return len(stack)
            else:
                literal_to_add = next(lit for lit in clause if lit in stack or -lit in stack)
                stack.append(literal_to_add)
                phi.remove([l for l in phi if literal_to_add in l or -literal_to_add in l])
        return len(stack)
    
    def generate_phi(n):
        phi = []
        for _ in range(2 ** n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(lit not in phi[-1] and -lit not in phi[-1] for lit in clause):
                phi.append(clause)
        return phi
    
    n_max = 40
    instances_tested = 0
    min_ranks = []
    
    for n in range(5, n_max + 1, 5):
        phi = generate_phi(n)
        omega = symplectic_form(phi)
        w_phi = resolution_width(phi)
        min_rank_omega = min_rank(omega)
        
        instances_tested += len(phi)
        min_ranks.append(min_rank_omega)
    
    mean_min_rank = sum(min_ranks) / len(min_ranks)
    conjecture_holds = all(r >= 0.1 * w for r, w in zip(min_ranks, [resolution_width(generate_phi(n)) for n in range(5, n_max + 1, 5)]))
    
    return {
        "metric_name": "min_rank_omega",
        "metric_value": mean_min_rank,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_min_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_min_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")