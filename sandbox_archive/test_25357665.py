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
    
    def generate_formula(m):
        variables = set()
        clauses = []
        for _ in range(m):
            clause = []
            for _ in range(random.randint(1, 3)):
                var = f'x{random.randint(0, m)}'
                if var not in variables:
                    variables.add(var)
                clause.append(var)
            clauses.append(clause)
        return clauses
    
    def formal_concept_order(clauses):
        concepts = set()
        for clause in clauses:
            concept = tuple(sorted(clause))
            concepts.add(concept)
        return len(concepts)
    
    def resolution_proof_width(clauses):
        # Simplified DPLL-based solver to estimate width
        stack = []
        literals = set()
        for clause in clauses:
            literals.update(clause)
        
        def dpll():
            if not stack:
                return 1
            literal = next(iter(literals))
            pos_literal, neg_literal = f'+{literal}', f'-{literal}'
            if pos_literal in literals and neg_literal in literals:
                literals.remove(pos_literal)
                literals.remove(neg_literal)
                stack.append((pos_literal, neg_literal))
                return dpll()
            elif pos_literal in literals:
                literals.remove(pos_literal)
                stack.append(pos_literal)
                return dpll()
            else:
                literals.remove(neg_literal)
                stack.append(neg_literal)
                return dpll()
        
        width = 0
        for _ in range(10):  # Simplified sampling
            literals.clear()
            literals.update(clauses)
            width = max(width, len(stack))
        return width
    
    n_trials = 30
    m_values = [5, 10, 15, 20, 30, 40]
    total_m = 0
    total_w = 0
    
    for _ in range(n_trials):
        m = random.choice(m_values)
        clauses = generate_formula(m)
        m_val = formal_concept_order(clauses)
        w_val = resolution_proof_width(clauses)
        total_m += m_val
        total_w += w_val
    
    mean_m = Fraction(total_m, n_trials)
    mean_w = Fraction(total_w, n_trials)
    
    correlation_coefficient = (n_trials * sum(m_val * w_val for m_val, w_val in zip([mean_m] * n_trials, [mean_w] * n_trials)) -
                               total_m * total_w) / math.sqrt((n_trials * sum(m_val**2 for m_val in [mean_m] * n_trials) - total_m**2) *
                                                            (n_trials * sum(w_val**2 for w_val in [mean_w] * n_trials) - total_w**2))
    
    conjecture_holds = correlation_coefficient >= 0.9
    counterexample = "" if conjecture_holds else f"Correlation: {correlation_coefficient}"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": n_trials,
        "n_max": max(m_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation below threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")