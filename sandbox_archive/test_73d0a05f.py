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
    
    def generate_ptf(n, m):
        clauses = []
        for _ in range(m):
            variables = random.sample(range(1, n+1), 2)
            polarity = [random.choice([True, False]) for _ in range(2)]
            clause = [(variables[i], polarity[i]) for i in range(2)]
            clauses.append(clause)
        return clauses
    
    def minimal_rank(ptf):
        m = len(ptf)
        n = max(max(abs(var) for var, _ in clause) for clause in ptf)
        
        # Create the incidence matrix
        A = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(ptf):
            for var, polarity in clause:
                if polarity:
                    A[i][var] = 1
                else:
                    A[i][var] = -1
        
        # Gaussian elimination to find the rank of the matrix
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            
            for j in range(cols):
                pivot_row = None
                for i in range(rank, rows):
                    if matrix[i][j] != 0:
                        pivot_row = i
                        break
                
                if pivot_row is not None:
                    matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                    rank += 1
                    
                    for i in range(rows):
                        if i != rank - 1:
                            factor = Fraction(matrix[i][j], matrix[rank-1][j])
                            for k in range(cols):
                                matrix[i][k] -= factor * matrix[rank-1][k]
            
            return rank
        
        return gaussian_elimination(A)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        m = random.randint(1, 10 * n)  # Ensure enough clauses
        ptf = generate_ptf(n, m)
        rank = minimal_rank(ptf)
        predicted_value = Fraction(m**(1/4) * n**(3/4)).limit_denominator()
        ratio = Fraction(rank, predicted_value).limit_denominator()
        results.append({"n": n, "m": m, "rank": rank, "predicted_value": predicted_value, "ratio": ratio})
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["ratio"] - mean_ratio)**2 for result in results) / len(results))
    
    conjecture_holds = all(0.5 <= result["ratio"] <= 2.5 for result in results)
    counterexample = "" if conjecture_holds else "n={}, m={}, rank={}, predicted_value={}".format(
        n_values[results.index(max(results, key=lambda x: abs(x["ratio"] - 1)))],
        results[max(results, key=lambda x: abs(x["ratio"] - 1))]["m"],
        results[max(results, key=lambda x: abs(x["ratio"] - 1))]["rank"],
        results[max(results, key=lambda x: abs(x["ratio"] - 1))]["predicted_value"]
    )
    
    return {
        "metric_name": "Ratio of Minimal Rank to Predicted Value",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL: {" + ", ".join(f"'{k}': {v}" for k, v in trial_result.items()) + "}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")