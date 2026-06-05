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
    
    def generate_formula(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for j in range(i)):
                clauses.append(clause)
        return clauses

    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        pure_literal = next((l for l in range(1, n+1) if (l in assignment or -l in assignment) and (-l in assignment or l in assignment)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            new_assignment[pure_literal] = False
            if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            return False
        literal, _ = random.choice(clauses)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        return False

    def resolution_width(clauses):
        queue = set()
        for clause in clauses:
            queue.add(tuple(sorted(clause)))
        while queue:
            clause1, clause2 = random.sample(queue, 2)
            resolvent = []
            for l1 in clause1:
                if -l1 in clause2:
                    resolvent.extend(l for l in clause2 if l != -l1)
                    break
            if not resolvent:
                continue
            resolvent.sort()
            queue.discard(clause1)
            queue.discard(clause2)
            queue.add(tuple(resolvent))
        return max(len(c) for c in queue)

    def algebraic_independence_relations(clauses):
        n = len(clauses[0])
        relations = []
        for i in range(n):
            for j in range(i+1, n):
                relation = [clauses[k][i] * clauses[k][j] for k in range(len(clauses))]
                if all(relation[k] != -relation[j] for k in range(j)):
                    relations.append(tuple(sorted(relation)))
        return relations

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        clauses = generate_formula(n)
        width = resolution_width(clauses)
        relations = algebraic_independence_relations(clauses)
        depth = dpll(clauses, {})
        results.append((n, width, len(relations), depth))

    m_n = sum(r[2] for r in results) / len(results)
    w_n = sum(r[1] for r in results) / len(results)
    correlation_coefficient = (sum((r[2] - m_n) * (r[1] - w_n) for r in results) /
                               math.sqrt(sum((r[2] - m_n)**2 for r in results) *
                                         sum((r[1] - w_n)**2 for r in results)))
    p_value = 2 * (1 - 0.5 * (1 + correlation_coefficient))

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r[0] for r in results),
        "conjecture_holds": correlation_coefficient >= 0.8 and p_value <= 0.05,
        "counterexample": "" if correlation_coefficient >= 0.8 and p_value <= 0.05 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")