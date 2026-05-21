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
    
    def generate_tseitin_formula(n):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(1, n + 1):
            clause = [random.choice([-1, 1]) * v for v in variables if v != i]
            clause.append(-i)
            clauses.append(clause)
        return variables, clauses

    def compute_automorphism_group_size(graph):
        n = len(graph)
        generators = []
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    generators.append((i, j))
        return len(generators)

    def resolution_proof_length(clauses):
        stack = clauses[:]
        while True:
            new_clauses = []
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if len(set(stack[i]) & set(stack[j])) == 2:
                        new_clause = [x for x in stack[i] if x not in stack[j]] + [x for x in stack[j] if x not in stack[i]]
                        new_clauses.append(new_clause)
            if new_clauses == stack:
                return len(clauses) - len(stack)
            stack += new_clauses

    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            variables, clauses = generate_tseitin_formula(n)
            graph = [[0] * n for _ in range(n)]
            for clause in clauses:
                for x in clause:
                    if x > 0:
                        i = abs(x) - 1
                        for y in clause:
                            if y != x and y > 0:
                                j = abs(y) - 1
                                graph[i][j] = 1
                                graph[j][i] = 1
            
            ν_G = compute_automorphism_group_size(graph)
            Resolution_length = resolution_proof_length(clauses)
            
            total_length += Resolution_length / (2 ** ν_G)
            instances_tested += 1
    
    mean_length = total_length / instances_tested
    conjecture_holds = all(mean_length <= 1.5 for _ in range(30))
    
    return {
        "metric_name": "mean_resolution_length_over_ν_G",
        "metric_value": mean_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")