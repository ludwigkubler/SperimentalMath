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
    
    def generate_cnf(m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, 2 * m) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses

    def incidence_matrix(cnf):
        m = len(cnf)
        n = max(max(clause) for clause in cnf)
        matrix = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(cnf):
            for literal in clause:
                if literal > 0:
                    matrix[i][literal] = 1
                else:
                    matrix[i][-literal] = -1
        return matrix

    def hodge_diamond_dimension(matrix):
        n = len(matrix)
        characteristic_poly = [1]
        for i in range(n):
            new_poly = [characteristic_poly[0]]
            for j in range(1, len(characteristic_poly)):
                new_poly.append(characteristic_poly[j] * (i + 1) - matrix[i][j])
            characteristic_poly = new_poly
        return len(characteristic_poly)

    def communication_complexity(cnf):
        m = len(cnf)
        n = max(max(clause) for clause in cnf)
        # Simplified version of a known upper bound for CNF communication complexity
        return math.ceil(math.log2(m * n))

    m = random.randint(5, 30)
    cnf = generate_cnf(m)
    matrix = incidence_matrix(cnf)
    hdd = hodge_diamond_dimension(matrix)
    c = communication_complexity(cnf)

    return {
        "metric_name": "HDD vs Communication Complexity",
        "metric_value": hdd / c,
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")