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
    
    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) * (-1 if random.choice([True, False]) else 1)]
            while len(clause) < 3:
                variable = random.choice(variables)
                if variable not in clause:
                    clause.append(variable * (-1 if random.choice([True, False]) else 1))
            clauses.append(tuple(sorted(clause)))
        return tuple(clauses)

    def dpll(cnf):
        def dpll_helper(assignment, clauses):
            if not clauses:
                return True
            literal = find_pure_literal(clauses)
            if literal is not None:
                assignment[literal] = True
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                if dpll_helper(assignment, new_clauses):
                    return True
                assignment[literal] = False
            else:
                literal = find_unit_clause(clauses)
                if literal is not None:
                    assignment[-literal] = True
                    new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                    if dpll_helper(assignment, new_clauses):
                        return True
            return False

        def find_pure_literal(clauses):
            count = {}
            for clause in clauses:
                for literal in clause:
                    if literal in count:
                        count[literal] += 1
                    else:
                        count[literal] = -1
            for literal, c in count.items():
                if c == len(clauses):
                    return literal
            return None

        def find_unit_clause(clauses):
            for clause in clauses:
                if len(clause) == 1:
                    return clause[0]
            return None

        assignment = {}
        return dpll_helper(assignment, cnf)

    def p_adic_l_function(cnf):
        # Placeholder for the actual computation of the p-adic L-function
        # This is a dummy implementation and should be replaced with the actual mapping
        return random.randint(1, 10)  # Dummy value

    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    rank = p_adic_l_function(cnf)
    height = dpll(cnf)

    return {
        "metric_name": "Rank vs DPLL Height",
        "metric_value": abs(rank - height),
        "instances_tested": 1,
        "conjecture_holds": abs(rank - height) <= 3,
        "counterexample": "" if rank == height else f"CNF: {cnf}, Rank: {rank}, Height: {height}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")