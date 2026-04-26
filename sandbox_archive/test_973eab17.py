import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n: int, m: int):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i + 1, n)):
                clauses.append(clause)
        return clauses
    
    def clause_compatibility(c1, c2):
        return not any(lit in [-c2_i, c2_i] for lit in c1 for c2_i in c2)
    
    def simplicial_complex_edges(clauses):
        edges = []
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                if clause_compatibility(clauses[i], clauses[j]):
                    edges.append((i, j))
        return edges
    
    def dpll(formula):
        def solve(model):
            if not formula:
                return True
            literal = next(lit for lit in range(1, n + 1) if lit not in model and -lit not in model)
            pos_literal = literal
            neg_literal = -literal
            if any(pos_literal in clause or neg_literal in clause for clause in formula):
                if solve(model | {pos_literal}):
                    return True
                elif solve(model | {neg_literal}):
                    return True
            return False
        
        return solve(set())
    
    def simplicial_complex_category(edges, n):
        # Naive implementation of Lusternik-Schnirelmann category via minimal coverings
        if not edges:
            return 0
        vertices = set(range(len(edges)))
        coverings = []
        for i in range(1, len(vertices) + 1):
            for subset in itertools.combinations(vertices, i):
                if all(any((u, v) in edges or (v, u) in edges for u in subset) for v in vertices - set(subset)):
                    coverings.append(subset)
        return min(len(covering) for covering in coverings)
    
    n = random.randint(5, 14)
    m = random.randint(n * 2, n * 3)
    clauses = generate_3cnf(n, m)
    edges = simplicial_complex_edges(clauses)
    category = simplicial_complex_category(edges, len(clauses))
    
    decision_tree_depth = dpll(clauses)
    
    return {
        "metric_name": "decision_tree_depth",
        "metric_value": decision_tree_depth,
        "instances_tested": 1,
        "conjecture_holds": decision_tree_depth <= category,
        "counterexample": "" if decision_tree_depth <= category else f"n={n}, m={m}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_depth = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")