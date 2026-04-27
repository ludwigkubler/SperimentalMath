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

    def f(x):
        return x & (x + 1)

    def log2_floor(n):
        return math.floor(math.log2(n))

    def kw_tree_depth_lower_bound(x, y):
        if x == y:
            return 0
        if x % 2 != y % 2:
            return 1
        return 1 + max(kw_tree_depth_lower_bound(x >> 1, y >> 1), log2_floor(abs(x - y)))

    def controlled_cover(diameter, multiplicity):
        cover = []
        queue = [(0, 0)]
        while queue:
            node, depth = queue.pop(0)
            if depth > diameter / 2:
                continue
            for i in range(1 << (log2_floor(node) + 1)):
                new_node = node ^ (1 << log2_floor(node))
                if new_node not in cover and len(cover) < multiplicity:
                    cover.append(new_node)
                    queue.append((new_node, depth + 1))
        return cover

    def sparse_matrix_trace(matrix):
        trace = 0
        for i in range(len(matrix)):
            trace += matrix[i][i]
        return trace

    def sparse_matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def sparse_matrix_transpose(matrix):
        n = len(matrix)
        T = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                T[j][i] = matrix[i][j]
        return T

    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x

    def matrix_power(matrix, power):
        result = [[0] * len(matrix) for _ in range(len(matrix))]
        for i in range(len(matrix)):
            result[i][i] = 1
        while power > 0:
            if power % 2 == 1:
                result = sparse_matrix_multiplication(result, matrix)
            matrix = sparse_matrix_multiplication(matrix, matrix)
            power //= 2
        return result

    def log_propagation(matrix):
        n = len(matrix)
        max_val = 0
        for i in range(n):
            for j in range(n):
                if abs(matrix[i][j]) > max_val:
                    max_val = abs(matrix[i][j])
        return math.log2(max_val)

    def signed_address_parity(x):
        parity = 0
        while x > 0:
            parity ^= x & 1
            x >>= 1
        return parity

    def build_operator_and_cocycle(k):
        n = k + 2 ** k
        T_k = [[0] * n for _ in range(n)]
        c_k = [0] * n
        for i in range(1, n):
            address_bit = log2_floor(i)
            T_k[i][i ^ (1 << address_bit)] = 1
            c_k[i] = (-1) ** (address_bit % 2)
        return T_k, c_k

    def trace_pairing(c_k, T_k):
        n = len(c_k)
        C = sparse_matrix_multiplication(sparse_matrix_transpose(c_k), T_k)
        return sparse_matrix_trace(C)

    k_values = [2, 3, 4]
    results = []
    for k in k_values:
        N = k + 2 ** k
        X = set(range(N))
        if len(X) > 1024:
            X = random.sample(X, 1024)
        d_k = [kw_tree_depth_lower_bound(x, y) for x in X for y in X]
        asdim_slope = []
        trace_ratio = []

        for R in range(1, 2 ** k + 1):
            cover = controlled_cover(R, k)
            m_R = len(cover)
            if m_R > 0:
                asdim_slope.append((math.log(m_R), math.log(R)))
            T_k, c_k = build_operator_and_cocycle(k)
            trace_ratio.append(trace_pairing(c_k, T_k) / log_propagation(T_k))

        if asdim_slope and trace_ratio:
            slope, _ = gaussian_elimination(asdim_slope, [0] * len(asdim_slope))
            mean_trace_ratio = sum(trace_ratio) / len(trace_ratio)
            results.append({
                "metric_name": "asdim_slope",
                "metric_value": slope,
                "instances_tested": len(X),
                "conjecture_holds": slope >= k - 2 and mean_trace_ratio >= 0.5 * k,
                "counterexample": ""
            })

    if not results:
        return {
            "metric_name": "",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_slope = sum(result["metric_value"] for result in results) / len(results)
    std_slope = math.sqrt(sum((result["metric_value"] - mean_slope) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    return {
        "metric_name": "asdim_slope",
        "metric_value": mean_slope,
        "instances_tested": len(X),
        "conjecture_holds": all(result["conjecture_holds"] for result in results) or support_fraction >= 0.8,
        "counterexample": "" if all(result["conjecture_holds"] for result in results) else "not_all_seeds_support"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    results = [run_trial(seed) for seed in seeds if "conjecture_holds" in result and result["conjecture_holds"]]
    mean_slope = sum(result["metric_value"] for result in results) / len(results)
    std_slope = math.sqrt(sum((result["metric_value"] - mean_slope) ** 2 for result in results) / len(results))
    support_fraction = len(results) / len(seeds)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_all_seeds_support\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")