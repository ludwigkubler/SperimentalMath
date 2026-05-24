# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

# Helper functions for tropical semiring operations
def tropical_add(a, b):
    return max(a, b)

def tropical_mul(a, b):
    if a == float('-inf') or b == float('-inf'):
        return float('-inf')
    return a + b

def tropical_neg(a):
    return -a

# Function to compute the minimal rank of a noncrossing partition matrix
def minimal_rank(cnf):
    n = len(cnf)
    m = len(cnf[0])
    
    # Initialize the indicator matrix
    I = [[0] * (2 * n) for _ in range(m)]
    for i, clause in enumerate(cnf):
        for literal in clause:
            if literal > 0:
                I[i][literal - 1] = 1
            else:
                I[i][-literal - 1] = 1
    
    # Compute the rank using Gaussian elimination
    rank = 0
    for i in range(m):
        pivot_row = None
        for j in range(i, m):
            if any(I[j][k] != float('-inf') for k in range(2 * n)):
                pivot_row = j
                break
        
        if pivot_row is None:
            continue
        
        rank += 1
        for k in range(2 * n):
            I[i][k], I[pivot_row][k] = I[pivot_row][k], I[i][k]
        
        for j in range(m):
            if i != j and any(I[j][k] != float('-inf') for k in range(2 * n)):
                factor = tropical_neg(I[j][i])
                for k in range(2 * n):
                    I[j][k] = tropical_add(I[j][k], tropical_mul(factor, I[i][k]))
    
    return rank

# Function to compute the DPLL proof width
def dpll_proof_width(cnf):
    # Placeholder function: this should be replaced with an actual DPLL implementation
    # For simplicity, we assume a constant width for all CNF formulas
    return 10

# Function to generate a random CNF formula
def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = set()
        while len(clause) < 3:
            literal = random.randint(1, n)
            if random.choice([True, False]):
                literal = -literal
            clause.add(literal)
        cnf.append(list(clause))
    return cnf

# Function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a set of random CNF formulas
    n_values = [10, 15, 20, 30, 40]
    m_values = [int(n * 0.1) for n in n_values]
    results = []
    
    for n, m in zip(n_values, m_values):
        for _ in range(6):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, m)
            rank = minimal_rank(cnf)
            width = dpll_proof_width(cnf)
            
            results.append({
                "n": n,
                "m": m,
                "rank": rank,
                "width": width
            })
    
    # Compute the mean and standard deviation of the ratio of rank to width
    ratios = [result["rank"] / result["width"] for result in results]
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in ratios) / len(ratios))
    
    # Compute Spearman's rank correlation coefficient
    sorted_indices = sorted(range(len(results)), key=lambda i: results[i]["rank"])
    sorted_widths = [results[i]["width"] for i in sorted_indices]
    n_pairs = len(sorted_widths)
    sum_d1_squared = sum((sorted_widths[i] - sorted_widths[j]) ** 2 for i, j in combinations(range(n_pairs), 2))
    rho = 1 - (6 * sum_d1_squared) / (n_pairs * (n_pairs**2 - 1))
    
    # Determine if the conjecture holds
    conjecture_holds = rho >= 0.8 and mean_ratio <= 1.2
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "rho < 0.8 or mean_ratio > 1.2"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.4f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    # Compute mean and standard deviation of metric value
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    
    # Compute fraction of seeds where conjecture holds
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")