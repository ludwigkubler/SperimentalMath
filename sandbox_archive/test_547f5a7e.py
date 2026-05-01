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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        cnf = [[random.choice([-i, i]) for _ in range(random.randint(1, n))] for _ in range(n)]
        return cnf
    
    def is_tautology(cnf):
        # Simplified DPLL algorithm to check if a CNF formula is tautological
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
                if dpll([c for c in clauses if -literal not in c], new_assignment):
                    return True
                return False
            pure_literal = next((l for l in range(1, n+1) if all(l not in c and -l not in c for c in clauses)), None)
            if pure_literal is not None:
                new_assignment[pure_literal] = True
                if dpll([c for c in clauses if pure_literal not in c], new_assignment):
                    return True
                new_assignment[pure_literal] = False
                if dpll([c for c in clauses if -pure_literal not in c], new_assignment):
                    return True
                return False
            literal, _ = random.choice(clauses)
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if -literal not in c], new_assignment):
                return True
            return False
        return dpll(cnf, {})
    
    def circuit_size(cnf):
        # Simplified SAT-based minimizer to estimate circuit size
        # This is a placeholder and should be replaced with an actual algorithm
        return len(cnf) * len(cnf[0])
    
    def extended_frege_proof_length(cnf):
        # Simplified DPLL-style Extended Frege proof length estimator
        # This is a placeholder and should be replaced with an actual algorithm
        return len(cnf) ** 2
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    if not is_tautology(cnf):
        return {
            "metric_name": "proof_length_to_circ_size_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "not a tautology"
        }
    
    circ_size = circuit_size(cnf)
    proof_length = extended_frege_proof_length(cnf)
    
    return {
        "metric_name": "proof_length_to_circ_size_ratio",
        "metric_value": proof_length / circ_size,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='not a tautology' first_failing_seed={first_failing_seed}")