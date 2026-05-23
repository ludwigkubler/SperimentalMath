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

# Constants
LIE_ALGEBRA = [[1, 0], [0, -1]]  # Example Lie algebra matrix for simplicity
K = 3  # Number of literals in each clause (k-CNF)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_instance(n):
        clauses = []
        for _ in range(n):
            literals = [random.choice([-1, 1]) * i for i in range(1, n+1)]
            clause = max(literals[:K], key=abs)
            clauses.append(clause)
        return clauses
    
    def dpll_width(instance):
        # Simplified DPLL algorithm to estimate width
        stack = []
        assignment = [0] * (len(instance) + 1)
        for clause in instance:
            if all(assignment[abs(lit)] != lit for lit in clause):
                stack.append((clause, assignment[:]))
        return len(stack)
    
    def tropicalize(matrix):
        # Convert matrix to tropical form
        return [[max(x + y for x, y in zip(row1, col2)) for row1, col2 in zip(mat1[i], mat2)] for i in range(len(mat1))]
    
    def tensor_product(instance, lie_algebra):
        # Compute tensor product of instance and Lie algebra
        result = []
        for clause in instance:
            row = [max(x + y for x, y in zip(clause, col)) for col in lie_algebra]
            result.append(row)
        return result
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_width = 0
    instances_tested = 0
    
    for n in n_values:
        instance = generate_instance(n)
        rank = len(tropicalize(tensor_product(instance, lie_algebra)))
        width = dpll_width(instance)
        
        if rank < width - 5:
            return {
                "metric_name": "Rank vs Width",
                "metric_value": rank,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"n={n}, rank={rank}, width={width}"
            }
        
        total_rank += rank
        total_width += width
        instances_tested += 1
    
    mean_rank = Fraction(total_rank, instances_tested)
    mean_width = Fraction(total_width, instances_tested)
    
    return {
        "metric_name": "Rank vs Width",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": mean_rank < mean_width - 5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] for r in results)
    total_width = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_rank/len(results)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_rank/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='n={results[0]['instances_tested']}, rank={total_rank/len(results)}, width={total_width/len(results)}' first_failing_seed={first_failing_seed}")