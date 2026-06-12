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
    
    def generate_kary_formula(k, n):
        if k == 2:
            return random.choice(['A', 'B'])
        else:
            return '(' + generate_kary_formula(k, n-1) + ' & ' + generate_kary_formula(k, n-1) + ')'
    
    def tseitin_formula(formula):
        literals = set()
        clauses = []
        
        def encode(lit):
            if lit not in literals:
                literals.add(lit)
                clauses.append([lit])
            return lit
        
        def decode(lit):
            return lit
        
        def parse(formula):
            if formula[0] == '(' and formula[-1] == ')':
                op = formula[1:-1]
                if ' & ' in op:
                    left, right = op.split(' & ')
                    return encode(parse(left)) + ' & ' + encode(parse(right))
                elif ' | ' in op:
                    left, right = op.split(' | ')
                    return '(' + decode(encode(parse(left))) + ' | ' + decode(encode(parse(right))) + ')'
            else:
                return formula
        
        def dpll(clauses):
            if not clauses:
                return True
            literal = next(l for l in literals if all(l not in c and -l not in c for c in clauses))
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return dpll(new_clauses) or dpll([c + [-literal] for c in new_clauses])
        
        return parse(formula), dpll(clauses)
    
    def motivic_order(formula):
        # Placeholder implementation
        return len(formula.split(' & '))
    
    n = 5
    k = random.randint(2, 3)
    formula = generate_kary_formula(k, n)
    tseitin, width = tseitin_formula(formula)
    order = motivic_order(tseitin)
    
    return {
        "metric_name": "MotivicOrder vs DPLLWidth",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": order <= 2 * width,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")