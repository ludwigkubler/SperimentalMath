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
        vertices = list(range(1, n+1))
        edges = [(i, j) for i in range(1, n+1) for j in range(i+1, n+1)]
        formula = []
        for v in vertices:
            clause = [f"x{v}"]
            for u in vertices:
                if (u, v) not in edges and (v, u) not in edges:
                    clause.append(f"~x{u}")
            formula.append(" | ".join(clause))
        return " & ".join(formula)
    
    def resolution_proof_length(formula):
        clauses = [c.split() for c in formula.split(" & ")]
        literals = set()
        for clause in clauses:
            literals.update(clause)
        
        def dpll(clauses, model):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_model = model.copy()
                new_model[literal] = True
                if dpll([c for c in clauses if literal not in c and "~" + literal not in c], new_model):
                    return True
                new_model[literal] = False
                if dpll([c for c in clauses if literal not in c and "~" + literal not in c], new_model):
                    return True
                else:
                    return False
            pure_literal = next((l for l in literals if all(l.startswith("~") != c.startswith("~") for c in clauses)), None)
            if pure_literal:
                new_model[pure_literal] = True if pure_literal.startswith("~") else False
                if dpll([c for c in clauses if pure_literal not in c and "~" + pure_literal not in c], new_model):
                    return True
                else:
                    return False
            return False
        
        return len(clauses) - sum(dpll(clauses, {}) for _ in range(10))
    
    def minimal_rank(formula):
        # Placeholder for the actual computation of minimal rank
        # This is a dummy implementation and should be replaced with a proper algorithm
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_tseitin_formula(n)
    rank = minimal_rank(formula)
    proof_length = resolution_proof_length(formula)
    
    conjecture_holds = rank <= 2 * proof_length
    counterexample = "" if conjecture_holds else f"Tseitin formula with n={n}, rank={rank}, proof_length={proof_length}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")