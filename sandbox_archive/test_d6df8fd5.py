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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        max_queries = 2**n
        queries = set()
        while len(queries) < max_queries:
            query = tuple(random.sample(range(n), n))
            if f[query] not in [0, 1]:
                return -1
            queries.add(query)
        return len(queries)
    
    def ehrhart_semigroup(f):
        n = int(math.log2(len(f)))
        semigroup = set()
        for i in range(2**n):
            binary = format(i, f'0{n}b')
            count = sum(int(bit) for bit in binary)
            if count % 2 == 0:
                semigroup.add(count // 2)
        return len(semigroup)
    
    def rank_ehrhart(f):
        n = int(math.log2(len(f)))
        semigroup = ehrhart_semigroup(f)
        if semigroup == 1:
            return 1
        for r in range(2, n + 1):
            matrix = [[0] * (r + 1) for _ in range(r + 1)]
            for i in range(r + 1):
                matrix[i][i] = 1
            for j in range(r):
                for k in range(j + 1, r + 1):
                    matrix[j][k] = -matrix[k][j]
            det = gaussian_elimination(matrix)
            if det == 0:
                return r
        return n
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            pivot_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[pivot_row][i]):
                    pivot_row = j
            A[i], A[pivot_row] = A[pivot_row], A[i]
            if A[i][i] == 0:
                return 0
            for j in range(i + 1, n):
                factor = -A[j][i] / A[i][i]
                for k in range(n + 1):
                    A[j][k] += factor * A[i][k]
        det = 1
        for i in range(n):
            det *= A[i][i]
        return det
    
    def is_permutation_invariant(f, perm):
        n = int(math.log2(len(f)))
        for i in range(2**n):
            binary = format(i, f'0{n}b')
            permuted_binary = ''.join(binary[perm[j]] for j in range(n))
            if f[i] != f[int(permuted_binary, 2)]:
                return False
        return True
    
    def count_distinct_values(f):
        n = int(math.log2(len(f)))
        distinct_values = set()
        for i in range(2**n):
            binary = format(i, f'0{n}b')
            permuted_binary = ''.join(binary[perm[j]] for j in range(n))
            distinct_values.add(f[int(permuted_binary, 2)])
        return len(distinct_values)
    
    def find_counterexample(f):
        n = int(math.log2(len(f)))
        perms = list(itertools.permutations(range(n)))
        for perm in perms:
            if not is_permutation_invariant(f, perm):
                return f"Permutation {perm} does not preserve symmetry"
        return ""
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    cc_symmetry_det = communication_complexity(f)
    rank_ehrhart_f = rank_ehrhart(f)
    distinct_values = count_distinct_values(f)
    counterexample = find_counterexample(f)
    
    if cc_symmetry_det > rank_ehrhart_f:
        return {
            "metric_name": "Rank_Ehrhart vs CC_SymmetryDet",
            "metric_value": rank_ehrhart_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    else:
        return {
            "metric_name": "Rank_Ehrhart vs CC_SymmetryDet",
            "metric_value": rank_ehrhart_f,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"] != ""), None)
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")