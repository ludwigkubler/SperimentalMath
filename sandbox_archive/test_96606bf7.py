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
    
    def generate_circuit(n):
        if n == 1:
            return ['NOT', random.choice([0, 1])]
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            op = random.choice(['AND', 'OR'])
            return [op, left, right]
    
    def tseitin_formula(circuit):
        if isinstance(circuit[0], str):
            return circuit
        else:
            var = f'x{len(formulas)}'
            formulas.append([circuit[0], var, tseitin_formula(circuit[1])])
            formulas.append(['NOT', var, tseitin_formula(circuit[2])])
            return var
    
    def resolution_width(formula):
        clauses = formula
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    lit_i = clauses[i][0]
                    lit_j = clauses[j][0]
                    if lit_i == 'NOT' and lit_j[0] != 'NOT' and lit_i[1:] == lit_j:
                        new_clauses.extend([c for c in clauses if c[0] != lit_j])
                        break
                    elif lit_j == 'NOT' and lit_i[0] != 'NOT' and lit_j[1:] == lit_i:
                        new_clauses.extend([c for c in clauses if c[0] != lit_i])
                        break
                else:
                    continue
                break
            else:
                return len(clauses)
            clauses = new_clauses
    
    def simplicial_decomposition(formula):
        stack = [formula]
        cells = 0
        while stack:
            clause = stack.pop()
            if isinstance(clause[0], str):
                cells += 1
            else:
                for subclause in clause[1:]:
                    stack.append(subclause)
        return cells
    
    n_max = 40
    instances_tested = 0
    total_cells = 0
    total_widths = 0
    
    for n in range(5, n_max + 1):
        for _ in range(30 // (n - 4)):
            circuit = generate_circuit(n)
            formula = tseitin_formula(circuit)
            width = resolution_width(formula)
            cells = simplicial_decomposition(formula)
            total_cells += cells
            total_widths += width
            instances_tested += 1
    
    mean_cells = total_cells / instances_tested
    mean_widths = total_widths / instances_tested
    correlation_coefficient = (instances_tested * sum(c * w for c, w in zip(cells, widths)) - 
                               mean_cells * sum(widths) - 
                               mean_widths * sum(cells)) / math.sqrt(
                                   (instances_tested * sum(c**2 for c in cells) - mean_cells**2) *
                                   (instances_tested * sum(w**2 for w in widths) - mean_widths**2))
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else "Pearson's correlation coefficient < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Pearson's correlation coefficient < 0.8' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")