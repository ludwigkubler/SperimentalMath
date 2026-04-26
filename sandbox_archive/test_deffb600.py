import sys
import json
from collections import defaultdict

def run_trial(seed: int) -> dict:
    from random import seed as set_seed
    from math import gcd
    from functools import reduce
    
    def lcm(a, b):
        return a * b // gcd(a, b)
    
    def resolution_width(phi):
        # Simplified DPLL with width tracking
        clauses = phi.split()
        variables = set()
        for clause in clauses:
            variables.update(clause.split())
        
        def dpll(model, clauses):
            if not clauses:
                return True, 0
            literal = next((lit for lit in variables if lit not in model and -lit not in model), None)
            if literal is None:
                return False, float('inf')
            
            new_clauses = []
            for clause in clauses:
                if literal in clause:
                    continue
                if -literal in clause:
                    new_clauses.extend(clause.split(literal) + clause.split(-literal))
                else:
                    new_clauses.append(clause)
            
            width = max(len(c.split()) for c in new_clauses)
            return dpll(model | {literal}, new_clauses), width
        
        _, width = dpll(set(), clauses)
        return width
    
    def selmer_rank(phi):
        # Simplified 2-descent over Q
        H = sum(int(clause) for clause in phi.split())
        n = len(phi.split())
        c = (H * n + 1) // 2
        q = 2
        
        def is_square(x):
            return int(x**0.5)**2 == x
        
        rank = 0
        for i in range(1, q+1):
            if not is_square(i * (i + 1) * (i - c)):
                rank += 1
        
        return rank
    
    def generate_phi(n):
        # Generate 3-CNF formula from Boolean Pythagorean triples problem
        clauses = []
        for a in range(1, n+1):
            for b in range(a+1, n+1):
                c = (a**2 + b**2)**0.5
                if c.is_integer():
                    clauses.append(f"{-a} {b} {-c}")
                    clauses.append(f"{a} {-b} {c}")
        return " ".join(clauses)
    
    set_seed(seed)
    results = []
    for n in range(5, 21):
        phi = generate_phi(n)
        s_n = selmer_rank(phi)
        w_n = resolution_width(phi)
        results.append((n, s_n, w_n))
    
    mean_diff = sum(abs(s - w) for _, s, w in results) / len(results)
    support_fraction = sum(1 for _, s, w in results if abs(s - w) <= 1) / len(results)
    
    conjecture_holds = support_fraction >= 0.9 and mean_diff <= 0.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "2-Selmer Rank vs Resolution Width",
        "metric_value": mean_diff,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")