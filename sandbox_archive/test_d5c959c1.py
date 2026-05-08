# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_truth_table(n):
        return [tuple(random.randint(0, 1) for _ in range(n)) for _ in range(2**n)]
    
    def is_constant(f):
        return all(f[0] == f[i] for i in range(len(f)))
    
    def decision_tree_depth(f, n):
        memo = {}
        
        def dp(sigma):
            if sigma in memo:
                return memo[sigma]
            if len(sigma) == 1:
                return 0
            max_depth = 0
            for i in range(n):
                new_sigma = list(sigma)
                new_sigma[i] = 0
                depth_0 = dp(tuple(new_sigma))
                new_sigma[i] = 1
                depth_1 = dp(tuple(new_sigma))
                if depth_0 == float('inf') or depth_1 == float('inf'):
                    max_depth = float('inf')
                    break
                max_depth = max(max_depth, 1 + max(depth_0, depth_1))
            memo[sigma] = max_depth
            return max_depth
        
        sigma = tuple(random.choice([0, 1]) for _ in range(n))
        return dp(sigma)
    
    def compute_betti_number(f, n):
        vertices = list(range(n))
        simplices = [vertices]
        
        def down_closure(W):
            closure = set(W)
            new_elements = True
            while new_elements:
                new_elements = False
                for v in vertices:
                    if v not in closure and any(w in closure for w in W):
                        closure.add(v)
                        new_elements = True
            return closure
        
        witness_sets = []
        for x, y in product(f, repeat=2):
            if f[x] == 1 and f[y] == 0:
                witness_set = [i for i in range(n) if x[i] != y[i]]
                witness_sets.append(witness_set)
        
        for W in witness_sets:
            simplices.extend(down_closure(W))
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            rank = 0
            for j in range(n):
                pivot_row = -1
                for i in range(rank, m):
                    if A[i][j] == 1:
                        pivot_row = i
                        break
                if pivot_row != -1:
                    A[pivot_row], A[rank] = A[rank], A[pivot_row]
                    rank += 1
                    for i in range(m):
                        if i != rank - 1 and A[i][j] == 1:
                            for k in range(n):
                                A[i][k] ^= A[rank - 1][k]
            return rank
        
        betti_number = 0
        for k in range(n + 1):
            boundary_matrix = []
            for i in range(len(simplices)):
                for j in range(i + 1, len(simplices)):
                    if all(v in simplices[j] for v in simplices[i]):
                        boundary_matrix.append([1 if v in simplices[j] and v not in simplices[i] else 0 for v in vertices])
            betti_number += (-1) ** k * gaussian_elimination(boundary_matrix)
        
        return betti_number
    
    n_values = [3, 4, 5, 6, 7, 8]
    total_trials = 30
    support_count = 0
    counterexample = ""
    
    for n in n_values:
        truth_tables = generate_truth_table(n)
        explicit_families = [
            lambda x: all(x[i] == 1 for i in range(n)),  # AND_n
            lambda x: any(x[i] == 1 for i in range(n)),  # OR_n
            lambda x: x[n // 2] ^ any(x[i] == 1 for i in range(n) if i != n // 2),  # XOR_n
            lambda x: sum(x[:n // 2]) >= n // 2,  # MAJ_n
            lambda x: all(x[i] == 0 for i in range(n - n // 2)) or any(x[i] == 1 for i in range(n - n // 2)),  # Th_{⌈n/2⌉}^n
            lambda x: (x[:a] + x[b:]) if a * b == n else None  # AND_a∘OR_b
        ]
        
        for _ in range(total_trials):
            f = random.choice(truth_tables)
            if is_constant(f):
                continue
            
            dt_depth = decision_tree_depth(f, n)
            betti_number = compute_betti_number(f, n)
            required_depth = math.ceil(math.log2(1 + betti_number))
            
            if dt_depth < required_depth:
                counterexample = f"Decision tree depth {dt_depth} < required depth {required_depth}"
                return {
                    "metric_name": "Decision Tree Depth",
                    "metric_value": dt_depth,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }
            
            if dt_depth >= required_depth:
                support_count += 1
    
    return {
        "metric_name": "Decision Tree Depth",
        "metric_value": (support_count / total_trials) * n_values[-1],
        "instances_tested": total_trials * len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    
    if support_fraction >= 0.95:
        result_status = "SUPPORTED"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        result_status = f"FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result_status} mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")