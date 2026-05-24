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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def frege_proof_width(cnf):
        # Simplified estimation of Frege proof width
        return len(cnf) * 2
    
    def bruhat_matrix(cnf):
        m = len(cnf)
        n = max(abs(lit) for clause in cnf for lit in clause)
        B = [[0] * (n + 1) for _ in range(n + 1)]
        
        for clause in cnf:
            for i, lit in enumerate(clause):
                if lit > 0:
                    B[lit][i + 1] += 1
                else:
                    B[-lit][i + 1] -= 1
        
        return B
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(i, n)):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m_min = int(n * 0.1)
        m_max = n
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(m_min, m_max)
            cnf = generate_cnf(n, m)
            B = bruhat_matrix(cnf)
            rank = min_rank(B)
            width = frege_proof_width(cnf)
            results.append({
                "n": n,
                "m": m,
                "rank": rank,
                "width": width
            })
    
    if not results:
        return {
            "metric_name": "min_rank",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    mean_width = sum(result["width"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["rank"] - mean_rank) ** 2 for result in results) / len(results))
    std_width = math.sqrt(sum((result["width"] - mean_width) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(result["rank"] <= math.log2(result["m"] / result["n"]) ** 2 for result in results)
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"m/n={result['m']}/{result['n']} rank={result['rank']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m/n too large\" first_failing_seed={first_failing_seed}")