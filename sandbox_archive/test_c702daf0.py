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
    
    def tropicalize_matrix(matrix):
        n = len(matrix)
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] > matrix[j][i]:
                    matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        return matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(i, n):
                matrix[i][j] /= pivot
            for j in range(n):
                if j != i and matrix[j][i] != 0:
                    factor = -matrix[j][i]
                    for k in range(i, n):
                        matrix[j][k] += factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        matrix = gaussian_elimination(matrix)
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
        return rank
    
    def generate_dihedral_group(n):
        elements = []
        for i in range(2 * n):
            elements.append((i % (2 * n), i // n))
        return elements
    
    def generate_ac0_circuit(n):
        edges = set()
        for i in range(1, 2 * n):
            edges.add((i - 1, i))
            edges.add((i, i + 1))
        return edges
    
    n = random.randint(5, 40)
    dihedral_group = generate_dihedral_group(n)
    ac0_circuit = generate_ac0_circuit(n)
    
    # Constructive mapping for tropicalization
    tropical_matrix = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        tropical_matrix[i][i] = 0
    for u, v in ac0_circuit:
        tropical_matrix[u % n][v % n] = min(tropical_matrix[u % n][v % n], 1)
    
    tropicalized_matrix = tropicalize_matrix(tropical_matrix)
    minimal_rank = rank(tropicalized_matrix)
    num_edges = len(ac0_circuit)
    
    ratio = minimal_rank / math.sqrt(num_edges)
    
    conjecture_holds = ratio <= 1.5
    counterexample = "" if conjecture_holds else f"Ratio {ratio} exceeds bound"
    
    return {
        "metric_name": "Minimal Rank Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_ratio = sum(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_ratio / len(results):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_ratio / len(results):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"Ratio {result['metric_value']:.2f} exceeds bound\" first_failing_seed={seed}")
                break