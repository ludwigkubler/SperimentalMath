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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        if unit_clauses:
            var = unit_clauses[0]
            new_assignment = assignment.copy()
            new_assignment[var] = True if var > 0 else False
            if not dpll([c for c in cnf if var not in c], new_assignment):
                new_assignment[var] = False if var > 0 else True
                return dpll([c for c in cnf if var not in c], new_assignment)
            return True
        pure_symbols = {}
        for clause in cnf:
            for lit in clause:
                if abs(lit) not in pure_symbols:
                    pure_symbols[abs(lit)] = (lit > 0, 1)
                else:
                    if pure_symbols[abs(lit)][0] != (lit > 0):
                        return False
                    pure_symbols[abs(lit)][1] += 1
        for lit, (polarity, count) in pure_symbols.items():
            new_assignment = assignment.copy()
            new_assignment[lit] = polarity
            if not dpll([c for c in cnf if lit not in c], new_assignment):
                return False
        return False

    def ehrhart_polygon(cnf):
        variables = set(abs(lit) for clause in cnf for lit in clause)
        n = len(variables)
        vertices = []
        for i in range(2**n):
            assignment = {var: (i >> j) & 1 for j, var in enumerate(sorted(variables))}
            if dpll(cnf, assignment):
                vertices.append([assignment[var] for var in sorted(variables)])
        return vertices

    def distance(p1, p2):
        return sum((x - y)**2 for x, y in zip(p1, p2))**0.5

    def convex_hull(points):
        if len(points) < 3:
            return points
        lower = []
        for (x, y) in sorted(points):
            while len(lower) >= 2 and distance(lower[-2], lower[-1]) + distance(lower[-1], (x, y)) > distance(lower[-2], (x, y)):
                lower.pop()
            lower.append((x, y))
        upper = []
        for (x, y) in sorted(points, key=lambda p: (-p[0], p[1])):
            while len(upper) >= 2 and distance(upper[-2], upper[-1]) + distance(upper[-1], (x, y)) > distance(upper[-2], (x, y)):
                upper.pop()
            upper.append((x, y))
        return lower[:-1] + upper[:-1]

    def area(polygon):
        n = len(polygon)
        return 0.5 * abs(sum(polygon[i][0] * polygon[(i + 1) % n][1] - polygon[i][1] * polygon[(i + 1) % n][0] for i in range(n)))

    def resolution_width(cnf):
        queue = cnf[:]
        while queue:
            new_queue = []
            for clause1 in queue:
                for clause2 in queue:
                    if len(set(clause1).intersection(set(clause2))) == 1:
                        new_clause = [lit for lit in clause1 + clause2 if lit not in set(clause1).intersection(set(clause2))]
                        if len(new_clause) == 0:
                            return float('inf')
                        new_queue.append(new_clause)
            queue = new_queue
        return max(len(clause) for clause in cnf)

    n_values = [5, 10, 15, 20, 30, 40]
    total_points = 0
    total_widths = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            vertices = ehrhart_polygon(cnf)
            hull = convex_hull(vertices)
            points = [tuple(p) for p in hull]
            total_points += len(points)
            width = resolution_width(cnf)
            if width == float('inf'):
                continue
            total_widths += width
            instances_tested += 1
            n_max = max(n_max, n)

    if instances_tested < 30:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean_points = total_points / instances_tested
    mean_widths = total_widths / instances_tested

    correlation_coefficient = (instances_tested * sum(p * w for p, w in zip(points, widths)) - instances_tested * mean_points * mean_widths) / \
                              math.sqrt((instances_tested * sum(p**2 for p in points) - instances_tested * mean_points**2) *
                                        (instances_tested * sum(w**2 for w in widths) - instances_tested * mean_widths**2))

    return {
        "metric_name": "resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(2, 6)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 or r["p_value"] > 0.2 for r in results):
        print("RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")