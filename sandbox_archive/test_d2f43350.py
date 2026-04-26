import random
import itertools
from collections import Counter

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n, m):
        variables = set(range(n))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(clauses):
        from itertools import product
        n = max(abs(x) for clause in clauses for x in clause)
        for assignment in product([-1, 1], repeat=n):
            if all(any(assignment[abs(x)-1] * x > 0 for x in clause) for clause in clauses):
                return True
        return False
    
    def toric_degeneration_volume(clauses):
        from sympy import symbols, groebner
        n = max(abs(x) for clause in clauses for x in clause)
        vars = symbols(f'x1:{n+1}')
        ideal = [sum(vars[i-1] for i in clause) - 1 for clause in clauses]
        gb = groebner(ideal, *vars, order='lex')
        return min([abs(gb.coeff(var)) for var in vars])
    
    def resolution_proof_size(clauses):
        from collections import defaultdict
        n = max(abs(x) for clause in clauses for x in clause)
        clauses_dict = defaultdict(list)
        for i, clause in enumerate(clauses):
            for literal in clause:
                clauses_dict[abs(literal)].append((i, literal))
        
        def dp(i, assignment):
            if i == len(clauses):
                return 0
            res_size = float('inf')
            for j, literal in clauses[i]:
                new_assignment = list(assignment)
                new_assignment[abs(literal)-1] *= -1
                if literal * new_assignment[abs(literal)-1] > 0:
                    res_size = min(res_size, dp(j+1, new_assignment) + 1)
            return res_size
        
        return dp(0, [1]*n)
    
    n = random.choice([5, 8, 11, 14])
    m = random.randint(n, n*3)
    clauses = generate_3cnf(n, m)
    satisfiable = is_satisfiable(clauses)
    V_min = toric_degeneration_volume(clauses)
    
    if satisfiable:
        res_size = None
    else:
        res_size = resolution_proof_size(clauses)
    
    metric_name = "resolution_proof_size"
    metric_value = res_size
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if not satisfiable and V_min > 0 and (res_size is None or res_size <= 100 * V_min):
        conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        support_fraction = sum(1 for res in results if res["metric_value"] > 0) / len(results)
        mean = sum(res["metric_value"] for res in results) / len(results)
        std = (sum((res["metric_value"] - mean)**2 for res in results) / len(results))**0.5
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(res["conjecture_holds"] and res["metric_value"] == 0 for res in results):
        first_failing_seed = next(seed for seed, res in enumerate(results) if res["conjecture_holds"] and res["metric_value"] == 0)
        print(f"RESULT: FALSIFIED counterexample=\"V_min=0\" first_failing_seed={first_failing_seed}")
    else:
        support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")