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
    
    def tseitin_formula(n):
        clauses = []
        for i in range(1, n+1):
            clauses.append((i,))
            for j in range(i+1, n+1):
                clauses.append((-i, -j))
                clauses.append((i, j))
        return clauses
    
    def min_diophantine_root_count(clauses):
        algebraic_numbers = set()
        for clause in clauses:
            for literal in clause:
                if literal > 0:
                    algebraic_numbers.add(literal)
                else:
                    algebraic_numbers.add(-literal)
        return len(algebraic_numbers)
    
    def dpll_solver(clauses, assignment={}):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            if literal < 0:
                literal = -literal
                if literal in assignment and assignment[literal]:
                    return False
                else:
                    assignment[literal] = True
            else:
                if literal in assignment and not assignment[literal]:
                    return False
                else:
                    assignment[literal] = False
        pure_literals = [l for l, count in collections.Counter([c[0] if c[0] > 0 else -c[0] for c in clauses]).items() if count % 2 == 1]
        if not pure_literals:
            literal = random.choice([l for l in range(1, len(clauses)+1) if l not in assignment])
        else:
            literal = pure_literals[0]
        return dpll_solver(clauses + [[-literal]], assignment) or dpll_solver(clauses + [[literal]], assignment)
    
    def proof_length(clauses):
        n = len(clauses)
        if n == 1:
            return 1
        return 2 * proof_length([c[1:] for c in clauses if c[0] < 0]) + 1
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = tseitin_formula(n)
            min_root_count = min_diophantine_root_count(formula)
            proof_len = proof_length(formula)
            results.append((min_root_count, proof_len))
    
    if not results:
        return {
            "metric_name": "MinRootCount vs ProofLength",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_root_counts = [r[0] for r in results]
    proof_lengths = [r[1] for r in results]
    
    mean_min_root_count = sum(min_root_counts) / len(min_root_counts)
    mean_proof_length = sum(proof_lengths) / len(proof_lengths)
    
    correlation_coefficient = sum((min_root_counts[i] - mean_min_root_count) * (proof_lengths[i] - mean_proof_length) for i in range(len(results))) / (len(results) * math.sqrt(sum((min_root_counts[i] - mean_min_root_count)**2 for i in range(len(results))) * sum((proof_lengths[i] - mean_proof_length)**2 for i in range(len(results)))))
    
    conjecture_holds = correlation_coefficient > 0.8 and all(min_root_count <= 2 * proof_len for min_root_count, proof_len in results)
    
    return {
        "metric_name": "MinRootCount vs ProofLength",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "correlation_coefficient < 0.8 or min_root_count > 2 * proof_length"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 9973) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] and "counterexample" not in r or r["counterexample"] == "" for r in results):
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
        result = f"RESULT: INCONCLUSIVE support_fraction={support_fraction}"
    
    print(result)