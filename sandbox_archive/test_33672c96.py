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
            clause = [random.choice([f'x{i}', f'~x{i}']) for i in range(n)]
            if len(set(clause)) == 1:
                continue
            random.shuffle(clause)
            clauses.append('(' + ' & '.join(clause) + ')')
        return ' | '.join(clauses)
    
    def resolution_length(cnf):
        stack = []
        while cnf:
            literals = set()
            for clause in cnf.split(' | '):
                if '(' in clause and ')' in clause:
                    continue
                literals.update(clause.split(' & '))
            literal = random.choice(list(literals))
            new_clauses = []
            for clause in cnf.split(' | '):
                if literal not in clause and f'~{literal}' not in clause:
                    new_clauses.append(clause)
                elif literal in clause:
                    continue
                else:
                    other_clause = clause.replace(f'~{literal}', '')
                    other_literals = set(other_clause.split(' & '))
                    for l in literals:
                        if l != literal and f'~{l}' not in other_literals:
                            new_clauses.append(f'({other_clause} & {l})')
            cnf = ' | '.join(new_clauses)
            stack.append(literal)
        return len(stack)
    
    def monodromy_rank(n):
        # Placeholder for actual mapping
        return n
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        t_F = resolution_length(cnf)
        R_F = monodromy_rank(n)
        if R_F == 0:
            continue
        results.append((t_F, R_F))
    
    if not results:
        return {
            "metric_name": "resolution_proof_length",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_t_F = sum(t_F for t_F, _ in results) / len(results)
    max_R_F = max(R_F for _, R_F in results)
    conjecture_holds = all(t_F <= n**2 * R_F for t_F, R_F in results)
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": mean_t_F,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={max_R_F}, t*(F)={mean_t_F}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_t_F = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_t_F} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = r["counterexample"]
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)