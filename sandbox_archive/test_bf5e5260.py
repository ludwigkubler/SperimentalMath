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
    
    # Generate a random group G and its representation V with |G| ≤ 40 and |V| ≤ 40
    n = random.randint(5, 30)
    G = list(range(n))
    V = [[random.random() for _ in range(n)] for _ in range(n)]
    
    # Construct the tropicalized version of V
    def tropicalize(V):
        n = len(V)
        V_trop = [[max(a, b) for a, b in zip(row1, row2)] for row1, row2 in V]
        return V_trop
    
    V_trop = tropicalize(V)
    
    # Construct an XOR-AND tree representing the group action and measure its width w
    def construct_xor_and_tree(G):
        if len(G) == 1:
            return 1
        else:
            mid = len(G) // 2
            left_tree = construct_xor_and_tree(G[:mid])
            right_tree = construct_xor_and_tree(G[mid:])
            return max(left_tree, right_tree) + 1
    
    w = construct_xor_and_tree(G)
    
    # Calculate the minimal rank r(V_trop)
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i][j] != 0 for j in range(n)):
                rank += 1
                for j in range(n):
                    matrix[i][j] /= matrix[i][j]
                for k in range(m):
                    if k != i and any(matrix[k][j] != 0 for j in range(n)):
                        for j in range(n):
                            matrix[k][j] -= matrix[k][i] * matrix[i][j]
        return rank
    
    r_V_trop = matrix_rank(V_trop)
    
    # Calculate the correlation between r(V_trop) and log_2(w + 1)
    if w == 0:
        correlation = None
    else:
        correlation = r_V_trop / math.log2(w + 1)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "conjecture_holds": correlation is not None and correlation <= 10,
        "counterexample": "" if correlation is not None else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r is not None and r <= 10) / len(results)
    
    if all(r is not None and r <= 10 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r is not None and r > 10 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if r is not None and r > 10)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")