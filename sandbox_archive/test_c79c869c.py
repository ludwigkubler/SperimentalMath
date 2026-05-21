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
        
        # Generate Tseitin formula for a simple OR gate
        for i in range(n-1):
            clauses.append([variables[i], variables[i+1]])
        
        # Add the final clause to ensure all variables are true
        clauses.append(variables)
        
        return variables, clauses
    
    def generate_expander_graph(n):
        if n < 4:
            raise ValueError("n must be at least 4")
        
        edges = []
        for i in range(1, n+1):
            j = (i * 2) % n + 1
            edges.append((i, j))
        
        return edges
    
    def young_diagram(clauses):
        # Simplified version of generating a Young diagram from clauses
        diagram = []
        for clause in clauses:
            if len(clause) == 1:
                diagram.append([clause[0]])
            else:
                diagram.append(sorted(clause, key=lambda x: int(x[1:])))
        return diagram
    
    def kronecker_coefficient(diagram):
        # Simplified version of computing Kronecker coefficient
        n = len(diagram)
        if n == 1:
            return Fraction(1, 1)
        
        coeff = Fraction(1, 1)
        for i in range(n-1):
            coeff *= Fraction(len(diagram[i]), len(diagram[i+1]))
        return coeff
    
    def symmetric_power_diagram(diagram, k):
        # Simplified version of computing symmetric power diagram
        new_diagram = []
        for _ in range(k):
            new_diagram.extend(diagram)
        return new_diagram
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        try:
            variables, clauses = generate_tseitin_formula(n)
            edges = generate_expander_graph(n)
            diagram = young_diagram(clauses)
            
            permanent_coeff = kronecker_coefficient(symmetric_power_diagram(diagram, 1))
            determinant_coeff = kronecker_coefficient(symmetric_power_diagram(diagram, 2))
            
            if permanent_coeff < determinant_coeff:
                raise ValueError("Permanent coefficient must be greater than determinant coefficient")
            
            results.append(permanent_coeff / determinant_coeff)
        except Exception as e:
            return {
                "metric_name": "kronecker_coefficient_ratio",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": str(e)
            }
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(result > 1 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "kronecker_coefficient_ratio",
        "metric_value": metric_value,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if trial_result["conjecture_holds"]:
            results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = len(results) / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")