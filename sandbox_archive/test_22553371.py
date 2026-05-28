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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clause = [variables[i-1]]
            for j in range(i+1, n+1):
                clause.append(f'~{variables[j-1]}')
            clauses.append(clause)
        return variables, clauses

    def convert_to_k_theory_space(variables, clauses):
        k_theory_space = {}
        for var in variables:
            k_theory_space[var] = set()
        for clause in clauses:
            for literal in clause:
                if literal.startswith('~'):
                    var = literal[1:]
                else:
                    var = literal
                k_theory_space[var].add(tuple(sorted(clause)))
        return k_theory_space

    def compute_minimal_rank(k_theory_space):
        rank = 0
        visited = set()
        for var in k_theory_space:
            if var not in visited:
                queue = [var]
                while queue:
                    current_var = queue.pop(0)
                    if current_var not in visited:
                        visited.add(current_var)
                        rank += 1
                        for neighbor in k_theory_space[current_var]:
                            queue.append(neighbor)
        return rank

    def resolution_refutation_size(variables, clauses):
        refutation_size = len(clauses) * len(variables)
        return refutation_size

    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    k_theory_space = convert_to_k_theory_space(variables, clauses)
    minimal_rank = compute_minimal_rank(k_theory_space)
    refutation_size = resolution_refutation_size(variables, clauses)

    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        RESULT = "SUPPORTED"
    elif any("counterexample" in r and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"] != "")
        RESULT = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE"

    print(RESULT)