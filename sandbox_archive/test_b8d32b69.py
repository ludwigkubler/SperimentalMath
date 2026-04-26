# auto-injected by SEC sandbox
import itertools
import collections
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
import sys
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def walsh_hadamard_transform(f, n):
        if n == 1:
            return f
        even = walsh_hadamard_transform([f[i] for i in range(0, len(f), 2)], n // 2)
        odd = walsh_hadamard_transform([f[i] for i in range(1, len(f), 2)], n // 2)
        result = [0] * n
        for k in range(n // 2):
            result[k] = even[k] + odd[k]
            result[k + n // 2] = even[k] - odd[k]
        return result
    
    def fourier_transform(f, n):
        f_hat = walsh_hadamard_transform(f, n)
        for k in range(n):
            f_hat[k] /= math.sqrt(n)
        return f_hat
    
    def g_F(x, clauses):
        return sum(2 * any(lit == x[i] for i, lit in enumerate(clause)) - 1 for clause in clauses) % 2
    
    def dpll(F, assignment, literals):
        if not F:
            return True
        unit_clause = next((c for c in F if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal in assignment and assignment[literal] != literal:
                return False
            assignment[literal] = literal
            literals.remove(literal)
            F = [c for c in F if literal not in c and -literal not in c]
            return dpll(F, assignment, literals)
        pure_literal = next((l for l in literals if all(l not in clause or -l in clause for clause in F)), None)
        if pure_literal:
            if pure_literal in assignment and assignment[pure_literal] != pure_literal:
                return False
            assignment[pure_literal] = pure_literal
            literals.remove(pure_literal)
            F = [c for c in F if pure_literal not in c and -pure_literal not in c]
            return dpll(F, assignment, literals)
        literal = literals[0]
        assignment[literal] = literal
        literals.remove(literal)
        F_true = [c for c in F if literal not in c and -literal not in c]
        F_false = [c for c in F if literal in c or -literal in c]
        return dpll(F_true, assignment.copy(), literals) or dpll(F_false, assignment.copy(), literals)
    
    def count_leaves(F):
        assignment = {}
        literals = list(range(len(F[0])))
        return sum(1 for _ in range(2 ** len(literals)) if dpll(F, assignment.copy(), literals))
    
    n_values = [10, 12, 14, 16, 18, 20]
    alpha_values = [3.0, 4.0, 4.267, 5.0]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for alpha in alpha_values:
            F = []
            for _ in range(int(alpha * n / 3)):
                clause = random.sample([-1, 1], n)
                F.append(clause)
            g_F_values = [g_F(x, F) for x in product([-1, 1], repeat=n)]
            f_hat = fourier_transform(g_F_values, 2 ** n)
            I_g_F = sum(abs(f_hat[k]) ** 2 * k for k in range(1, len(f_hat))) / (2 ** n)
            L_F = count_leaves(F)
            if not (2 ** (I_g_F / 3 - 1) <= L_F <= 2 ** (I_g_F + math.log2(n + 1))):
                conjecture_holds = False
                counterexample += f"n={n}, alpha={alpha}: L(F)={L_F}, I[g_F]={I_g_F}\n"
            instances_tested += 1
    
    return {
        "metric_name": "log2(L(F)) vs. I[g_F]",
        "metric_value": math.log2(L_F),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction == 1.0:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED (partial) mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")