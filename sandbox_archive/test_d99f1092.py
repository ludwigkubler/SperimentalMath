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
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        pure_literal = next((l for l in range(1, len(assignment) + 2) if (l not in assignment and -l in assignment)), None)
        if pure_literal:
            new_assignment[pure_literal] = True
            if dpll([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            return False
        literal = next(lit for lit in range(1, len(assignment) + 2) if lit not in assignment and -lit not in assignment)
        new_assignment[literal] = True
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        return False
    
    def minimal_rank(cnf):
        n = len(cnf)
        rank = 0
        while cnf:
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                cnf = [c for c in cnf if literal not in c and -literal not in c]
            else:
                literal = random.choice(range(1, n + 1))
                new_cnf = []
                for clause in cnf:
                    if literal in clause:
                        continue
                    elif -literal in clause:
                        new_clause = [l for l in clause if l != -literal]
                        if new_clause:
                            new_cnf.append(new_clause)
                    else:
                        new_cnf.append(clause)
                cnf = new_cnf
            rank += 1
        return rank
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2 * n):
            clause = random.sample(range(1, n + 1), k=3)
            cnf.append(clause)
        return cnf
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            rank = minimal_rank(cnf)
            s_phi = len(dpll(cnf, {}))
            if s_phi == 0:
                continue
            ratio = abs(Fraction(rank, s_phi) - 1)
            results.append({
                "n": n,
                "rank": rank,
                "s_phi": s_phi,
                "ratio": ratio
            })
    
    mean_ratio = sum(r["ratio"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if abs(r["ratio"] - 1) <= 0.2) / len(results)
    
    return {
        "metric_name": "Ratio of Minimal Rank to Circuit Size",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "Ratio outside tolerance"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio outside tolerance' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")