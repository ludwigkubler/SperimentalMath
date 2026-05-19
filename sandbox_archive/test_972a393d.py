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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = []
            for _ in range(3):
                var = random.randint(1, n)
                polarity = random.choice(['x', '¬'])
                clause.append(f"{polarity}x{var}")
            cnf.append(" ∨ ".join(clause))
        return " ∧ ".join(cnf)
    
    def is_unsatisfiable(cnf):
        n = max(int(literal[2:]) if literal.startswith('x') else int(literal[3:]) for literal in cnf.replace(' ∨ ', ' ').replace(' ∧ ', ' ') if literal)
        clauses = cnf.split(" ∧ ")
        variables = set()
        for clause in clauses:
            literals = clause.split(" ∨ ")
            for literal in literals:
                var = int(literal[2:]) if literal.startswith('x') else int(literal[3:])
                variables.add(var)
        
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c.split(" ∨ ")) == 1), None)
            if unit_clause:
                literal = unit_clause.strip()
                polarity = 'x' if literal.startswith('x') else '¬'
                var = int(literal[2:]) if literal.startswith('x') else int(literal[3:])
                assignment[var] = polarity == 'x'
                return dpll([c for c in clauses if not (polarity + f"x{var}" in c or f"¬x{var}" in c)], assignment)
            pure_literal = next((l for l in variables if all(polarity + f"x{l}" in c or f"¬x{l}" in c for c in clauses) for polarity in ['x', '¬']), None)
            if pure_literal:
                polarity = 'x' if pure_literal.startswith('x') else '¬'
                var = int(pure_literal[2:]) if pure_literal.startswith('x') else int(pure_literal[3:])
                assignment[var] = polarity == 'x'
                return dpll([c for c in clauses if not (polarity + f"x{var}" in c or f"¬x{var}" in c)], assignment)
            literal = random.choice(clauses.split(" ∨ "))
            polarity = 'x' if literal.startswith('x') else '¬'
            var = int(literal[2:]) if literal.startswith('x') else int(literal[3:])
            assignment[var] = polarity == 'x'
            return dpll([c for c in clauses if not (polarity + f"x{var}" in c or f"¬x{var}" in c)], assignment)
        
        return not dpll(clauses, {})
    
    def walsh_transform(cnf):
        n = max(int(literal[2:]) if literal.startswith('x') else int(literal[3:]) for literal in cnf.replace(' ∨ ', ' ').replace(' ∧ ', ' ') if literal)
        clauses = cnf.split(" ∧ ")
        p_F = [0] * (1 << n)
        for clause in clauses:
            literals = clause.split(" ∨ ")
            for S in range(1, 1 << n):
                if all(literal[2:] if literal.startswith('x') else literal[3:] in bin(S)[2:].zfill(n) for literal in literals):
                    p_F[S] += (-1)**sum(int(literal[2:]) if literal.startswith('x') else int(literal[3:]) == i for literal in literals)
        return p_F
    
    def dpll_refutation_size(cnf):
        n = max(int(literal[2:]) if literal.startswith('x') else int(literal[3:]) for literal in cnf.replace(' ∨ ', ' ').replace(' ∧ ', ' ') if literal)
        clauses = cnf.split(" ∧ ")
        variables = set()
        for clause in clauses:
            literals = clause.split(" ∨ ")
            for literal in literals:
                var = int(literal[2:]) if literal.startswith('x') else int(literal[3:])
                variables.add(var)
        
        def dpll(clauses, assignment):
            if not clauses:
                return 0
            unit_clause = next((c for c in clauses if len(c.split(" ∨ ")) == 1), None)
            if unit_clause:
                literal = unit_clause.strip()
                polarity = 'x' if literal.startswith('x') else '¬'
                var = int(literal[2:]) if literal.startswith('x') else int(literal[3:])
                assignment[var] = polarity == 'x'
                return 1 + dpll([c for c in clauses if not (polarity + f"x{var}" in c or f"¬x{var}" in c)], assignment)
            pure_literal = next((l for l in variables if all(polarity + f"x{l}" in c or f"¬x{l}" in c for c in clauses) for polarity in ['x', '¬']), None)
            if pure_literal:
                polarity = 'x' if pure_literal.startswith('x') else '¬'
                var = int(pure_literal[2:]) if pure_literal.startswith('x') else int(pure_literal[3:])
                assignment[var] = polarity == 'x'
                return 1 + dpll([c for c in clauses if not (polarity + f"x{var}" in c or f"¬x{var}" in c)], assignment)
            literal = random.choice(clauses.split(" ∨ "))
            polarity = 'x' if literal.startswith('x') else '¬'
            var = int(literal[2:]) if literal.startswith('x') else int(literal[3:])
            assignment[var] = polarity == 'x'
            return 1 + dpll([c for c in clauses if not (polarity + f"x{var}" in c or f"¬x{var}" in c)], assignment)
        
        return dpll(clauses, {})
    
    def t_F(cnf):
        p_F = walsh_transform(cnf)
        n = max(int(literal[2:]) if literal.startswith('x') else int(literal[3:]) for literal in cnf.replace(' ∨ ', ' ').replace(' ∧ ', ' ') if literal)
        return sum(math.sqrt(sum(p_F[S] ** 2 for S in range(1 << n) if bin(S).count('1') == i)) for i in range(1, 4))
    
    def pearson_correlation(log_2_1_plus_t_F, T_F_over_sqrt_m):
        mean_log = sum(log_2_1_plus_t_F) / len(log_2_1_plus_t_F)
        mean_T = sum(T_F_over_sqrt_m) / len(T_F_over_sqrt_m)
        cov = sum((log_2_1_plus_t_F[i] - mean_log) * (T_F_over_sqrt_m[i] - mean_T) for i in range(len(log_2_1_plus_t_F))) / len(log_2_1_plus_t_F)
        var_log = sum((log_2_1_plus_t_F[i] - mean_log) ** 2 for i in range(len(log_2_1_plus_t_F))) / len(log_2_1_plus_t_F)
        var_T = sum((T_F_over_sqrt_m[i] - mean_T) ** 2 for i in range(len(T_F_over_sqrt_m))) / len(T_F_over_sqrt_m)
        return cov / (math.sqrt(var_log) * math.sqrt(var_T))
    
    n_values = [16, 20, 24, 28, 32]
    alpha_values = [4.0, 4.5, 5.0]
    results = []
    
    for n in n_values:
        for alpha in alpha_values:
            m = math.ceil(alpha * n)
            cnf = generate_cnf(n, m)
            if not is_unsatisfiable(cnf):
                continue
            
            T_F_val = t_F(cnf)
            B_F = dpll_refutation_size(cnf)
            log_2_1_plus_t_F = [math.log2(1 + B_F)]
            T_F_over_sqrt_m = [T_F_val / math.sqrt(m)]
            
            results.append({
                "n": n,
                "alpha": alpha,
                "m": m,
                "B_F": B_F,
                "log_2_1_plus_t_F": log_2_1_plus_t_F[0],
                "T_F_over_sqrt_m": T_F_over_sqrt_m[0]
            })
    
    if not results:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No unsatisfiable instances found"
        }
    
    log_2_1_plus_t_F = [r["log_2_1_plus_t_F"] for r in results]
    T_F_over_sqrt_m = [r["T_F_over_sqrt_m"] for r in results]
    correlation = pearson_correlation(log_2_1_plus_t_F, T_F_over_sqrt_m)
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": all(math.log2(1 + B_F) >= 0.1 * T_F_val / math.sqrt(m) for r in results),
        "counterexample": "" if all(math.log2(1 + B_F) >= 0.1 * T_F_val / math.sqrt(m) for r in results) else f"First failing instance: n={r['n']}, alpha={r['alpha']}, m={r['m']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
    
    results = []
    for n in [16, 20, 24, 28, 32]:
        for alpha in [4.0, 4.5, 5.0]:
            m = math.ceil(alpha * n)
            instances = sum(1 for r in results if r["n"] == n and r["alpha"] == alpha)
            if instances >= 30:
                correlation = pearson_correlation([r["log_2_1_plus_t_F"] for r in results if r["n"] == n and r["alpha"] == alpha], [r["T_F_over_sqrt_m"] for r in results if r["n"] == n and r["alpha"] == alpha])
                support_fraction = sum(1 for r in results if r["n"] == n and r["alpha"] == alpha and math.log2(1 + r["B_F"]) >= 0.1 * r["T_F_over_sqrt_m"] / math.sqrt(m)) / instances
                results.append({
                    "n": n,
                    "alpha": alpha,
                    "instances_tested": instances,
                    "conjecture_holds": support_fraction == 1,
                    "correlation": correlation,
                    "support_fraction": support_fraction
                })
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['correlation'] for r in results) / len(results)} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing = next(r for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={first_failing['n']}, alpha={first_failing['alpha']}, m={math.ceil(first_failing['alpha'] * first_failing['n'])}\" first_failing_seed=0")
    else:
        print("RESULT: INCONCLUSIVE no unsatisfiable instances found")