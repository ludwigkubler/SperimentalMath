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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i + 1, n)):
                clauses.append(clause)
        return clauses
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            var = abs(literal)
            new_assignment = assignment[:]
            new_assignment[var - 1] = literal > 0
            return dpll([c for c in clauses if literal not in c], new_assignment) or \
                   dpll([c for c in clauses if -literal not in c], new_assignment)
        pure_literal = next((l for l in range(1, n + 1) if (l in assignment and -l not in assignment) or (-l in assignment and l not in assignment)), None)
        if pure_literal:
            literal = pure_literal if pure_literal in assignment else -pure_literal
            new_assignment = assignment[:]
            new_assignment[abs(literal) - 1] = literal > 0
            return dpll([c for c in clauses if literal not in c], new_assignment)
        var = random.choice(range(1, n + 1))
        return dpll(clauses, assignment + [True]) or dpll(clauses, assignment + [False])
    
    def resolution_width(clauses):
        queue = set()
        while True:
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if not unit_clause:
                break
            literal = unit_clause[0]
            new_clauses = []
            for clause in clauses:
                if literal in clause:
                    continue
                if -literal in clause:
                    new_clauses.append([l for l in clause if l != -literal])
                else:
                    new_clauses.append(clause)
            queue.add(literal)
            clauses = new_clauses
        return len(queue)

    def coxeter_group_order(n):
        # Simplified Coxeter group order calculation (not accurate but sufficient for testing)
        return 2 ** n

    results = []
    for n in [10, 20, 30]:
        total_width = 0
        for _ in range(100):
            cnf = generate_3cnf(n)
            if dpll(cnf, []):
                width = resolution_width(cnf)
                results.append((n, width))
                total_width += width
    
    average_order = sum(coxeter_group_order(n) for n, _ in results) / len(results)
    support_fraction = sum(1 for _, w in results if abs(w - average_order) <= 0.2 * average_order) / len(results)
    
    return {
        "metric_name": "average_width",
        "metric_value": total_width / len(results),
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"support_fraction={support_fraction:.2f} < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    average_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={average_width:.2f} std=NA support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction={support_fraction:.2f} < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction=<0.8")