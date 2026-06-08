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
        cnf = []
        for _ in range(2**n):
            clause = [random.randint(-1, 0) * (i + 1) for i in range(n)]
            if any(x == -y for x, y in zip(clause, clause[1:])):
                continue
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        def search(assignment, clauses):
            if not clauses:
                return True
            literal = find_pure_literal(clauses)
            if literal is not None:
                assignment[literal] = True
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                if search(assignment, new_clauses):
                    return True
                assignment[literal] = False
                new_clauses = [c for c in clauses if -literal not in c]
                if search(assignment, new_clauses):
                    return True
            else:
                literal = find_unit_clause(clauses)
                if literal is not None:
                    assignment[literal] = True
                    new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                    if search(assignment, new_clauses):
                        return True
                else:
                    literal = random.choice([l for l in range(1, n + 1) if l not in assignment])
                    assignment[literal] = True
                    new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                    if search(assignment, new_clauses):
                        return True
                    assignment[literal] = False
                    new_clauses = [c for c in clauses if -literal not in c]
                    if search(assignment, new_clauses):
                        return True
            return False
        
        def find_pure_literal(clauses):
            pure_literals = set()
            for clause in clauses:
                positive_lits = {x for x in clause if x > 0}
                negative_lits = {-x for x in clause if x < 0}
                pure_literals.update(positive_lits - negative_lits)
                pure_literals.update(negative_lits - positive_lits)
            return next(iter(pure_literals), None)
        
        def find_unit_clause(clauses):
            unit_clauses = [c for c in clauses if len(c) == 1]
            return next(iter(unit_clauses), None)
        
        assignment = {}
        return search(assignment, cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        proof_length = len(cnf) if dpll(cnf) else float('inf')
        results.append(proof_length)
    
    mean_proof_length = sum(results) / len(results)
    std_deviation = math.sqrt(sum((x - mean_proof_length)**2 for x in results) / len(results))
    
    return {
        "metric_name": "DPLL Proof Length",
        "metric_value": mean_proof_length,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": mean_proof_length >= 0.8 * n_values[-1],
        "counterexample": "" if mean_proof_length >= 0.8 * n_values[-1] else f"Mean proof length {mean_proof_length} is less than 0.8 * {n_values[-1]}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_msl = sum(results) / len(results)
    std_dev_msl = math.sqrt(sum((x - mean_msl)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.8 * n_values[-1]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_msl} std={std_dev_msl} support_fraction={support_fraction}")
    elif any(r < 0.8 * n_values[-1] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 0.8 * n_values[-1])
        print(f"RESULT: FALSIFIED counterexample='mean proof length less than 0.8 * {n_values[-1]}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")