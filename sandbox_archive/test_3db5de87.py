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
    
    def generate_k_cnf(k, m):
        variables = set()
        clauses = []
        for _ in range(m):
            clause = random.sample(variables | {-v for v in variables}, k)
            clauses.append(clause)
            variables.update(clause)
        return clauses
    
    def incidence_matrix(clauses):
        n = len(clauses)
        m = len(set(abs(v) for clause in clauses for v in clause))
        M = [[0] * m for _ in range(n)]
        var_map = {}
        i = 0
        for v in set(abs(v) for clause in clauses for v in clause):
            var_map[v] = i
            i += 1
        for j, clause in enumerate(clauses):
            for v in clause:
                M[j][var_map[abs(v)]] = 1 if v > 0 else -1
        return M
    
    def determinant(M):
        n = len(M)
        if n == 1:
            return M[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in M[1:]]
            det += (-1) ** j * M[0][j] * determinant(submatrix)
        return det
    
    def shannon_entropy(clause_set):
        n = len(clause_set)
        counts = {}
        for clause in clause_set:
            count = tuple(sorted(clause))
            if count in counts:
                counts[count] += 1
            else:
                counts[count] = 1
        entropy = 0
        for count in counts.values():
            p = count / n
            entropy -= p * math.log2(p)
        return entropy
    
    def minimal_brauer_group_order(M):
        det = determinant(M)
        if det == 0:
            return None
        return abs(det)
    
    k = random.randint(3, 5)  # Number of literals per clause
    m = random.randint(10, 20)  # Number of clauses
    n = len(set(abs(v) for v in generate_k_cnf(k, m)))
    if n <= 1:
        return {
            "metric_name": "minimal_brauer_group_order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    clauses = generate_k_cnf(k, m)
    M = incidence_matrix(clauses)
    order = minimal_brauer_group_order(M)
    if order is None:
        return {
            "metric_name": "minimal_brauer_group_order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    entropy = shannon_entropy(clauses)
    if entropy == 0:
        return {
            "metric_name": "minimal_brauer_group_order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = order / entropy
    return {
        "metric_name": "minimal_brauer_group_order",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 10,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_conjecture")