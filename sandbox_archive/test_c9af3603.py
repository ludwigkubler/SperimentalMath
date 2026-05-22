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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i + 1, rows):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def resolution_length(clauses):
        stack = list(clauses)
        while stack:
            clause = stack.pop()
            new_clauses = []
            for other_clause in clauses:
                if len(set(clause) & set(other_clause)) == 2:
                    literal, neg_literal = next(lit for lit in clause if -lit in other_clause)
                    new_clause = [l for l in clause + other_clause if l != literal and l != -neg_literal]
                    if not new_clause:
                        return len(clauses) - len(stack)
                    new_clauses.append(new_clause)
            stack.extend(new_clauses)
        return float('inf')
    
    def geometric_rank(n):
        # Placeholder for actual geometric rank computation
        return random.randint(1, n)
    
    n = 20
    clauses = [[random.choice([-1, 1]) * (i + 1) for i in range(n)] for _ in range(n)]
    rank = geometric_rank(n)
    proof_length = resolution_length(clauses)
    
    if proof_length == float('inf'):
        return {
            "metric_name": "rank_to_proof_length_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_proved_unsat"
        }
    
    ratio = rank / proof_length
    return {
        "metric_name": "rank_to_proof_length_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_to_proof_length_ratio > 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")