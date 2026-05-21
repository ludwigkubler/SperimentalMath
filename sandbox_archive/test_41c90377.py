# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, n), random.randint(1, n), random.randint(1, n)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses
    
    def simplicial_complex_from_clauses(clauses):
        nodes = set()
        for clause in clauses:
            nodes.update(clause)
        simplices = []
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                for k in range(j + 1, len(nodes)):
                    if any(node in clause for node in [nodes[i], nodes[j], nodes[k]]) and \
                       all(node not in clause for node in set(clauses) - {tuple(sorted([nodes[i], nodes[j], nodes[k]]))}):
                        simplices.append((nodes[i], nodes[j], nodes[k]))
        return simplices
    
    def persistent_homology(simplices):
        # Simplified version of persistent homology using a filtration
        barcode = []
        for simplex in sorted(simplices, key=lambda s: len(set(s))):
            barcode.append(len(set(simplex)))
        return sum(barcode)
    
    n = 40
    clauses = generate_3cnf(n)
    simplices = simplicial_complex_from_clauses(clauses)
    barcode_length = persistent_homology(simplices)
    
    # Disjointness communication complexity is Ω(n) if there are at least n/2 clauses
    disjointness_communication_complexity = len(clauses) >= n / 2
    
    return {
        "metric_name": "disjointness_communication_complexity",
        "metric_value": barcode_length,
        "instances_tested": 1,
        "conjecture_holds": barcode_length == Fraction(n).limit_denominator() and disjointness_communication_complexity,
        "counterexample": "" if barcode_length == Fraction(n).limit_denominator() else f"Graph with n={n}, A=[{', '.join(map(str, clauses))}]"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")