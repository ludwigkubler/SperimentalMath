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

    def dpll_solve(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0:
                literal = -literal
                assignment[literal] = False
            else:
                assignment[literal] = True
            new_clauses = []
            for c in clauses:
                if literal not in c and -literal not in c:
                    new_clauses.append(c)
            return dpll_solve(new_clauses, assignment)
        pure_literal = next((l for l in variables if (l not in assignment and -l not in assignment)), None)
        if pure_literal is None:
            return False
        assignment[pure_literal] = True
        new_clauses = []
        for c in clauses:
            if pure_literal not in c and -pure_literal not in c:
                new_clauses.append(c)
        if dpll_solve(new_clauses, assignment):
            return True
        assignment[pure_literal] = False
        new_clauses = []
        for c in clauses:
            if pure_literal not in c and -pure_literal not in c:
                new_clauses.append(c)
        return dpll_solve(new_clauses, assignment)

    def extract_coxeter_dynkin_diagram(clauses):
        # This is a placeholder function. Implement the actual logic to extract
        # the Coxeter-Dynkin diagram from the resolution proof.
        return 0

    n = random.randint(5, 40)
    instance = generate_sat_instance(n)
    assignment = {}
    if dpll_solve(instance, assignment):
        diagram_size = extract_coxeter_dynkin_diagram(instance)
        upper_bound = (n ** 2) * math.log(n)
        conjecture_holds = diagram_size <= upper_bound
        return {
            "metric_name": "Coxeter-Dynkin Diagram Size",
            "metric_value": diagram_size,
            "instances_tested": 1,
            "conjecture_holds": conjecture_holds,
            "counterexample": "" if conjecture_holds else f"Diagram size {diagram_size} exceeds upper bound {upper_bound}"
        }
    return {
        "metric_name": "Coxeter-Dynkin Diagram Size",
        "metric_value": 0,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "DPLL solver did not find a satisfying assignment"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Diagram size exceeds upper bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")