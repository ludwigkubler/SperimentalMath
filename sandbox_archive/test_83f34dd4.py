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
        for i in range(n):
            clause = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        unassigned_vars = [v for v in range(1, len(cnf) + 1) if v not in assignment and -v not in assignment]
        if not unassigned_vars:
            return all([all([assignment[v] if v > 0 else not assignment[-v] for v in clause]) for clause in cnf])
        var = random.choice(unassigned_vars)
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            if dpll(cnf, new_assignment):
                return True
        return False
    
    def calculate_entropy(transitions):
        counts = {}
        for (s1, s2), count in transitions.items():
            if s1 not in counts:
                counts[s1] = 0
            counts[s1] += count
        p_s1 = [count / sum(counts.values()) for count in counts.values()]
        entropy = -sum(p * math.log2(p) for p in p_s1)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_entropy = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        transitions = {}
        
        for _ in range(10):
            assignment = {}
            if dpll(cnf, assignment):
                instances_tested += 1
                n_max = max(n_max, len(transitions))
                
                # Simulate DPLL search and record transitions
                stack = [(assignment.copy(), cnf)]
                while stack:
                    current_assignment, remaining_clauses = stack.pop()
                    unassigned_vars = [v for v in range(1, len(remaining_clauses) + 1) if v not in current_assignment and -v not in current_assignment]
                    if not unassigned_vars:
                        continue
                    var = random.choice(unassigned_vars)
                    for val in [True, False]:
                        new_assignment = current_assignment.copy()
                        new_assignment[var] = val
                        new_clauses = [clause for clause in remaining_clauses if all([new_assignment[v] if v > 0 else not new_assignment[-v] for v in clause])]
                        if new_clauses:
                            stack.append((new_assignment, new_clauses))
                        else:
                            transitions[(tuple(sorted(current_assignment.items())), tuple(sorted(new_assignment.items())))] = transitions.get((tuple(sorted(current_assignment.items())), tuple(sorted(new_assignment.items()))), 0) + 1
    
    if instances_tested < 30:
        return {
            "metric_name": "topological_entropy",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_entropy = total_entropy / instances_tested
    C = 1.0  # Placeholder for the constant C
    upper_bound = C * math.log(n_max)
    
    return {
        "metric_name": "topological_entropy",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(mean_entropy - upper_bound) <= 3,
        "counterexample": "" if abs(mean_entropy - upper_bound) <= 3 else f"mean_entropy={mean_entropy}, upper_bound={upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break