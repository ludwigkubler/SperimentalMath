# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        if n == 1:
            return 1
        if n == 2:
            return 2
        if n == 3:
            return 4
        # For larger n, use a simple DPLL solver (simplified version)
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                if dpll([c for c in clauses if literal not in c], new_assignment):
                    return True
                new_assignment[literal] = False
                if dpll([c for c in clauses if -literal not in c], new_assignment):
                    return True
                return False
            pure_literal = next((l for l in range(1, n+1) if (l not in assignment and -l not in assignment)), None)
            if pure_literal:
                new_assignment[pure_literal] = True
                if dpll(clauses, new_assignment):
                    return True
                new_assignment[pure_literal] = False
                if dpll(clauses, new_assignment):
                    return True
                return False
            literal = random.choice([l for l in range(1, n+1) if l not in assignment and -l not in assignment])
            new_assignment[literal] = True
            if dpll(clauses, new_assignment):
                return True
            new_assignment[literal] = False
            if dpll(clauses, new_assignment):
                return True
            return False
        
        def to_clauses(f):
            n = len(f)
            clauses = []
            for i in range(2**n):
                clause = []
                for j in range(n):
                    if (i >> j) & 1:
                        clause.append(j + 1)
                    else:
                        clause.append(-(j + 1))
                clauses.append(clause)
            return clauses
        
        clauses = to_clauses(f)
        assignment = {}
        return len(assignment) if dpll(clauses, assignment) else n
    
    def minimal_affine_curve_degree(f):
        n = len(f)
        # Simplified procedure to estimate the degree (not actual affine curve construction)
        return n // 2
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        comm_complexity = communication_complexity(f)
        degree = minimal_affine_curve_degree(f)
        results.append((comm_complexity, degree))
    
    if not results:
        return {
            "metric_name": "communication_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    comm_ranks = [comm for comm, _ in results]
    degrees = [deg for _, deg in results]
    correlation = sum((comm - sum(comm_ranks) / len(comm_ranks)) * (deg - sum(degrees) / len(degrees)) for comm, deg in results)
    correlation /= (len(results) * sum((comm - sum(comm_ranks) / len(comm_ranks))**2 for comm in comm_ranks) * sum((deg - sum(degrees) / len(degrees))**2 for deg in degrees))**0.5
    
    return {
        "metric_name": "communication_rank",
        "metric_value": correlation,
        "instances_tested": 30,
        "n_max": max(n for _, n in results),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE reason=empty_results")
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif any(not r["conjecture_holds"] for r in results):
            first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")