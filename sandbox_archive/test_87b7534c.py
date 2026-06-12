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
    
    def tseitin_formula(f, n):
        literals = list(range(-n, 0)) + list(range(1, n+1))
        clauses = []
        for i in range(2**n):
            binary_rep = [int(x) for x in format(i, f'0{n}b')]
            clause = [literals[binary_rep[j]] if binary_rep[j] > 0 else -literals[-binary_rep[j]-1] for j in range(n)]
            clauses.append(clause)
        return literals, clauses
    
    def frege_proof_depth(clauses):
        n = len(clauses[0])
        stack = []
        for clause in clauses:
            if all(x not in stack and -x not in stack for x in clause):
                stack.extend(clause)
            else:
                return float('inf')
        return len(stack)
    
    def geometric_entropy(f, n):
        adjacency_matrix = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if f[i] == f[j]:
                    continue
                diff = [x != y for x, y in zip(format(i, f'0{n}b'), format(j, f'0{n}b'))]
                adjacency_matrix[i][j] = sum(diff)
        degree_sum = sum(sum(row) for row in adjacency_matrix)
        return math.log2(degree_sum / (n * 2**n))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            literals, clauses = tseitin_formula(f, n)
            d = frege_proof_depth(clauses)
            if d == float('inf'):
                continue
            H = geometric_entropy(f, n)
            instances_tested += 1
            n_max = max(n_max, n)
            total_ratio += H / d
    
    if instances_tested < 30:
        return {
            "metric_name": "H(f)/d(φ_f)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_ratio = total_ratio / instances_tested
    std_dev = math.sqrt(sum((H / d - mean_ratio) ** 2 for f in instances_tested) / instances_tested)
    correlation_coefficient = (mean_ratio - 1) / 0.1
    
    return {
        "metric_name": "H(f)/d(φ_f)",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    
    if support_fraction >= 0.8:
        RESULT = f"SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results):.4f} std={math.sqrt(sum((r['metric_value'] - (sum(r['metric_value'] for r in results) / len(results))) ** 2 for r in results) / len(results)):.4f} support_fraction={support_fraction:.4f}"
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}"
    
    print(RESULT)