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

def finite_projective_plane(q):
    points = list(range(q * q + q + 1))
    lines = []
    for i in range(q * q + q + 1):
        line = set()
        for j in range(q * q + q + 1):
            if (i * j) % (q * q + q + 1) == 0:
                line.add(j)
        lines.append(line)
    return points, lines

def cnf_from_plane(points, lines):
    clauses = []
    for point in points:
        for line in lines:
            clause = {point: True}
            for p in line:
                if p != point:
                    clause[p] = False
            clauses.append(clause)
    return clauses

def solve(variables, assignment):
    for var, val in assignment.items():
        variables[var] = val
    for var, val in variables.items():
        if not all(assignment[var] == val for var, val in assignment.items()):
            return False
    return True

def branch_and_bound(cnf):
    variables = {var: None for var in cnf[0].keys()}
    def backtrack(assignment):
        unassigned = [var for var in variables if variables[var] is None]
        if not unassigned:
            return solve(variables, assignment)
        var = unassigned[0]
        for val in [True, False]:
            assignment[var] = val
            if backtrack(assignment):
                return True
            assignment[var] = None
        return False
    return backtrack({})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    q_values = [2, 3]
    results = []
    for q in q_values:
        points, lines = finite_projective_plane(q)
        clauses = cnf_from_plane(points, lines)
        mcsp_value = branch_and_bound(cnf=clauses)
        if not (q**2 / 2 <= mcsp_value <= 2 * q**2):
            return {
                "metric_name": "MCSP Complexity",
                "metric_value": mcsp_value,
                "instances_tested": len(clauses),
                "conjecture_holds": False,
                "counterexample": f"q={q}, MCSP(Φ)={mcsp_value} (not in [{q**2 / 2}, {2 * q**2}])"
            }
    return {
        "metric_name": "MCSP Complexity",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(clauses),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if not result["conjecture_holds"]:
            break
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    if not result["conjecture_holds"]:
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seed}")