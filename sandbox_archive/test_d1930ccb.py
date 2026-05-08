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

def generate_random_3cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = []
        for _ in range(3):
            var = random.randint(0, n - 1)
            sign = random.choice([-1, 1])
            clause.append((sign, var))
        clauses.append(clause)
    return clauses

def communication_matrix(clauses, n):
    m = 2 ** n
    matrix = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            x = [int(bin(i)[2:].zfill(n)[j // (1 << k) & 1]) for k in range(n)]
            y = [int(bin(j)[2:].zfill(n)[k // (1 << k) & 1]) for k in range(n)]
            if all((x[var] == sign or x[var] == -sign) for sign, var in clauses):
                matrix[i][j] = 1
    return matrix

def viterbi_algorithm(matrix, n):
    m = 2 ** n
    dist = [[math.inf] * m for _ in range(m)]
    prev = [[None] * m for _ in range(m)]
    dist[0][0] = 0
    
    for i in range(m):
        for j in range(m):
            if matrix[i][j] == 1:
                for k in range(n):
                    if (i & (1 << k)) != (j & (1 << k)):
                        new_dist = dist[i][k] + 1
                        if new_dist < dist[j][k]:
                            dist[j][k] = new_dist
                            prev[j][k] = i
    
    return dist, prev

def backtrack(prev, n):
    m = 2 ** n
    paths = []
    for j in range(m):
        path = [j]
        k = j
        while prev[k][path[-1]] is not None:
            path.append(prev[k][path[-1]])
            k = path[-1]
        paths.append(path[::-1])
    return paths

def persistent_homology(matrix, n):
    m = 2 ** n
    dist, _ = viterbi_algorithm(matrix, n)
    bars = []
    
    for i in range(m):
        for j in range(i + 1, m):
            if dist[i][j] < math.inf:
                bars.append((dist[i][j], dist[j][i]))
    
    return bars

def karchmer_wigderson_protocol_cost(n):
    # Simplified approximation for demonstration purposes
    return n * (n - 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    clauses = generate_random_3cnf(n)
    matrix = communication_matrix(clauses, n)
    bars = persistent_homology(matrix, n)
    barcode_lengths = [bar[0] for bar in bars]
    sum_barcode_lengths = sum(barcode_lengths) / (2 ** n)
    cc_f = karchmer_wigderson_protocol_cost(n)
    
    if cc_f == 0:
        return {
            "metric_name": "Sum of Barcode Lengths",
            "metric_value": sum_barcode_lengths,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "CC(f) is zero, cannot compute Θ(log CC(f))"
        }
    
    ratio = sum_barcode_lengths / math.log(cc_f)
    return {
        "metric_name": "Sum of Barcode Lengths",
        "metric_value": sum_barcode_lengths,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - 1) < 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")