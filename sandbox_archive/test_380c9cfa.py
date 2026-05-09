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

def generate_k_clique(n, k):
    if k > n:
        return None
    vertices = list(range(n))
    edges = []
    for i in range(k):
        for j in range(i + 1, k):
            edges.append((vertices[i], vertices[j]))
    for _ in range(n - k):
        u = random.choice(vertices)
        v = random.choice(vertices)
        if (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
    return edges

def generate_dnf(n, m):
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) < 2 or random.choice([True, False]):
            clause.add(random.randint(0, n - 1))
        clauses.append(tuple(sorted(clause)))
    return clauses

def hypergraph_to_matrix(hypergraph, n):
    matrix = [[0] * n for _ in range(n)]
    for edge in hypergraph:
        for i in edge:
            for j in edge:
                if i != j:
                    matrix[i][j] += 1
    return matrix

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] + [0] * n for row in matrix]
    rank = 0
    for col in range(n):
        pivot_row = -1
        for i in range(rank, n):
            if augmented_matrix[i][col] != 0:
                pivot_row = i
                break
        if pivot_row == -1:
            continue
        augmented_matrix[pivot_row], augmented_matrix[rank] = augmented_matrix[rank], augmented_matrix[pivot_row]
        for i in range(n):
            if i != rank and augmented_matrix[i][col] != 0:
                factor = augmented_matrix[i][col] / augmented_matrix[rank][col]
                for j in range(2 * n):
                    augmented_matrix[i][j] -= factor * augmented_matrix[rank][j]
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        k_clique_edges = generate_k_clique(n, n // 2)
        dnf_clauses = generate_dnf(n, n * (n - 1) // 2)
        
        if k_clique_edges is None:
            continue
        
        k_clique_matrix = hypergraph_to_matrix(k_clique_edges, n)
        dnf_matrix = hypergraph_to_matrix(dnf_clauses, n)
        
        rank_k_clique = gaussian_elimination(k_clique_matrix)
        rank_dnf = gaussian_elimination(dnf_matrix)
        
        if rank_k_clique < 0.7 * math.sqrt(n):
            return {
                "metric_name": "rank",
                "metric_value": rank_k_clique,
                "instances_tested": len(results),
                "conjecture_holds": False,
                "counterexample": f"k-CLIQUE: n={n}, rank={rank_k_clique}"
            }
        if rank_dnf > 5 * math.log(n):
            return {
                "metric_name": "rank",
                "metric_value": rank_dnf,
                "instances_tested": len(results),
                "conjecture_holds": False,
                "counterexample": f"DNF: n={n}, rank={rank_dnf}"
            }
        results.append((rank_k_clique, rank_dnf))
    
    mean_rank_k_clique = sum(rank for rank, _ in results) / len(results)
    mean_rank_dnf = sum(rank for _, rank in results) / len(results)
    support_fraction = len([r for r, _ in results if r >= 0.7 * math.sqrt(n)]) / len(results)
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank_k_clique,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.2f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank_k_clique = sum(r for r, _ in [res for res in results if 'k-CLIQUE' in res['counterexample']]) / len([res for res in results if 'k-CLIQUE' in res['counterexample']])
    mean_rank_dnf = sum(r for _, r in [res for res in results if 'DNF' in res['counterexample']]) / len([res for res in results if 'DNF' in res['counterexample']])
    support_fraction = sum(1 for res in results if 'k-CLIQUE' not in res['counterexample']) / len(results)
    
    if all(res['conjecture_holds'] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank_k_clique:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif any('k-CLIQUE' in res['counterexample'] for res in results) or any('DNF' in res['counterexample'] for res in results):
        print(f"RESULT: FALSIFIED counterexample=\"{'k-CLIQUE' if any('k-CLIQUE' in res['counterexample'] for res in results) else 'DNF'}\" first_failing_seed={seeds[next(i for i, res in enumerate(results) if 'k-CLIQUE' in res['counterexample'] or 'DNF' in res['counterexample'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")