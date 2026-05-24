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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def indicator_matrix(clauses, n):
        matrix = [[0] * (2 ** n) for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            for assignment in range(2 ** n):
                if all((assignment >> (var - 1)) & 1 == 1 for var in clause):
                    matrix[i][assignment] = 1
        return matrix
    
    def tropical_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[j][i] != 0 for j in range(i, m)):
                pivot_row = next(j for j in range(i, m) if matrix[j][i] != 0)
                matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
                rank += 1
                for j in range(m):
                    if i != j:
                        factor = -matrix[j][i] / matrix[i][i]
                        for k in range(n):
                            matrix[j][k] += factor * matrix[i][k]
        return rank
    
    def dpll_width(clauses, n):
        def backtrack(assignment, clause_index):
            if clause_index == len(clauses):
                return 1
            var = next(var for var in range(1, n + 1) if var not in assignment)
            assignment[var] = 0
            if any((assignment >> (v - 1)) & 1 == 1 for v in clauses[clause_index]):
                return backtrack(assignment, clause_index + 1)
            assignment[var] = 1
            if all((assignment >> (v - 1)) & 1 == 1 for v in clauses[clause_index]):
                return backtrack(assignment, clause_index + 1)
            return 0
        
        assignment = [None] * (n + 1)
        return backtrack(assignment, 0)
    
    def spearman_correlation(ranks1, ranks2):
        n = len(ranks1)
        sorted_ranks1 = sorted(range(n), key=lambda i: ranks1[i])
        sorted_ranks2 = sorted(range(n), key=lambda i: ranks2[i])
        rho_numerator = sum((sorted_ranks1[i] - sorted_ranks2[i]) ** 2 for i in range(n))
        rho_denominator = n * (n**2 - 1)
        return 1 - (6 * rho_numerator) / rho_denominator
    
    def mean_ratio(ranks1, ranks2):
        return sum(rank1 / rank2 for rank1, rank2 in zip(ranks1, ranks2)) / len(ranks1)
    
    n_values = [10, 15, 20, 30, 40]
    m_values = [int(0.5 * n) for n in n_values]
    results = []
    
    for n, m in zip(n_values, m_values):
        cnf = generate_cnf(n, m)
        indicator_mat = indicator_matrix(cnf, n)
        rank = tropical_rank(indicator_mat)
        width = dpll_width(cnf, n)
        results.append((rank, width))
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman's Rank Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    ranks1, ranks2 = zip(*results)
    rho = spearman_correlation(ranks1, ranks2)
    mean_ratio_val = mean_ratio(ranks1, ranks2)
    
    return {
        "metric_name": "Spearman's Rank Correlation",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": rho >= 0.8 and mean_ratio_val <= 1.2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman's rank correlation < 0.8 or mean ratio > 1.2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")