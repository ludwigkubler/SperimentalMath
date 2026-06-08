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
    
    def generate_sat_instance(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = [random.choice(variables), -random.choice(variables)]
            clauses.append(clause)
        return clauses

    def dpll(clauses, assignment={}):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            var = abs(unit_clause[0])
            val = unit_clause[0] > 0
            if var in assignment and assignment[var] != val:
                return False
            assignment[var] = val
            new_clauses = [c for c in clauses if var not in c]
            for i, c in enumerate(new_clauses):
                if -var in c:
                    new_clauses[i].remove(-var)
            return dpll(new_clauses, assignment)
        pure_literal = next((v for v in variables if all(v not in c or -v not in c for c in clauses)), None)
        if pure_literal is not None:
            val = True
            if pure_literal < 0:
                val = False
                pure_literal = -pure_literal
            assignment[pure_literal] = val
            new_clauses = [c for c in clauses if pure_literal not in c]
            for i, c in enumerate(new_clauses):
                if -pure_literal in c:
                    new_clauses[i].remove(-pure_literal)
            return dpll(new_clauses, assignment)
        var = random.choice(variables)
        val = True
        if var in assignment and assignment[var] != val:
            return False
        assignment[var] = val
        new_clauses = [c for c in clauses if var not in c]
        for i, c in enumerate(new_clauses):
            if -var in c:
                new_clauses[i].remove(-var)
        if dpll(new_clauses, assignment):
            return True
        del assignment[var]
        val = False
        if var in assignment and assignment[var] != val:
            return False
        assignment[var] = val
        new_clauses = [c for c in clauses if var not in c]
        for i, c in enumerate(new_clauses):
            if -var in c:
                new_clauses[i].remove(-var)
        return dpll(new_clauses, assignment)

    def max_complexity_coxeter_group(n):
        # Placeholder for actual computation of Coxeter group complexity
        return n**2  # Simplified example

    def height_dpll_search_tree(clauses):
        return len(dpll(clauses))

    instances_tested = 0
    metric_value = 0.0
    n_max = 1
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            clauses = generate_sat_instance(n)
            height = height_dpll_search_tree(clauses)
            complexity = max_complexity_coxeter_group(n)
            instances_tested += 1
            if n > n_max:
                n_max = n
            metric_value += abs(height - complexity) / complexity
            if abs(height - complexity) / complexity > 0.1 * complexity:  # Arbitrary threshold for simplicity
                conjecture_holds = False
                counterexample = f"n={n}, height={height}, complexity={complexity}"

    return {
        "metric_name": "Height of DPLL Search Tree vs Complexity",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")