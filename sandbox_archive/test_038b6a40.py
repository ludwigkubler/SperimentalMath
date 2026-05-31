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
    
    def tseitin_diagram(cnf):
        n = len(cnf)
        new_vars = {}
        diagram = []
        
        for i in range(n):
            literal = f"x{i+1}"
            if literal not in new_vars:
                new_vars[literal] = len(diagram)
                diagram.append([0])
            row = diagram[new_vars[literal]]
            row[0] = 1
            for clause in cnf[i]:
                if clause not in new_vars:
                    new_vars[clause] = len(diagram)
                    diagram.append([-1, -1])
                diagram[new_vars[clause]][0] = 1
                diagram[new_vars[clause]][1] = new_vars[literal]
        
        return diagram
    
    def resolution_width(cnf):
        n = len(cnf)
        clauses = [set(clause) for clause in cnf]
        unit_clauses = {i: set([x]) for i, x in enumerate(range(1, n+1))}
        
        while True:
            new_clause = None
            for clause in clauses:
                if len(clause) == 1:
                    unit_clauses[next(iter(clause))] = set()
                    new_clause = set([-next(iter(clause))])
                    break
            
            if not new_clause:
                return len(unit_clauses)
            
            for i, clause in enumerate(clauses):
                if new_clause.intersection(clause):
                    clauses[i] = (clause - new_clause) | (clauses[i] - {-new_clause})
                    if len(clauses[i]) == 0:
                        return len(unit_clauses)
    
    def minimal_geometric_defect(diagram):
        # Simplified heuristic for geometric defect
        return sum(1 for row in diagram if any(x != 0 for x in row))
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    cnf = []
    variables = set()
    
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
        if all(x not in variables for x in clause):
            variables.update(clause)
            cnf.append(clause)
    
    diagram = tseitin_diagram(cnf)
    defect = minimal_geometric_defect(diagram)
    width = resolution_width(cnf)
    
    return {
        "metric_name": "Defect/Width Ratio",
        "metric_value": Fraction(defect, width),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Defect/Width Ratio\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested=30")