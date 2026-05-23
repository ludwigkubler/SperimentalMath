# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations, permutations
from fractions import Fraction

def generate_kcnf(n: int, k: int) -> list:
    variables = [f'x{i}' for i in range(1, n + 1)]
    clauses = []
    for _ in range(k):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [f'-{v}' for v in clause]
        clauses.append(clause)
    return clauses

def hypergeometric_rank(clause: list) -> int:
    rank = 0
    seen = set()
    for literal in clause:
        var = literal[1:] if literal.startswith('-') else literal
        if var not in seen:
            seen.add(var)
            rank += 1
    return rank

def resolution_length(clauses: list) -> int:
    assignment = {}
    variables = {var[1:] for var in set(lit for clause in clauses for lit in clause)}
    stack = [clauses]
    
    def dpll(formula, assignment, variables):
        if not formula:
            return True
        unassigned_var = next((v for v in variables if v not in assignment), None)
        if unassigned_var is None:
            return False
        
        true_branch = dpll([c for c in formula if any(lit.startswith(f'+{unassigned_var}') or lit == f'-{unassigned_var}' for lit in c)], {**assignment, unassigned_var: True}, variables)
        false_branch = dpll([c for c in formula if any(lit.startswith(f'+{unassigned_var}') or lit == f'-{unassigned_var}' for lit in c)], {**assignment, unassigned_var: False}, variables)
        
        return true_branch or false_branch
    
    while stack:
        current_clause = stack.pop()
        if not current_clause:
            continue
        unit_clause = next((c for c in current_clause if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            var = literal[1:] if literal.startswith('-') else literal
            assignment[var] = literal.startswith('+')
            stack.extend([c for c in current_clause if var not in c])
        else:
            literals = [lit for clause in current_clause for lit in clause]
            pairs = list(permutations(literals, 2))
            for pair in pairs:
                if pair[0].startswith('-') and pair[1] == f'+{pair[0][1:]}':
                    new_clause = [lit for lit in literals if lit not in pair]
                    stack.append(new_clause)
    
    return len(assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    k = 2 * n
    clauses = generate_kcnf(n, k)
    ranks = [hypergeometric_rank(clause) for clause in clauses]
    proof_lengths = [resolution_length(clauses) for _ in range(30)]
    
    if not all(ranks):
        return {
            "metric_name": "Hypergeometric Rank",
            "metric_value": sum(ranks) / len(ranks),
            "instances_tested": len(ranks),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = 0
    n_tests = min(len(proof_lengths), len(ranks))
    for i in range(n_tests):
        correlation += (proof_lengths[i] - sum(proof_lengths) / n_tests) * (ranks[i] - sum(ranks) / n_tests)
    correlation /= (n_tests * sum((x - sum(proof_lengths) / n_tests) ** 2 for x in proof_lengths) * sum((y - sum(ranks) / n_tests) ** 2 for y in ranks)) ** 0.5
    
    return {
        "metric_name": "Hypergeometric Rank",
        "metric_value": correlation,
        "instances_tested": n_tests,
        "conjecture_holds": correlation > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std_dev = (sum((r['metric_value'] - mean) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        counterexample = min((r['counterexample'] for r in results if not r['conjecture_holds']), default="")
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")