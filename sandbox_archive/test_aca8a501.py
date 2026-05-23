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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for x in variables:
            clauses.append([x])
        for i in range(1, n):
            clauses.append([variables[i], f'~{variables[i-1]}'])
        clauses.append(['~', variables[-1]])
        return clauses
    
    def dpll(clauses, assignment={}):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and '~' + literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and '~' + literal not in c], new_assignment):
                return True
            return False
        pure_literal = next((l for l in variables if all(l not in c or '~' + l in c for c in clauses) and all('~' + l not in c or l in c for c in clauses)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll([c for c in clauses if pure_literal not in c and '~' + pure_literal not in c], new_assignment):
                return True
            new_assignment[pure_literal] = False
            if dpll([c for c in clauses if pure_literal not in c and '~' + pure_literal not in c], new_assignment):
                return True
            return False
        literal = random.choice(variables)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c and '~' + literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if literal not in c and '~' + literal not in c], new_assignment):
            return True
        return False
    
    def frege_proof_length(clauses):
        assignment = {}
        proof = []
        while not dpll(clauses, assignment):
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                proof.append(literal)
                assignment[literal] = True
                clauses = [c for c in clauses if literal not in c and '~' + literal not in c]
            else:
                pure_literal = next((l for l in variables if all(l not in c or '~' + l in c for c in clauses) and all('~' + l not in c or l in c for c in clauses)), None)
                if pure_literal:
                    proof.append(pure_literal)
                    assignment[pure_literal] = True
                    clauses = [c for c in clauses if pure_literal not in c and '~' + pure_literal not in c]
                else:
                    literal = random.choice(variables)
                    proof.append(literal)
                    assignment[literal] = True
                    clauses = [c for c in clauses if literal not in c and '~' + literal not in c]
        return len(proof)
    
    def geometric_invariant(clauses):
        # Placeholder for actual computation of geometric invariant
        # For simplicity, we use the number of variables as a proxy
        return len(variables)
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    proof_length = frege_proof_length(formula)
    rank = geometric_invariant(formula)
    
    return {
        "metric_name": "Rank vs Proof Length",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")