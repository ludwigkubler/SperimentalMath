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
    
    def generate_protocol(n):
        # Generate a random n-communication protocol
        protocol = [random.randint(0, 1) for _ in range(n)]
        return protocol
    
    def calculate_lid(protocol):
        # Calculate the local induction dimension (LID) of the input space
        # This is a placeholder function; replace with actual LID calculation
        return len(set(protocol))
    
    def calculate_comm_rank_var(protocol):
        # Calculate the variance in communication complexity rank among all possible inputs with size n
        # This is a placeholder function; replace with actual CommRankVar calculation
        comm_rank = [sum(p) for p in protocol]
        mean_rank = sum(comm_rank) / len(comm_rank)
        var_rank = sum((x - mean_rank) ** 2 for x in comm_rank) / len(comm_rank)
        return var_rank
    
    def pearson_correlation(x, y):
        # Calculate the Pearson correlation coefficient
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_dev_x * std_dev_y)
    
    def gaussian_elimination(A):
        # Perform Gaussian elimination to solve a system of linear equations
        n = len(A)
        for i in range(n):
            max_row = i
            for k in range(i + 1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def matrix_multiplication(A, B):
        # Perform matrix multiplication
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        # Calculate the determinant of a matrix
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def inverse(A):
        # Calculate the inverse of a matrix
        n = len(A)
        I = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
        A_augmented = [row + col for row, col in zip(A, I)]
        A_rref = gaussian_elimination(A_augmented)
        inverse_A = [[A_rref[i][j] for j in range(n, 2 * n)] for i in range(n)]
        return inverse_A
    
    def solve_linear_system(A, b):
        # Solve a system of linear equations Ax = b
        A_b = [row + [b[i]] for i, row in enumerate(A)]
        A_rref = gaussian_elimination(A_b)
        n = len(A)
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = A_rref[i][n]
            for j in range(i + 1, n):
                x[i] -= A_rref[i][j] * x[j]
        return x
    
    def generate_random_matrix(n):
        # Generate a random n x n matrix
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def generate_random_vector(n):
        # Generate a random n-dimensional vector
        return [random.randint(0, 1) for _ in range(n)]
    
    def calculate_comm_rank(protocol):
        # Calculate the communication complexity rank of the protocol
        comm_rank = [sum(p) for p in protocol]
        return max(comm_rank)
    
    def calculate_comm_rank_var(protocol):
        # Calculate the variance in communication complexity rank among all possible inputs with size n
        comm_rank = [calculate_comm_rank(p) for p in protocol]
        mean_rank = sum(comm_rank) / len(comm_rank)
        var_rank = sum((x - mean_rank) ** 2 for x in comm_rank) / len(comm_rank)
        return var_rank
    
    def calculate_lid(protocol):
        # Calculate the local induction dimension (LID) of the input space
        lid = len(set(tuple(p) for p in protocol))
        return lid
    
    def run_protocol(n):
        protocol = generate_protocol(n)
        comm_rank_var = calculate_comm_rank_var(protocol)
        lid = calculate_lid(protocol)
        return lid, comm_rank_var
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        lid_sum = 0
        comm_rank_var_sum = 0
        instances_tested = 0
        
        for _ in range(5):
            lid, comm_rank_var = run_protocol(n)
            lid_sum += lid
            comm_rank_var_sum += comm_rank_var
            instances_tested += 1
        
        mean_lid = lid_sum / instances_tested
        mean_comm_rank_var = comm_rank_var_sum / instances_tested
        
        results.append({
            "n": n,
            "mean_lid": mean_lid,
            "mean_comm_rank_var": mean_comm_rank_var
        })
    
    correlation_coefficient = pearson_correlation([r["mean_lid"] for r in results], [r["mean_comm_rank_var"] for r in results])
    
    if correlation_coefficient < 0.8:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "Correlation coefficient is less than 0.8"
        }
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient is less than 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support_fraction")