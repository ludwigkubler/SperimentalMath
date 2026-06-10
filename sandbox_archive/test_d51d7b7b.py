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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = {**assignment, abs(literal): literal > 0}
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                del new_assignment[abs(literal)]
        pure_literal = next((l for l in range(1, n + 1) if (l in assignment or -l in assignment) and (-l in assignment or l in assignment)), None)
        if pure_literal is not None:
            new_assignment[pure_literal] = True
            if dpll([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            else:
                del new_assignment[pure_literal]
        for literal in range(1, n + 1):
            if literal not in assignment and -literal not in assignment:
                if dpll(cnf, {**assignment, literal: True}):
                    return True
                if dpll(cnf, {**assignment, literal: False}):
                    return True
        return False
    
    def rank(group):
        generators = list(group)
        n = len(set([abs(x) for x in sum(generators, [])]))
        return n
    
    def algebraic_automorphism_group(cnf):
        # Simplified algorithm to find a generating set of the automorphism group
        variables = set(abs(lit) for clause in cnf for lit in clause)
        generators = []
        for var in variables:
            gen = [var, -var]
            if all(all((lit in gen or -lit in gen) == (other_lit in gen or -other_lit in gen) for other_clause in cnf for other_lit in other_clause) for clause in cnf):
                generators.append(gen)
        return set(generators)
    
    n_max = 40
    instances_tested = 30
    circuit_ranks = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = generate_cnf(n)
        group = algebraic_automorphism_group(cnf)
        r = rank(group)
        c = dpll(cnf)
        circuit_ranks.append((r, c))
    
    correlation_coefficient = sum((x[0] - mean_x) * (x[1] - mean_y) for x in circuit_ranks) / instances_tested
    mean_x = sum(x[0] for x in circuit_ranks) / instances_tested
    mean_y = sum(x[1] for x in circuit_ranks) / instances_tested
    
    support_fraction = len([x for x in circuit_ranks if x[0] * x[1] > 0]) / instances_tested
    
    conjecture_holds = support_fraction >= 0.8 and correlation_coefficient <= 3
    counterexample = "" if conjecture_holds else "correlation_coefficient"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    support_fractions = [r["conjecture_holds"] for r in results if "conjecture_holds" in r]
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(support_fractions) / len(support_fractions)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={seeds[next(i for i, x in enumerate(results) if not x['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")