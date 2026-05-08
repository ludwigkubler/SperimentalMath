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

def generate_random_circuit(n, s, d):
    gates = []
    for _ in range(s):
        gate_type = random.choice(['AND', 'OR', 'NOT', 'MOD_2', 'MOD_3'])
        if gate_type == 'NOT':
            inputs = [random.randint(0, n-1)]
        else:
            inputs = sorted(random.sample(range(n), 2))
        gates.append((gate_type, inputs))
    return gates

def evaluate_circuit(circuit, input_values):
    for gate_type, inputs in circuit:
        if gate_type == 'AND':
            result = all(input_values[i] for i in inputs)
        elif gate_type == 'OR':
            result = any(input_values[i] for i in inputs)
        elif gate_type == 'NOT':
            result = not input_values[inputs[0]]
        elif gate_type == 'MOD_2':
            result = sum(input_values[i] for i in inputs) % 2
        elif gate_type == 'MOD_3':
            result = sum(input_values[i] for i in inputs) % 3
        else:
            raise ValueError(f"Unknown gate type: {gate_type}")
        input_values.append(result)
    return input_values[-1]

def compute_anf(truth_table):
    n = int(math.log2(len(truth_table)))
    anf = [0] * (1 << n)
    for i in range(1 << n):
        anf[i] = truth_table[i]
    for k in range(n-1, -1, -1):
        mask = 1 << k
        for i in range((1 << n) - 1, -1, -1):
            if i & mask:
                anf[i] ^= anf[i ^ mask]
    return anf

def compute_catalecticant_matrix(anf, n, k):
    from itertools import combinations
    C = list(combinations(range(n), k))
    M = [[0] * len(C) for _ in range(len(C))]
    for i, S in enumerate(C):
        for j, T in enumerate(C):
            if not set(S).intersection(set(T)):
                U = tuple(sorted(S + T))
                M[i][j] = anf[sum(1 << bit for bit in U)]
    return M

def gaussian_elimination(M):
    n = len(M)
    rank = 0
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        if M[i][i] == 0:
            continue
        rank += 1
        for j in range(i+1, n):
            factor = M[j][i] / M[i][i]
            for k in range(n):
                M[j][k] -= factor * M[i][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [8, 10, 12]:
        for s in [n, 3*n, 9*n]:
            for d in [2, 3]:
                circuit = generate_random_circuit(n, s, d)
                input_values = [random.randint(0, 1) for _ in range(n)]
                truth_table = [evaluate_circuit(circuit, input_values[:i] + [val] + input_values[i+1:]) for i in range(1 << n)]
                anf = compute_anf(truth_table)
                M = compute_catalecticant_matrix(anf, n, n // 2)
                rank = gaussian_elimination(M)
                results.append((s, d, rank))
    
    random_truth_table = [random.randint(0, 1) for _ in range(1 << n)]
    anf_random = compute_anf(random_truth_table)
    M_random = compute_catalecticant_matrix(anf_random, n, n // 2)
    rank_random = gaussian_elimination(M_random)
    
    MAJ_n_truth_table = [int(i == n // 2) for i in range(1 << n)]
    anf_MAJ_n = compute_anf(MAJ_n_truth_table)
    M_MAJ_n = compute_catalecticant_matrix(anf_MAJ_n, n, n // 2)
    rank_MAJ_n = gaussian_elimination(M_MAJ_n)
    
    mean_rank = sum(rank for _, _, rank in results) / len(results)
    std_rank = math.sqrt(sum((rank - mean_rank) ** 2 for _, _, rank in results) / len(results))
    slope, intercept = 0, 0
    if len(results) > 1:
        x = [math.log(s * d + 1) for s, d, _ in results]
        y = [math.log(rank) for _, _, rank in results]
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
    
    conjecture_holds = all(rank <= (s + 1) ** (2 * d) for s, d, rank in results)
    random_support = sum(1 for rank in [rank_random, rank_MAJ_n] if rank >= Fraction(n, 2) * math.comb(n, n // 2)) / 2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "MCR",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3**j + 5**k for i, j, k in product(range(4), range(4), range(4))]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    std_rank = math.sqrt(sum((res["metric_value"] - mean_rank) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")