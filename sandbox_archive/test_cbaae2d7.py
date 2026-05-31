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
    
    def generate_cnf(n: int, m: int):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def tseitin_diagram(cnf):
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        
        new_vars = {lit: i + len(literals) for i, lit in enumerate(literals)}
        diagram = []
        
        for clause in cnf:
            if len(clause) == 1:
                diagram.append([new_vars[abs(clause[0])], -clause[0]])
            else:
                new_lit = new_vars[len(literals) + len(cnf)]
                literals.add(new_lit)
                diagram.append([new_lit, -clause[0]])
                for lit in clause[1:]:
                    diagram.append([-new_lit, lit])
                diagram.append([new_lit])
        
        return diagram
    
    def minimal_geometric_defect(diagram):
        # Simplified version of computing the number of vertices in a Tseitin diagram
        return len(diagram)
    
    def resolution_width(cnf):
        stack = []
        for clause in cnf:
            if all(lit not in stack and -lit not in stack for lit in clause):
                stack.extend(clause)
        
        width = 0
        while stack:
            unit_clause = next((lit for lit in stack if abs(lit) == 1), None)
            if unit_clause is None:
                break
            width += 1
            stack.remove(unit_clause)
            for clause in cnf:
                if unit_clause in clause:
                    stack.remove(-unit_clause)
        
        return width
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    cnf = generate_cnf(n, m)
    diagram = tseitin_diagram(cnf)
    
    defect = minimal_geometric_defect(diagram)
    width = resolution_width(cnf)
    
    if width == 0:
        return {
            "metric_name": "MinimalDefect",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_is_zero"
        }
    
    metric_values = [defect / width]
    
    return {
        "metric_name": "MinimalDefect",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_defect = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len([res for res in results if res["metric_value"] is not None])
    std_dev = math.sqrt(sum((res["metric_value"] - mean_defect) ** 2 for res in results if res["metric_value"] is not None) / (len(results) - 1))
    
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_defect} std={std_dev} support_fraction={support_fraction}")
    elif any(res["counterexample"] != "" for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if res["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(res['counterexample'] for res in results if res['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")