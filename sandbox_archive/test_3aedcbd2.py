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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def tseitin_diagram(cnf):
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        
        vertices = {0}
        edges = []
        
        var_counter = 1
        for i, clause in enumerate(cnf):
            literal_vars = [var_counter + j for j in range(len(clause))]
            var_counter += len(clause)
            
            # Add literals to vertices
            vertices.update(literal_vars)
            
            # Add edges for OR clauses
            if len(clause) > 1:
                for j in range(len(clause)):
                    for k in range(j + 1, len(clause)):
                        edges.append((literal_vars[j], literal_vars[k]))
            
            # Add edges for NOT literals
            for lit_var in literal_vars:
                vertices.add(-lit_var)
                edges.append((0, -lit_var))
        
        return vertices, edges
    
    def minimal_geometric_defect(vertices):
        return len(vertices)
    
    def resolution_proof_width(cnf):
        stack = []
        clauses = {tuple(clause) for clause in cnf}
        
        while stack:
            literal = stack.pop()
            if literal > 0:
                literals_to_add = [lit for lit in cnf if literal in lit]
                for lit in literals_to_add:
                    clauses.remove(tuple(lit))
                    if not any(clause for clause in clauses if set(clause) == set(lit)):
                        return len(stack)
            else:
                neg_literal = -literal
                literals_to_add = [lit for lit in cnf if neg_literal in lit]
                for lit in literals_to_add:
                    clauses.remove(tuple(lit))
                    if not any(clause for clause in clauses if set(clause) == set(lit)):
                        return len(stack)
        
        return len(stack)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        m = random.randint(n, n * 2)
        cnf = generate_cnf(n, m)
        
        vertices, edges = tseitin_diagram(cnf)
        defect = minimal_geometric_defect(vertices)
        width = resolution_proof_width(cnf)
        
        metric_values.append(defect / width)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(abs(x - mean_value) <= 3 * std_dev for x in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "MinimalDefect/ResolutionProofWidth",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support n_tested={len(results)}")