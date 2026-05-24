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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def characteristic_polynomial(f):
        n = len(f)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                if f[i * 2 + j] == 1:
                    A[i][j] = 1
        A[n][:] = [1] * (n + 1)
        return A
    
    def riemann_hypothesis_exponent(A):
        n = len(A) - 1
        det = determinant(A)
        if det == 0:
            return None
        return Fraction(n, math.log2(abs(det)))
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def k_clique_instance(f, n, k):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if f[i * 2 + j] == 1:
                    edges.append((i, j))
        return edges
    
    def communication_complexity(edges, k):
        # Simplified model: each edge requires one bit to communicate
        return len(edges)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    A = characteristic_polynomial(f)
    exponent = riemann_hypothesis_exponent(A)
    if exponent is None:
        return {
            "metric_name": "riemann_hypothesis_exponent",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    edges = k_clique_instance(f, n, 3)
    cc = communication_complexity(edges, 3)
    
    return {
        "metric_name": "riemann_hypothesis_exponent",
        "metric_value": exponent.numerator / exponent.denominator,
        "instances_tested": 1,
        "conjecture_holds": exponent <= Fraction(n, math.log2(2**n / n)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")