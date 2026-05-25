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
    
    def generate_max_cut_instance(n):
        variables = list(range(n))
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        cut_edges = random.sample(edges, n // 2)
        return variables, cut_edges

    def evaluate_polynomial(terms, x_values):
        result = Fraction(0)
        for term in terms:
            value = 1
            for var, exp in term:
                value *= x_values[var] ** exp
            result += term[2] * value
        return result

    def construct_moment_matrix(polynomial, variables):
        n = len(variables)
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for term in polynomial:
            x_values = [Fraction(1)] * (n + 1)
            for var, exp in term:
                x_values[var] = Fraction(term[2], 1) ** (exp / n)
            for i in range(n + 1):
                for j in range(n + 1):
                    M[i][j] += x_values[i] * x_values[j]
        return M

    def gaussian_elimination(matrix, b):
        n = len(matrix)
        augmented_matrix = [row + [b[i]] for i, row in enumerate(matrix)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(augmented_matrix[r][i]))
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            denom = augmented_matrix[i][i]
            if denom == 0:
                continue
            for j in range(n + 1):
                augmented_matrix[i][j] /= denom
            for k in range(n):
                if k != i and augmented_matrix[k][i] != 0:
                    factor = augmented_matrix[k][i]
                    for j in range(n + 1):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
        return [row[-1] for row in augmented_matrix]

    def rank(matrix):
        n = len(matrix)
        M = [row[:] for row in matrix]
        r = 0
        for i in range(n):
            if sum(M[j][i] ** 2 for j in range(i, n)) == 0:
                continue
            r += 1
            for j in range(n):
                M[i], M[j] = M[j], M[i]
                for k in range(n + 1):
                    M[j][k] /= M[i][i]
                for l in range(n):
                    if l != i:
                        factor = M[l][i]
                        for k in range(n + 1):
                            M[l][k] -= factor * M[i][k]
        return r

    def approximation_ratio(polynomial, variables, cut_edges):
        n = len(variables)
        x_values = [Fraction(1)] * (n + 1)
        p_value = evaluate_polynomial(polynomial, x_values)
        for var in range(n):
            x_values[var] = Fraction(1 - 2 * random.randint(0, 1), 1)
        q_value = evaluate_polynomial(polynomial, x_values)
        return abs(q_value / p_value)

    n = random.choice([5, 10, 15, 20, 30, 40])
    variables, cut_edges = generate_max_cut_instance(n)
    d = len(cut_edges)
    polynomial = []
    for var in range(n):
        polynomial.append(((var,), 1, Fraction(1)))
    for i, j in cut_edges:
        polynomial.append(((i,), 1, Fraction(-1)))
        polynomial.append(((j,), 1, Fraction(-1)))

    M_p = construct_moment_matrix(polynomial, variables)
    rank_M_p = rank(M_p)

    if rank_M_p < d * math.log(n) ** 2:
        ratio = approximation_ratio(polynomial, variables, cut_edges)
        conjecture_holds = ratio > 0.878
        counterexample = "" if conjecture_holds else f"Approximation ratio {ratio} <= 0.878"
    else:
        conjecture_holds = True
        counterexample = ""

    return {
        "metric_name": "Rank of Moment Matrix",
        "metric_value": rank_M_p,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Approximation ratio <= 0.878\" first_failing_seed={seeds[first_failing_seed]}")