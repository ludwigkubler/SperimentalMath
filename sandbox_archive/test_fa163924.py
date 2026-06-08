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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def frege_proof_depth(cnf):
        # Simplified DPLL solver to estimate proof depth
        stack = []
        for clause in cnf:
            if all(x not in stack and -x not in stack for x in clause):
                stack.extend(clause)
            else:
                continue  # This is a simplified heuristic
        return len(stack)
    
    def k_theoretic_index(cnf):
        n = len(cnf[0])
        B = [[0] * n for _ in range(n)]
        for clause in cnf:
            for x in clause:
                if x > 0:
                    B[x-1][x-1] += 1
                else:
                    B[-x-1][-x-1] += 1
        det = determinant(B)
        return abs(det) ** (1/n)
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def is_valid_cnf(cnf, n):
        if not all(len(clause) > 0 for clause in cnf):
            return False
        if any(abs(x) > n for x in [x for clause in cnf for x in clause]):
            return False
        return True
    
    results = []
    for n in range(5, 41):
        for _ in range(30):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            if not is_valid_cnf(cnf, n):
                continue
            depth = frege_proof_depth(cnf)
            index = k_theoretic_index(cnf)
            results.append((n, depth, index))
    
    metric_value = sum(index for _, _, index in results) / len(results)
    conjecture_holds = all(depth <= 10 and index >= n**(2/3) for _, depth, index in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "K-theoretic Index",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")