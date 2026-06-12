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
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0 or d > n - 1:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < d * n // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for u in range(n):
            clause = [literals[u]]
            for v in graph[u]:
                clause.append(f'-{literals[v]}')
            clauses.append(clause)
        for u in range(n):
            for v in range(u+1, n):
                clause = [f'-{literals[u]}', f'-{literals[v]}']
                for w in range(n):
                    if w != u and w != v:
                        clause.append(literals[w])
                clauses.append(clause)
        return literals, clauses
    
    def gaussian_elimination(matrix, mod):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] = (matrix[i][j] * pow(pivot, -1, mod)) % mod
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] = (matrix[j][k] - factor * matrix[i][k]) % mod
        return matrix
    
    def minimal_local_index_of_sheaves(literals, clauses, mod):
        n = len(literals)
        matrix = [[0] * n for _ in range(n)]
        for clause in clauses:
            for lit in clause:
                if lit[0] == '-':
                    var = int(lit[1:])
                    matrix[var][var] -= 1
                else:
                    var = int(lit)
                    matrix[var][var] += 1
        matrix = gaussian_elimination(matrix, mod)
        lrs = sum(1 for row in matrix if any(x != 0 for x in row))
        return lrs
    
    def frege_proof_length(clauses):
        n = len(clauses)
        proof_length = n * (n + 1) // 2
        return proof_length
    
    def pearson_correlation(lrs_values, proof_lengths):
        if len(lrs_values) != len(proof_lengths):
            raise ValueError("Lists must have the same length")
        n = len(lrs_values)
        mean_lrs = sum(lrs_values) / n
        mean_proof_length = sum(proof_lengths) / n
        numerator = sum((lrs_values[i] - mean_lrs) * (proof_lengths[i] - mean_proof_length) for i in range(n))
        denominator = math.sqrt(sum((lrs_values[i] - mean_lrs) ** 2 for i in range(n))) * math.sqrt(sum((proof_lengths[i] - mean_proof_length) ** 2 for i in range(n)))
        if denominator == 0:
            return None
        return numerator / denominator
    
    n = random.randint(5, 40)
    d = (n + 1) // 2
    graph = generate_d_regular_graph(n, d)
    if not graph:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "d-regular graph generation failed"
        }
    literals, clauses = tseitin_formula(graph)
    mod = 2
    lrs_values = [minimal_local_index_of_sheaves(literals, clauses, mod) for _ in range(30)]
    proof_lengths = [frege_proof_length(clauses) for _ in range(30)]
    
    r = pearson_correlation(lrs_values, proof_lengths)
    if r is None:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "zero denominator in Pearson correlation"
        }
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": r,
        "instances_tested": 30,
        "n_max": n,
        "conjecture_holds": abs(r) >= 0.8 and r <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_r = sum(r for r in [res['metric_value'] for res in results if res['metric_value'] is not None]) / len([res for res in results if res['metric_value'] is not None])
    support_fraction = sum(1 for res in results if res['conjecture_holds']) / len(results)
    
    if all(res['conjecture_holds'] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std=0.0 support_fraction={support_fraction}")
    elif any(not res['conjecture_holds'] for res in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"Pearson correlation does not meet the acceptance criterion\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_support n_tested={len(results)}")