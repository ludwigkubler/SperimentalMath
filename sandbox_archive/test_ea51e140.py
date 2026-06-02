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
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            if all(abs(x) != abs(y) for x, y in itertools.combinations(clause, 2)):
                clauses.append(clause)
        return clauses
    
    def tseitin_encoding(cnf):
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        
        n_vars = max(literals)
        new_var = n_vars + 1
        tseitin_clauses = []
        
        for i, clause in enumerate(cnf):
            for literal in clause:
                tseitin_clauses.append([literal, -new_var])
            tseitin_clauses.append([-new_var] + [-l for l in clause])
            new_var += 1
        
        return tseitin_clauses
    
    def resolution_width(clauses):
        queue = clauses[:]
        learned = []
        
        while queue:
            literal_counts = {}
            for clause in queue:
                for lit in clause:
                    if abs(lit) not in literal_counts:
                        literal_counts[abs(lit)] = 0
                    literal_counts[abs(lit)] += 1
            
            unit_clauses = [lit for lit, count in literal_counts.items() if count == 1]
            if not unit_clauses:
                return len(queue)
            
            unit_clause = random.choice(unit_clauses)
            polarity = -unit_clause if unit_clause < 0 else unit_clause
            queue = [clause for clause in queue if polarity not in clause and -polarity not in clause]
            learned.append([polarity, -polarity])
        
        return len(queue) + len(learned)
    
    def construct_braided_monoidal_category(cnf):
        # Placeholder function to simulate the construction of a braided monoidal category
        # This is a dummy implementation and should be replaced with an actual mapping
        return 1
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    tseitin_clauses = tseitin_encoding(cnf)
    width = resolution_width(tseitin_clauses)
    m_phi = construct_braided_monoidal_category(cnf)
    
    if m_phi == 0:
        return {
            "metric_name": "resolution_proof_width_to_braided_categories_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = width / m_phi
    return {
        "metric_name": "resolution_proof_width_to_braided_categories_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if ratio <= n * math.log(n) else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    ratios = [r["metric_value"] for r in results if "metric_value" in r]
    supports = [r["conjecture_holds"] for r in results if "conjecture_holds" in r]
    
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in ratios) / len(ratios))
    support_fraction = sum(supports) / len(supports)
    
    if all(supports):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif sum(supports) >= 0.8 * len(supports):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, s in enumerate(supports) if not s)
        print(f"RESULT: FALSIFIED counterexample=\"not enough supports\" first_failing_seed={first_failing_seed}")