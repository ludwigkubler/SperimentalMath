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
    
    def generate_tseitin_formula(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(m):
            clause = random.choice(variables)
            if random.choice([True, False]):
                clause = f'~{clause}'
            clauses.append(clause)
        return ' & '.join(clauses)

    def evaluate_clause(clause, assignment):
        if '~' in clause:
            var = clause[2:]
            return not assignment[int(var) - 1]
        else:
            return assignment[int(clause) - 1]

    def tropicalize_vector(v):
        return [max(x, y) for x, y in zip(v, v)]

    def tensor_product(vectors):
        if len(vectors) == 0:
            return []
        elif len(vectors) == 1:
            return vectors[0]
        else:
            result = []
            for i in range(len(vectors[0])):
                row = [max(vectors[j][i], vectors[j+1][i]) for j in range(0, len(vectors)-1, 2)]
                if len(vectors) % 2 == 1:
                    row.append(max(vectors[-1][i], vectors[-2][i]))
                result.append(row)
            return tensor_product(result)

    def resolution_width(clauses):
        width = 0
        for clause in clauses:
            if ' & ' in clause:
                width += len(clause.split(' & '))
            else:
                width += 1
        return width

    n = random.randint(5, 30)
    m = random.randint(n, 2 * n)
    formula = generate_tseitin_formula(n, m)
    clauses = formula.split(' & ')
    
    assignment = [random.choice([True, False]) for _ in range(n)]
    ranks = []
    widths = []

    for clause in clauses:
        rank = 0
        for var in variables:
            if var in clause or f'~{var}' in clause:
                rank += 1
        ranks.append(rank)
    
    tensor_prod = tensor_product([tropicalize_vector([evaluate_clause(clause, assignment) for clause in clauses])])
    min_rank = len(tensor_prod)

    width = resolution_width(clauses)

    return {
        "metric_name": "min_rank_over_width",
        "metric_value": min_rank / width,
        "instances_tested": 1,
        "conjecture_holds": min_rank <= width,
        "counterexample": "" if min_rank <= width else f"Formula: {formula}, Min Rank: {min_rank}, Width: {width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*3 + 1))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")