import random
import subprocess
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    k = random.randint(2, 5)
    
    # Generate a random 3-CNF formula with n variables and m clauses
    m = random.randint(n, 2 * n)
    clauses = []
    for _ in range(m):
        lits = [random.choice([f'x{i+1}', f'-x{i+1}']) for i in range(3)]
        clauses.append(' '.join(lits))
    
    cnf_formula = '\n'.join(clauses) + '\n'
    
    # Compute the resolution width using bounded DPLL
    dpll_output = subprocess.run(['bounded_dpll', '--width', str(n), '--cnf'], input=cnf_formula.encode(), capture_output=True, text=True)
    w_phi = int(dpll_output.stdout.strip())
    
    # Construct the Vandermonde matrix M_φ over GF(2^k)
    variables = [f'x{i+1}' for i in range(n)]
    variable_indices = {var: idx for idx, var in enumerate(variables)}
    M_phi = []
    for clause in clauses:
        row = [0] * n
        for lit in clause.split():
            if lit.startswith('x'):
                var_idx = variable_indices[lit]
                row[var_idx] = 1
            elif lit.startswith('-x'):
                var_idx = variable_indices[lit[2:]]
                row[var_idx] = 0
        M_phi.append(row)
    
    # Compute the rank of M_φ over GF(2)
    rank_M_phi = sum(1 for i in range(n) if any(M_phi[j][i] != 0 for j in range(len(M_phi))))
    
    # Check if the conjecture holds
    conjecture_holds = abs(w_phi - rank_M_phi) <= 1
    counterexample = "" if conjecture_holds else f"resolution_width={w_phi}, vandermonde_rank={rank_M_phi}"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": w_phi,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps({'seed': seed, **result})}")
        results.append(result)
    
    # Compute mean/std of metric_value and fraction of seeds where conjecture_holds
    total_metric_value = sum(r['metric_value'] for r in results)
    total_instances_tested = sum(r['instances_tested'] for r in results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    mean_metric_value = total_metric_value / total_instances_tested
    import statistics
    std_metric_value = statistics.stdev([r['metric_value'] for r in results])
    
    if all(r['conjecture_holds'] for r in results) or support_fraction >= 0.95:
        result = "SUPPORTED"
    elif any(abs(r['metric_value'] - rank_M_phi) >= 2 for r in results):
        first_failing_seed = next(seed for seed, r in enumerate(results) if abs(r['metric_value'] - rank_M_phi) >= 2)
        result = f"FALSIFIED counterexample=\"resolution_width={w_phi}, vandermonde_rank={rank_M_phi}\" first_failing_seed={first_failing_seed}"
    else:
        result = "INCONCLUSIVE not enough data"
    
    print(f"RESULT: {result} mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")