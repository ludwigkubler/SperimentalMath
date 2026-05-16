# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def hamming_distance(x, y):
    return sum(1 for a, b in zip(x, y) if a != b)

def vietoris_rips_complex(points, max_distance):
    n = len(points)
    edges = []
    for i, j in itertools.combinations(range(n), 2):
        d = hamming_distance(points[i], points[j])
        if d <= max_distance:
            edges.append((i, j))
    return edges

def compute_boundary_matrix(edges, n):
    boundary_matrix = defaultdict(list)
    for i, (u, v) in enumerate(edges):
        boundary_matrix[i] = [u, v]
    return boundary_matrix

def reduce_boundary_matrix(boundary_matrix):
    pivots = {}
    for col in sorted(boundary_matrix.keys()):
        row = boundary_matrix[col]
        for pivot_col, pivot_row in pivots.items():
            if row == pivot_row:
                del boundary_matrix[col]
                break
        else:
            pivots[col] = row
    return pivots

def compute_persistence_diagram(boundary_matrix, max_distance):
    pivots = reduce_boundary_matrix(boundary_matrix)
    diagram = []
    for col, row in pivots.items():
        if len(row) == 2:
            u, v = row
            birth = min(hamming_distance(u, v) for u, v in itertools.combinations(row, 2))
            death = max_distance
            diagram.append((birth, death))
    return diagram

def compute_total_persistence(diagram):
    return sum(death - birth for birth, death in diagram)

def generate_matrix(matrix_type, n):
    N = 2 ** n
    if matrix_type == 'DISJ':
        matrix = [[0] * N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                matrix[i][j] = (i & j) != 0
    elif matrix_type == 'IP':
        matrix = [[0] * N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                matrix[i][j] = bin(i & j).count('1') % 2
    elif matrix_type == 'EQ':
        matrix = [[0] * N for _ in range(N)]
        for i in range(N):
            matrix[i][i] = 1
    else:
        matrix = [[random.choice([-1, 1]) for _ in range(N)] for _ in range(N)]
    return matrix

def run_trial(seed):
    random.seed(seed)
    n_values = [4, 5, 6]
    matrix_types = ['DISJ', 'IP', 'EQ', 'RAND']
    results = []

    for n in n_values:
        N = 2 ** n
        k = math.ceil(math.sqrt(N))
        for matrix_type in matrix_types:
            matrix = generate_matrix(matrix_type, n)
            total_persistence = 0
            instances_tested = 0

            for _ in range(30):
                if instances_tested >= 30:
                    break
                S = random.sample(range(N), k)
                subcloud = [matrix[x] for x in S]
                max_distance = sorted(hamming_distance(subcloud[i], subcloud[j]) for i, j in itertools.combinations(range(k), 2))[int(0.75 * len(subcloud) * (len(subcloud) - 1) / 2)]
                edges = vietoris_rips_complex(subcloud, max_distance)
                boundary_matrix = compute_boundary_matrix(edges, k)
                diagram = compute_persistence_diagram(boundary_matrix, max_distance)
                total_persistence += compute_total_persistence(diagram)
                instances_tested += 1

            avg_persistence = total_persistence / instances_tested
            metric_value = math.log2(1 + avg_persistence * k)
            conjecture_holds = True
            counterexample = ""

            if matrix_type == 'DISJ' and avg_persistence < 0.05:
                conjecture_holds = False
                counterexample = f"DISJ matrix with low persistence: {avg_persistence}"

            results.append({
                "n": n,
                "matrix_type": matrix_type,
                "metric_name": "log2(1 + E_S[τ_PH] * k)",
                "metric_value": metric_value,
                "instances_tested": instances_tested,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample
            })

    return results

def main():
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    all_results = []

    for seed in seeds:
        results = run_trial(seed)
        for result in results:
            print(f"TRIAL: {result}")
            all_results.append(result)

    metric_values = [result["metric_value"] for result in all_results if result["matrix_type"] in ['DISJ', 'IP']]
    eq_metric_values = [result["metric_value"] for result in all_results if result["matrix_type"] == 'EQ']

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    mean_eq_metric = sum(eq_metric_values) / len(eq_metric_values) if eq_metric_values else 0

    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results) if all_results else 0

    if any(result["counterexample"] for result in all_results):
        counterexample = next(result["counterexample"] for result in all_results if result["counterexample"])
        first_failing_seed = next(result["seed"] for result in all_results if result["counterexample"])
        print(f'RESULT: FALSIFIED counterexample="{counterexample}" first_failing_seed={first_failing_seed}')
    elif support_fraction >= 0.8 and mean_metric >= 0.8 * max(result["n"] for result in all_results) and mean_eq_metric <= math.log2(max(result["n"] for result in all_results)) + 1:
        print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')

if __name__ == "__main__":
    main()