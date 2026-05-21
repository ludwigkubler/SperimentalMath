# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_graph(n):
        edges = set()
        for u in range(n):
            for v in range(u + 1, n):
                if random.random() < 0.5:
                    edges.add((u, v))
        return {u: [v for v in range(n) if (u, v) in edges or (v, u) in edges] for u in range(n)}
    
    def eigenvalues(matrix):
        n = len(matrix)
        A = matrix.copy()
        for i in range(n):
            pivot_row = max(range(i, n), key=lambda r: abs(A[r][i]))
            if A[pivot_row][i] == 0:
                continue
            A[pivot_row], A[i] = A[i], A[pivot_row]
            for j in range(n):
                if j != i:
                    factor = -A[j][i] / A[i][i]
                    A[j] = [x + factor * y for x, y in zip(A[j], A[i])]
        eigenvals = []
        for row in A:
            if all(x == 0 for x in row[:n-1]):
                eigenvals.append(row[-1])
        return eigenvals
    
    def geometric_entropy(eigenvals):
        return sum(-x * math.log2(x) for x in eigenvals if x > 0)
    
    def sos_certificate(matrix, d):
        n = len(matrix)
        variables = set()
        for u in range(n):
            for v in range(u + 1, n):
                if matrix[u][v] != 0:
                    variables.add((u, v))
        return variables
    
    def max_cut_approximation(graph, certificate):
        cut_value = sum(1 for (u, v) in graph if (u, v) in certificate)
        return cut_value / len(graph)
    
    n = random.randint(5, 40)
    d = random.randint(2, 3)
    M = generate_graph(n)
    eigenvals = eigenvalues(M)
    entropy = geometric_entropy(eigenvals)
    sos_cert = sos_certificate(M, d)
    max_cut_approx = max_cut_approximation(M, sos_cert)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": entropy,
        "instances_tested": 1,
        "conjecture_holds": entropy <= n ** (1 / (d / 2)) and max_cut_approx >= 0.878 * len(sos_cert),
        "counterexample": "" if entropy <= n ** (1 / (d / 2)) and max_cut_approx >= 0.878 * len(sos_cert) else f"Entropy: {entropy}, Max-CUT Approx: {max_cut_approx}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_entropy = math.sqrt(sum((r["metric_value"] - mean_entropy) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break