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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def frege_proof_depth(phi):
        n = int(math.log2(len(phi)))
        if len(phi) != 2**n or n == 0:
            return float('inf')
        depth = 0
        while any(x > 1 for x in phi):
            new_phi = []
            for i in range(0, len(phi), 2):
                new_phi.append((phi[i] + phi[i+1]) % 2)
            phi = new_phi
            depth += 1
        return depth
    
    def quadratic_form_representation(phi):
        n = int(math.log2(len(phi)))
        Q = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                Q[i][j] = sum(phi[k] * phi[k + 1] for k in range(2**n)) / (2**(n+1))
                if j > i:
                    Q[j][i] = Q[i][j]
        return Q
    
    def tensor_product_rank(Q):
        n = len(Q)
        rank = 0
        while any(any(x != 0 for x in row) for row in Q):
            max_row = max(range(n), key=lambda i: sum(abs(x) for x in Q[i]))
            max_col = max(range(n), key=lambda j: sum(abs(Q[i][j]) for i in range(n)))
            rank += 1
            for i in range(n):
                Q[i][max_col] -= Q[i][max_row] * Q[max_row][max_col]
                Q[max_row][i] -= Q[max_row][max_col] * Q[max_row][i]
        return rank
    
    n = random.randint(5, 30)
    phi = generate_random_boolean_function(n)
    depth = frege_proof_depth(phi)
    if depth == float('inf'):
        return {
            "metric_name": "tensor_product_rank",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "phi has infinite Frege proof depth"
        }
    
    Q = quadratic_form_representation(phi)
    rank = tensor_product_rank(Q)
    
    return {
        "metric_name": "tensor_product_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rank <= 40 and depth <= math.log2(n)**2,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [random.getrandbits(32) for _ in range(30)]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
    
    if all(r["metric_value"] is not None for r in results):
        RESULT = f"SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    else:
        RESULT = f"FALSIFIED counterexample='phi has infinite Frege proof depth' first_failing_seed={first_failing_seed}"
    
    print(RESULT)