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
    
    def generate_formula(n):
        clauses = []
        for _ in range(n):
            literals = [f"x{i}" if random.choice([True, False]) else f"~x{i}" for i in range(1, n+1)]
            clause = " & ".join(literals)
            clauses.append(clause)
        formula = " | ".join(clauses)
        return formula
    
    def compute_min_ents(formula):
        # Placeholder for actual computation
        # For simplicity, we'll assume a linear relationship here
        min_ents = [random.uniform(1, 5) for _ in range(n)]
        return min_ents
    
    def compute_entropy(clauses):
        entropy = sum(-len(clause.split(' & ')) * math.log2(len(clause.split(' & '))) for clause in clauses)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n)
        min_ents = compute_min_ents(formula)
        entropies = [compute_entropy(clause.split(' | ')) for clause in formula.split(' | ')]
        
        if len(min_ents) != len(entropies):
            return {
                "metric_name": "Pearson Correlation Coefficient",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "Mismatch in number of min_ents and entropies"
            }
        
        results.append({
            "min_ents": min_ents,
            "entropies": entropies
        })
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": None,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": False,
        "counterexample": "Not enough data to compute correlation"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.8 and all(abs(me - e) <= 3 for me, e in zip(result["min_ents"], result["entropies"]))) / len(results)
    else:
        support_fraction = None
    
    if support_fraction is not None and support_fraction >= 0.8:
        RESULT = "SUPPORTED"
    elif any("counterexample" in r and r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r)
        RESULT = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(r for r in results if 'counterexample' in r))]}"
    else:
        RESULT = "INCONCLUSIVE insufficient_data"
    
    print(RESULT)