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
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(clause[i] == -clause[j] for i in range(n) for j in range(i+1, n)):
                continue
            clauses.append(clause)
        return clauses

    def dpll(cnf):
        def search(assignment):
            unsatisfied = [c for c in cnf if not any(l in assignment or -l in assignment for l in c)]
            if not unsatisfied:
                return True, assignment
            literal = next((l for c in unsatisfied for l in c if l > 0), None)
            if literal is None:
                return False, {}
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            result, _ = search(new_assignment)
            if result:
                return True, new_assignment
            new_assignment[literal] = False
            result, _ = search(new_assignment)
            return result, new_assignment
        _, satisfying_assignments = search({})
        return len(satisfying_assignments)

    def topological_entropy(cnf):
        n = len(cnf[0])
        transitions = [[0] * (2**n) for _ in range(2**n)]
        for assignment in range(2**n):
            for literal in range(n):
                next_assignment = assignment ^ (1 << literal)
                if any(l in cnf[next_assignment] or -l in cnf[next_assignment] for l in cnf[assignment]):
                    transitions[assignment][next_assignment] += 1
        total_transitions = sum(sum(row) for row in transitions)
        entropy = 0
        for i in range(2**n):
            if any(transitions[i][j] > 0 for j in range(2**n)):
                p_i = sum(transitions[i]) / total_transitions
                entropy -= p_i * math.log2(p_i)
        return entropy

    n_values = [5, 10, 15, 20, 30, 40]
    entropies = []
    diameters = []

    for n in n_values:
        cnf = generate_cnf(n)
        entropy = topological_entropy(cnf)
        diameter = dpll(cnf)
        entropies.append(entropy)
        diameters.append(diameter)

    correlation_coefficient = sum((entropies[i] - mean_entropies) * (diameters[i] - mean_diameters) for i in range(len(n_values))) / len(n_values)
    mean_entropies = sum(entropies) / len(entropies)
    mean_diameters = sum(diameters) / len(diameters)

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={r['seed']}")
                break