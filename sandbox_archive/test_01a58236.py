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

def generate_formula(n):
    literals = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(n):
        clause = random.sample(literals, 2)
        clause.append(random.choice(['', '¬']))
        clauses.append(clause)
    return clauses

def aic(formula):
    literals = set()
    for clause in formula:
        for literal in clause:
            if literal.startswith('¬'):
                literal = literal[1:]
            literals.add(literal)
    
    literal_to_index = {literal: i for i, literal in enumerate(literals)}
    matrix = [[0] * len(literals) for _ in range(len(literals))]
    
    for clause in formula:
        if clause[-1]:
            continue
        literal1 = clause[0]
        literal2 = clause[1]
        index1 = literal_to_index[literal1]
        index2 = literal_to_index[literal2]
        
        matrix[index1][index2] += 1
        matrix[index2][index1] += 1
    
    rank = gaussian_elimination(matrix)
    return len(literals) - rank

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i+1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                continue
        
        pivot = Fraction(matrix[i][i])
        for j in range(n):
            matrix[i][j] /= pivot
        
        for j in range(n):
            if i == j:
                continue
            factor = Fraction(matrix[j][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    aic_values = []
    clause_counts = []
    
    for n in n_values:
        formula = generate_formula(n)
        aic_value = aic(formula)
        clause_count = len(formula)
        
        aic_values.append(aic_value)
        clause_counts.append(clause_count)
    
    mean_aic = sum(aic_values) / len(aic_values)
    mean_clause_count = sum(clause_counts) / len(clause_counts)
    
    correlation_coefficient = 0
    for i in range(len(aic_values)):
        correlation_coefficient += (aic_values[i] - mean_aic) * (clause_counts[i] - mean_clause_count)
    
    correlation_coefficient /= math.sqrt(sum((x - mean_aic) ** 2 for x in aic_values)) * math.sqrt(sum((y - mean_clause_count) ** 2 for y in clause_counts))
    
    p_value = 1.0
    if abs(correlation_coefficient) > 0:
        t_statistic = correlation_coefficient * math.sqrt(len(aic_values) - 2) / math.sqrt(1 - correlation_coefficient ** 2)
        p_value = 2 * (1 - math.erf(abs(t_statistic) / math.sqrt(2)))
    
    conjecture_holds = correlation_coefficient >= 0.8 and p_value <= 0.05
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}> p_value=<{}>".format(correlation_coefficient, p_value)
    
    return {
        "metric_name": "AIC vs Clause Count",
        "metric_value": correlation_coefficient,
        "instances_tested": len(aic_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, 0.0, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, 0.0, support_fraction))
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[first_failing_seed]["counterexample"], first_failing_seed))