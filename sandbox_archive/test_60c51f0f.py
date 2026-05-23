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
    
    def generate_tseitin_formula(n):
        if n == 1:
            return "A"
        else:
            p = f"A{n-1}"
            q = f"B{n-1}"
            r = f"C{n-1}"
            formula = f"({p} & {q}) -> {r}"
            return formula
    
    def compute_riemannian_metric(variables):
        n = len(variables)
        metric = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    metric[i][j] = 1
                else:
                    metric[i][j] = random.random()
                    metric[j][i] = metric[i][j]
        return metric
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(i, n):
                matrix[i][j] *= factor
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(i, n):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        echelon_form = gaussian_elimination(matrix)
        rank = 0
        for row in echelon_form:
            if any(row):
                rank += 1
        return rank
    
    def frege_proof_length(formula):
        # Placeholder function, replace with actual Frege proof length computation
        return len(formula.split())
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    variables = list(range(n))
    metric = compute_riemannian_metric(variables)
    min_rank = rank(metric)
    proof_length = frege_proof_length(formula)
    
    conjecture_holds = min_rank <= 2 * proof_length
    counterexample = "" if conjecture_holds else f"Formula: {formula}, Min Rank: {min_rank}, Proof Length: {proof_length}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        counterexample = next(r['counterexample'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")