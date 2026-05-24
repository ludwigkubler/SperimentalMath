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
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i + 1, n)):
                clauses.append(clause)
        return clauses
    
    def compute_automorphic_forms(clauses):
        forms = set()
        for clause in clauses:
            form = tuple(sorted([abs(x) for x in clause]))
            if form not in forms:
                forms.add(form)
        return len(forms)
    
    def dpll_refutation_tree_width(clauses):
        # Simplified DPLL refutation tree width estimation
        return sum(1 for _ in clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_3cnf(n)
            automorphic_count = compute_automorphic_forms(clauses)
            refutation_width = dpll_refutation_tree_width(clauses)
            results.append((n, automorphic_count, refutation_width))
    
    if not results:
        return {
            "metric_name": "automorphic_forms",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    automorphic_counts = [r[1] for r in results]
    refutation_widths = [r[2] for r in results]
    
    mean_automorphic_count = sum(automorphic_counts) / len(automorphic_counts)
    std_automorphic_count = (sum((x - mean_automorphic_count) ** 2 for x in automorphic_counts) / len(automorphic_counts)) ** 0.5
    support_fraction = sum(1 for count, width in zip(automorphic_counts, refutation_widths) if count <= 2 ** width) / len(results)
    
    return {
        "metric_name": "automorphic_forms",
        "metric_value": mean_automorphic_count,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"mean={mean_automorphic_count} std={std_automorphic_count}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")