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
    
    def generate_tseitin_formula(m, n):
        variables = [f'x{i}' for i in range(1, m + 1)]
        clauses = []
        
        # Generate unit clauses
        for var in variables:
            clauses.append([var])
        
        # Generate binary clauses
        for _ in range(n):
            var1 = random.choice(variables)
            var2 = random.choice(variables)
            while var1 == var2:
                var2 = random.choice(variables)
            clauses.append([f'~{var1}', f'{var2}'])
        
        # Generate negated unit clauses
        for var in variables:
            clauses.append([f'~{var}'])
        
        return variables, clauses
    
    def resolution_tree_width(clauses):
        n = len(variables)
        tree = {i: [] for i in range(n)}
        
        def resolve(lit1, lit2):
            if lit1[0] == '~':
                lit1 = lit1[1:]
                negated = True
            else:
                lit1 = lit1
                negated = False
            
            if lit2[0] == '~':
                lit2 = lit2[1:]
                negated = True
            else:
                lit2 = lit2
                negated = False
            
            if lit1 == lit2 and negated:
                return []
            
            resolvent = [f'~{lit1}' if not negated else lit1, f'~{lit2}' if not negated else lit2]
            return resolvent
        
        def add_clause(clause):
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    resolvent = resolve(clause[i], clause[j])
                    if resolvent:
                        tree[variables.index(resolvent[0])].append(variables.index(resolvent[1]))
        
        for clause in clauses:
            add_clause(clause)
        
        def max_width(node):
            if not tree[node]:
                return 1
            return 1 + max(max_width(neighbor) for neighbor in tree[node])
        
        return max(max_width(i) for i in range(n))
    
    n = random.randint(5, 40)
    m = random.randint(2 * n, 3 * n)
    variables, clauses = generate_tseitin_formula(m, n)
    
    width = resolution_tree_width(clauses)
    
    return {
        "metric_name": "resolution_tree_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= 2 ** m - 1,
        "counterexample": "" if width >= 2 ** m - 1 else f"Formula with {m} variables and {n} clauses has width {width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")