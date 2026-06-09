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
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        max_rank = 0
        for i in range(2**n):
            assignment = [int(x) for x in format(i, f'0{n}b')]
            rank = sum(f[i] != f[j] for j in range(2**n) if assignment == [int(x) for x in format(j, f'0{n}b')])
            max_rank = max(max_rank, rank)
        return max_rank
    
    def grothendieck_tate_module_dimension(f):
        n = int(math.log2(len(f)))
        matrix = [[f[i] ^ f[j] for j in range(2**n)] for i in range(2**n)]
        rank = gaussian_elimination(matrix)
        return 2**n - rank
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            i_max = None
            for i in range(rank, m):
                if A[i][j] == 1:
                    i_max = i
                    break
            if i_max is not None:
                A[rank], A[i_max] = A[i_max], A[rank]
                for i in range(rank + 1, m):
                    factor = A[i][j]
                    for k in range(n):
                        A[i][k] ^= (A[rank][k] * factor) % 2
                rank += 1
        return rank
    
    def variance(values):
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        comm_rank = communication_complexity_rank(f)
        dim_module = grothendieck_tate_module_dimension(f)
        results.append((comm_rank, dim_module))
    
    comm_ranks = [r[0] for r in results]
    dim_modules = [r[1] for r in results]
    
    if any(dim == 0 for dim in dim_modules):
        return {
            "metric_name": "Variance of Communication Complexity Rank",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    var_comm_rank = variance(comm_ranks)
    conjecture_holds = all(var_comm_rank <= dim for dim in dim_modules)
    
    return {
        "metric_name": "Variance of Communication Complexity Rank",
        "metric_value": var_comm_rank,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Var(CommRank)={var_comm_rank} > dim(M_f)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_var_comm_rank = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_var_comm_rank} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)