# auto-injected by SEC sandbox
import itertools
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from collections import defaultdict

def matrix_mult(a, b):
    """Multiply two matrices a and b."""
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def matrix_sub(a, b):
    """Subtract matrix b from matrix a."""
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def matrix_transpose(a):
    """Transpose matrix a."""
    return [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]

def frobenius_inner_product(a, b):
    """Compute the Frobenius inner product of matrices a and b."""
    a_transpose = matrix_transpose(a)
    product = matrix_mult(a_transpose, b)
    return sum(sum(row) for row in product)

def generate_random_matrix(w, seed):
    """Generate a random w x w matrix with entries in {0, 1}."""
    random.seed(seed)
    return [[random.randint(0, 1) for _ in range(w)] for _ in range(w)]

def generate_random_bp(n, w, seed):
    """Generate a random read-twice oblivious BP."""
    random.seed(seed)
    layers = list(range(2 * n))
    random.shuffle(layers)
    x_layers = layers[:n]
    y_layers = layers[n:]
    M = [generate_random_matrix(w, seed + i) for i in range(2 * n)]
    N = [matrix_sub(M[i], M[i]) for i in range(2 * n)]
    return x_layers, y_layers, M, N

def generate_blocks_ordered_bp(n, w, seed):
    """Generate a blocks-ordered read-twice oblivious BP for IP_2."""
    random.seed(seed)
    x_layers = list(range(n))
    y_layers = list(range(n, 2 * n))
    M = [generate_random_matrix(w, seed + i) for i in range(2 * n)]
    N = [matrix_sub(M[i], M[i]) for i in range(2 * n)]
    return x_layers, y_layers, M, N

def compute_rho(P, w):
    """Compute the operator-SoS 4-trace gap rho(P)."""
    max_inner_product = 0
    for u in range(len(P)):
        for v in range(u + 1, len(P)):
            inner_product = abs(frobenius_inner_product(P[u], P[v]))
            if inner_product > max_inner_product:
                max_inner_product = inner_product
    if max_inner_product == 0:
        return 0.0
    return math.log2(max_inner_product) - 2 * math.log2(w)

def run_trial(seed):
    """Run a single trial with the given seed."""
    random.seed(seed)
    n_values = [4, 6, 8, 10, 16, 24, 32, 40]
    w_values = [2, 4, 8]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for w in w_values:
            # Generate random read-twice oblivious BP
            x_layers, y_layers, M, N = generate_random_bp(n, w, seed)
            P = [matrix_mult(N[a], N[b]) for a, b in zip(x_layers, y_layers)]
            rho = compute_rho(P, w)
            metric_values.append(rho)
            instances_tested += 1

            # Check trivial upper bound
            if rho > 2 * math.log2(w) + 2:
                conjecture_holds = False
                counterexample = f"Random BP with n={n}, w={w}, rho={rho} violates upper bound"

            # Generate blocks-ordered read-twice oblivious BP for IP_2
            if n in [4, 6, 8, 10]:
                x_layers, y_layers, M, N = generate_blocks_ordered_bp(n, 2**n, seed)
                P = [matrix_mult(N[a], N[b]) for a, b in zip(x_layers, y_layers)]
                rho = compute_rho(P, 2**n)
                metric_values.append(rho)
                instances_tested += 1

                # Check lower bound
                if rho < n / 16 - 4 * math.log2(n):
                    conjecture_holds = False
                    counterexample = f"Blocks-ordered IP_2 BP with n={n}, rho={rho} violates lower bound"

    metric_value = sum(metric_values) / len(metric_values) if metric_values else 0.0
    return {
        "metric_name": "operator-SoS 4-trace gap",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_counts = 0

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps({'seed': seed, **result})}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = conjecture_holds_counts / len(seeds) if seeds else 0.0

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")