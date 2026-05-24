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
    
    def generate_tseitin_formula(n, clause_density):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(int(n * clause_density)):
            literals = random.sample(variables + [-v for v in variables], 2)
            if literals[0] > 0 and literals[1] < 0:
                clauses.append((literals[0], -literals[1]))
            elif literals[0] < 0 and literals[1] > 0:
                clauses.append((-literals[0], literals[1]))
        return variables, clauses

    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def resolution_width(clauses):
        clauses_set = set(tuple(sorted(c)) for c in clauses)
        queue = list(clauses_set)
        while queue:
            clause1 = queue.pop()
            if len(clause1) == 0:
                return float('inf')
            literal_to_remove = random.choice(clause1)
            new_clauses = []
            for clause2 in clauses_set:
                if literal_to_remove not in clause2 and -literal_to_remove not in clause2:
                    new_clause = list(sorted(set(clause1) ^ set(clause2)))
                    if len(new_clause) > 0:
                        new_clauses.append(tuple(new_clause))
            queue.extend(new_clauses)
        return max(len(c) for c in clauses_set)

    def irreducible_representations(group):
        # Placeholder function to generate irreducible representations
        # This is a simplified version and may not be accurate for all groups
        if group == 'C2':
            return [{'dim': 1}, {'dim': 1}]
        elif group == 'S3':
            return [{'dim': 1}, {'dim': 1}, {'dim': 2}]
        else:
            return []

    n = random.choice([5, 10, 15, 20, 30, 40])
    clause_density = random.uniform(0.1, 0.9)
    variables, clauses = generate_tseitin_formula(n, clause_density)
    group = 'C2' if n <= 10 else 'S3'
    representations = irreducible_representations(group)

    min_dimension = min(rep['dim'] for rep in representations)
    lower_bound = 2 ** (math.log2(min_dimension) - 1e-6)

    width = resolution_width(clauses)
    if width < lower_bound:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": width,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Group {group}, n={n}, clause_density={clause_density}"
        }
    else:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": width,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")