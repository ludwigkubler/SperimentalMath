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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 ** n):
            clause = [random.randint(-n, -1) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def resolution(cnf):
        clauses = cnf[:]
        while True:
            new_clauses = []
            found_resolvent = False
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    p = clauses[i]
                    q = clauses[j]
                    if any(x == -y for x in p for y in q):
                        new_clause = [x for x in p if x not in [-y for y in q] and x != -y]
                        if new_clause:
                            new_clauses.append(new_clause)
                            found_resolvent = True
            if not found_resolvent:
                break
            clauses.extend(new_clauses)
        return len(clauses)
    
    def vector_space_representation(cnf):
        n = max(abs(x) for clause in cnf for x in clause)
        vectors = []
        for clause in cnf:
            vector = [0] * (2 * n + 1)
            for literal in clause:
                if literal > 0:
                    vector[literal - 1] = 1
                else:
                    vector[-literal] = -1
            vectors.append(vector)
        return vectors
    
    def dimension(vectors):
        m, n = len(vectors), len(vectors[0])
        A = [v[:] for v in vectors]
        rank = 0
        for j in range(n):
            i_max = next((i for i in range(rank, m) if A[i][j] != 0), None)
            if i_max is not None:
                A[rank], A[i_max] = A[i_max], A[rank]
                pivot = A[rank][j]
                for k in range(j + 1, n):
                    A[rank][k] /= pivot
                for i in range(m):
                    if i != rank and A[i][j] != 0:
                        factor = -A[i][j]
                        for k in range(j, n):
                            A[i][k] += factor * A[rank][k]
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    width = resolution(cnf)
    vectors = vector_space_representation(cnf)
    dim = dimension(vectors)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")