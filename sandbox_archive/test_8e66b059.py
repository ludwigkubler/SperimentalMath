# auto-injected by SEC sandbox
import collections
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
import json
from itertools import combinations

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def det(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        det_val = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det_val += (-1) ** j * A[0][j] * det(submatrix)
        return det_val

def norm(A):
    return math.sqrt(sum(x**2 for row in A for x in row))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_matrix(n, type_):
        if type_ == "bernoulli":
            return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        elif type_ == "hadamard":
            H = [[1]]
            for i in range(1, n):
                H.append([1] + [-h if j % 2 != (i+1) % 2 else h for j, h in enumerate(H[i-1])])
                for j in range(i):
                    H[j].append(H[j][i])
            return H
        elif type_ == "circulant":
            first_row = [random.choice([-1, 1]) for _ in range(n)]
            return [[first_row[(j-i) % n] for j in range(n)] for i in range(n)]
        elif type_ == "toeplitz":
            first_row = [random.choice([-1, 1]) for _ in range(n)]
            first_col = [random.choice([-1, 1]) for _ in range(n)]
            return [[first_col[i] if j == 0 else first_row[j-i] if i == 0 else first_col[i] * first_row[j-i] for j in range(n)] for i in range(n)]
        elif type_ == "adversarial":
            M = generate_matrix(n, "bernoulli")
            rank = random.randint(1, n//2)
            U = generate_matrix(rank, "circulant")
            V = generate_matrix(rank, "toeplitz")
            return [[sum(U[i][k] * V[k][j] for k in range(rank)) + random.choice([-1, 1]) for j in range(n)] for i in range(n)]
        else:
            raise ValueError("Unknown matrix type")

    def subdeterminant_dispersion(M):
        n = len(M)
        max_disp = 0
        for k in range(2, min(n, 7)):
            for S in combinations(range(n), k):
                for T in combinations(range(n), k):
                    submatrix = [[M[i][j] for j in T] for i in S]
                    det_val = abs(det(gaussian_elimination(submatrix)))
                    max_disp = max(max_disp, det_val**(1/k) / math.sqrt(k))
        return max_disp

    def energy_tail_rank(M):
        _, s, _ = map(list, zip(*sorted(zip(*gaussian_elimination([[x**2 for x in row] for row in M])))))
        norm_M = norm(M)
        return sum(1 for sigma_i in s if sigma_i**2 >= norm_M**2 / len(s))

    n_values = [6, 8, 10, 12, 14, 16, 20]
    results = []
    
    for n in n_values:
        for _ in range(30):
            M = generate_matrix(n, random.choice(["bernoulli", "hadamard", "circulant", "toeplitz", "adversarial"]))
            delta = subdeterminant_dispersion(M)
            tau = energy_tail_rank(M)
            results.append((n, tau * delta**2 / n))
    
    min_ratio = min(results, key=lambda x: x[1])[1]
    support_fraction = sum(1 for _, ratio in results if ratio >= 0.25) / len(results)
    median_ratios = sorted([ratio for _, ratio in results])
    spearman_rho = -sum((i - (len(median_ratios) + 1) / 2) * (j - (len(median_ratios) + 1) / 2) for i, j in enumerate(median_ratios)) / sum((i - (len(median_ratios) + 1) / 2)**2 for i in range(len(median_ratios)))
    
    return {
        "metric_name": "R(M)",
        "metric_value": min_ratio,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8 and spearman_rho > -0.5,
        "counterexample": "" if support_fraction >= 0.8 else f"support_fraction={support_fraction}, median_R={median_ratios[len(median_ratios)//2]}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
    
    results = [run_trial(seed) for seed in seeds]
    min_ratio = min(results, key=lambda x: x["metric_value"])["metric_value"]
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    median_ratios = sorted([res["metric_value"] for res in results])
    spearman_rho = -sum((i - (len(median_ratios) + 1) / 2) * (j - (len(median_ratios) + 1) / 2) for i, j in enumerate(median_ratios)) / sum((i - (len(median_ratios) + 1) / 2)**2 for i in range(len(median_ratios)))
    
    if support_fraction >= 0.8 and spearman_rho > -0.5:
        print(f"RESULT: SUPPORTED mean={min_ratio} std=0 support_fraction={support_fraction}")
    elif any(res["metric_value"] < 0.25 for res in results):
        first_failing_seed = next(i for i, res in enumerate(results) if res["metric_value"] < 0.25)
        print(f"RESULT: FALSIFIED counterexample=\"median_R too small\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}, median_R={median_ratios[len(median_ratios)//2]}")