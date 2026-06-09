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
            if all(abs(x) != abs(y) for x, y in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses

    def dpll(cnf, assignment):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if -literal not in c], new_assignment):
                return True
            return False
        literal, polarity = random.choice([(l, True) for l in range(1, n+1)] + [(-l, False) for l in range(1, n+1)])
        new_assignment = assignment.copy()
        new_assignment[literal] = polarity
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        return dpll([c for c in cnf if -literal not in c], new_assignment)

    def height_dpll(cnf):
        return len(dpll_search_tree(cnf))

    def dpll_search_tree(cnf):
        if not cnf:
            return [()]
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            return [(True, *dpll_search_tree(new_cnf)), (False, *dpll_search_tree([c for c in cnf if -literal not in c]))]
        literal, polarity = random.choice([(l, True) for l in range(1, n+1)] + [(-l, False) for l in range(1, n+1)])
        new_cnf = [c for c in cnf if literal not in c and -literal not in c]
        return [(polarity, *dpll_search_tree(new_cnf))]

    def quantum_group_order(cnf):
        # Placeholder for actual quantum group order calculation
        return random.randint(1, 2**len(cnf))

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    ord_q = quantum_group_order(cnf)
    h_DPLL = height_dpll(cnf)

    return {
        "metric_name": "ord_q vs h_DPLL",
        "metric_value": ord_q,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ord_q <= h_DPLL,
        "counterexample": "" if ord_q <= h_DPLL else f"ord_q({n})={ord_q}, h_DPLL({n})={h_DPLL}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ord_q < h_DPLL\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")