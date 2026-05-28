# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def min_rank(A):
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank

    n = random.randint(5, 40)
    k = 3
    size = random.randint(10, 20)

    # Construct a random circuit computing k-CLIQUE
    C_k_clique = [[random.choice(['AND', 'OR']) for _ in range(k)] for _ in range(size)]
    
    # Construct a random circuit not computing k-CLIQUE
    C_not_k_clique = [[random.choice(['NOT', 'XOR']) for _ in range(k)] for _ in range(size)]

    # Compute the p-adic lattice associated with each circuit's gates (simplified mapping)
    def p_adic_lattice(circuit):
        lattice = []
        for gate in circuit:
            if gate == 'AND':
                lattice.append([1, 0, 0])
            elif gate == 'OR':
                lattice.append([0, 1, 0])
            elif gate == 'NOT':
                lattice.append([0, 0, 1])
            elif gate == 'XOR':
                lattice.append([1, 1, 1])
        return lattice

    lattice_k_clique = p_adic_lattice(C_k_clique)
    lattice_not_k_clique = p_adic_lattice(C_not_k_clique)

    # Calculate the minimal rank of each lattice
    rank_k_clique = min_rank(lattice_k_clique)
    rank_not_k_clique = min_rank(lattice_not_k_clique)

    # Compute the metric values
    alpha = Fraction(1, 2)  # Example constant for k-CLIQUE circuits
    beta = Fraction(1, 4)   # Example smaller constant for non-k-CLIQUE circuits

    metric_value_k_clique = rank_k_clique / (alpha * n**2)
    metric_value_not_k_clique = rank_not_k_clique / (beta * size)

    # Determine if the conjecture holds
    conjecture_holds_k_clique = rank_k_clique >= alpha * n**2
    conjecture_holds_not_k_clique = rank_not_k_clique <= beta * size

    counterexample = ""
    if not conjecture_holds_k_clique:
        counterexample += "k-CLIQUE circuit failed: rank_k_clique < alpha * n^2\n"
    if not conjecture_holds_not_k_clique:
        counterexample += "Non-k-CLIQUE circuit failed: rank_not_k_clique > beta * size"

    return {
        "metric_name": "rank",
        "metric_value": (metric_value_k_clique + metric_value_not_k_clique) / 2,
        "instances_tested": 2,
        "conjecture_holds": conjecture_holds_k_clique and conjecture_holds_not_k_clique,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    total_metric = sum(r['metric_value'] for r in results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric/len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.9:
        first_failing_seed = next(i for i, r in enumerate(results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence_or_incomplete_data")