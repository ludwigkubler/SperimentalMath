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
    if isinstance(x, int) or isinstance(y, int):
        return bin(x ^ y).count('1')
    return sum(1 for a, b in zip(x, y) if a != b)

def generate_disj_matrix(n):
    N = 2 ** n
    matrix = []
    for i in range(N):
        row = [0] * N
        for j in range(n):
            if (i >> j) & 1:
                row[(1 << j) - 1] = 1
        matrix.append(row)
    return matrix

def generate_ip_matrix(n):
    N = 2 ** n
    matrix = []
    for i in range(N):
        row = [0] * N
        for j in range(N):
            row[j] = bin(i & j).count('1') % 2
        matrix.append(row)
    return matrix

def generate_eq_matrix(n):
    N = 2 ** n
    matrix = []
    for i in range(N):
        row = [0] * N
        row[i] = 1
        matrix.append(row)
    return matrix

def generate_random_matrix(n):
    N = 2 ** n
    matrix = []
    for _ in range(N):
        row = [random.choice([0, 1]) for _ in range(N)]
        matrix.append(row)
    return matrix

def compute_boundary_matrix(rows, max_distance):
    N = len(rows[0])
    boundary_matrix = defaultdict(list)
    for i, row in enumerate(rows):
        for j, col in enumerate(row):
            if col == 1:
                boundary_matrix[(i, j)] = []
                for k in range(N):
                    if rows[i][k] == 1 and rows[j][k] == 1:
                        boundary_matrix[(i, j)].append((i, k))
                        boundary_matrix[(i, j)].append((j, k))
    return boundary_matrix

def compute_persistence_diagram(boundary_matrix, max_distance):
    diagram = []
    for (i, j), boundary in boundary_matrix.items():
        if not boundary:
            continue
        birth = min(hamming_distance(u, v) for u, v in itertools.combinations(boundary, 2))
        death = max(hamming_distance(u, v) for u, v in itertools.combinations(boundary, 2))
        if death <= max_distance:
            diagram.append((birth, death))
    return diagram

def run_trial(seed):
    random.seed(seed)
    n_values = [4, 5, 6]
    matrix_families = {
        'DISJ': generate_disj_matrix,
        'IP': generate_ip_matrix,
        'EQ': generate_eq_matrix,
        'RANDOM': generate_random_matrix
    }

    results = []
    for n in n_values:
        N = 2 ** n
        k = math.ceil(math.sqrt(N))
        for family_name, matrix_generator in matrix_families.items():
            matrix = matrix_generator(n)
            total_persistence = 0
            instances_tested = 0
            for _ in range(30):
                S = random.sample(range(N), k)
                rows = [matrix[i] for i in S]
                max_distance = sorted([hamming_distance(rows[i], rows[j]) for i, j in itertools.combinations(range(k), 2)])[int(0.75 * len(S) * (len(S) - 1) / 2)]
                boundary_matrix = compute_boundary_matrix(rows, max_distance)
                diagram = compute_persistence_diagram(boundary_matrix, max_distance)
                persistence = sum(death - birth for birth, death in diagram) / N
                total_persistence += persistence
                instances_tested += 1

            avg_persistence = total_persistence / instances_tested
            metric_value = math.log2(1 + avg_persistence * k)
            conjecture_holds = True
            counterexample = ""

            if family_name == 'DISJ' and avg_persistence < 0.05:
                conjecture_holds = False
                counterexample = f"DISJ matrix with n={n} has persistence {avg_persistence} < 0.05"

            results.append({
                'n': n,
                'family': family_name,
                'metric_name': 'log2(1 + E_S[τ_PH] * k)',
                'metric_value': metric_value,
                'instances_tested': instances_tested,
                'conjecture_holds': conjecture_holds,
                'counterexample': counterexample
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

    if not all_results:
        print("RESULT: INCONCLUSIVE reason=no_trials_executed")
        return

    disj_results = [r for r in all_results if r['family'] == 'DISJ']
    ip_results = [r for r in all_results if r['family'] == 'IP']
    eq_results = [r for r in all_results if r['family'] == 'EQ']

    disj_mean = sum(r['metric_value'] for r in disj_results) / len(disj_results)
    ip_mean = sum(r['metric_value'] for r in ip_results) / len(ip_results)
    eq_mean = sum(r['metric_value'] for r in eq_results) / len(eq_results)

    disj_std = math.sqrt(sum((r['metric_value'] - disj_mean) ** 2 for r in disj_results) / len(disj_results))
    ip_std = math.sqrt(sum((r['metric_value'] - ip_mean) ** 2 for r in ip_results) / len(ip_results))
    eq_std = math.sqrt(sum((r['metric_value'] - eq_mean) ** 2 for r in eq_results) / len(eq_results))

    disj_support = sum(1 for r in disj_results if r['conjecture_holds']) / len(disj_results)
    ip_support = sum(1 for r in ip_results if r['conjecture_holds']) / len(ip_results)
    eq_support = sum(1 for r in eq_results if r['conjecture_holds']) / len(eq_results)

    if any(r['counterexample'] for r in all_results):
        first_counterexample = next(r for r in all_results if r['counterexample'])
        print(f"RESULT: FALSIFIED counterexample=\"{first_counterexample['counterexample']}\" first_failing_seed={seeds[all_results.index(first_counterexample)]}")
    elif disj_support >= 0.8 and ip_support >= 0.8 and eq_support >= 0.8:
        print(f"RESULT: SUPPORTED mean_disj={disj_mean:.2f} std_disj={disj_std:.2f} support_fraction_disj={disj_support:.2f} mean_ip={ip_mean:.2f} std_ip={ip_std:.2f} support_fraction_ip={ip_support:.2f} mean_eq={eq_mean:.2f} std_eq={eq_std:.2f} support_fraction_eq={eq_support:.2f}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")

if __name__ == "__main__":
    main()