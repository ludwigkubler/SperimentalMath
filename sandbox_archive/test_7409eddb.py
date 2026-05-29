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
    
    def algebra_generated_by_cnf(cnf):
        variables = set()
        for clause in cnf:
            for lit in clause:
                variables.add(abs(lit))
        algebras = {var: [0] * (2**len(variables)) for var in variables}
        for clause in cnf:
            mask = 0
            for lit in clause:
                mask |= 1 << (lit - 1)
            for var, coeffs in algebras.items():
                new_coeffs = []
                for coeff in coeffs:
                    new_coeff = 0
                    for i in range(len(variables)):
                        if (mask & (1 << i)) != 0:
                            new_coeff += coeff * (-1) ** (lit < 0)
                        else:
                            new_coeff += coeff
                    new_coeffs.append(new_coeff)
                algebras[var] = new_coeffs
        return algebras
    
    def tensor_product(algebra_A, algebra_B):
        keys_A = list(algebra_A.keys())
        keys_B = list(algebra_B.keys())
        result = {}
        for key_A in keys_A:
            for key_B in keys_B:
                result[(key_A, key_B)] = [0] * (len(keys_A) * len(keys_B))
                for i in range(len(keys_A)):
                    for j in range(len(keys_B)):
                        result[(key_A, key_B)][i * len(keys_B) + j] = algebra_A[keys_A[i]][j]
        return result
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m == 0 or n == 0:
            return 0
        matrix = [row[:] for row in matrix]
        pivot_row = 0
        for i in range(n):
            if pivot_row >= m:
                break
            max_row = pivot_row
            for j in range(pivot_row + 1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[pivot_row], matrix[max_row] = matrix[max_row], matrix[pivot_row]
            if matrix[pivot_row][i] == 0:
                continue
            for j in range(n):
                matrix[pivot_row][j] /= matrix[pivot_row][i]
            for j in range(m):
                if j != pivot_row:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[pivot_row][k]
            pivot_row += 1
        return pivot_row
    
    def frege_proof_depth(cnf):
        # Simplified heuristic to estimate Frege proof depth
        m = len(cnf)
        n = max(abs(lit) for clause in cnf for lit in clause)
        return int(math.log2(m * n))
    
    results = []
    for n in [5, 10, 20, 40]:
        for _ in range(30):
            m = random.randint(1, n**2)
            cnf = generate_cnf(n, m)
            algebra_A = algebra_generated_by_cnf(cnf)
            algebra_B = algebra_generated_by_cnf([[var] for var in range(1, n+1)])
            tensor_prod = tensor_product(algebra_A, algebra_B)
            rank_value = rank(tensor_prod)
            depth = frege_proof_depth(cnf)
            results.append((rank_value, depth))
    
    if len(results) == 0:
        return {
            "metric_name": "Spearman's Rank Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No data generated"
        }
    
    rank_values = [r[0] for r in results]
    depths = [r[1] for r in results]
    
    def spearman_rank_correlation(ranks, values):
        n = len(ranks)
        if n == 0:
            return None
        ranks_dict = {rank: i for i, rank in enumerate(sorted(set(ranks)), start=1)}
        sorted_ranks = [ranks_dict[rank] for rank in ranks]
        sorted_values = sorted(values)
        n_pairs = sum((sorted_ranks[i] - sorted_ranks[j]) * (sorted_values[i] - sorted_values[j])
                      for i in range(n) for j in range(i + 1, n)) / 2
        rho_numerator = n_pairs
        rho_denominator = n * (n**2 - 1) / 6
        return 1 - (6 * rho_numerator) / rho_denominator
    
    correlation_coefficient = spearman_rank_correlation(rank_values, depths)
    
    return {
        "metric_name": "Spearman's Rank Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 32))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_rank_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    total_instances = sum(r["instances_tested"] for r in results if r["instances_tested"] > 0)
    
    if len(total_rank_values) == 0:
        print("RESULT: INCONCLUSIVE No data generated")
    else:
        mean_value = sum(total_rank_values) / len(total_rank_values)
        std_value = math.sqrt(sum((x - mean_value)**2 for x in total_rank_values) / len(total_rank_values))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")