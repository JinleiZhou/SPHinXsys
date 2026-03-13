import os
import sys

def find_regression_test_base_dir(script_path):
    current_dir = os.path.dirname(os.path.abspath(script_path))
    while True:
        candidate = os.path.join(
            current_dir,
            "PythonScriptStore",
            "RegressionTest",
            "regression_test_base_tool.py",
        )
        if os.path.isfile(candidate):
            return os.path.dirname(candidate)
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            break
        current_dir = parent_dir
    raise ModuleNotFoundError(
        "Cannot find PythonScriptStore/RegressionTest/regression_test_base_tool.py "
        f"starting from {script_path}"
    )

path = find_regression_test_base_dir(__file__)
if path not in sys.path:
    sys.path.append(path)

from regression_test_base_tool import SphinxsysRegressionTest


case_name = "static_tire_center_deflection"
body_name = "TireObserver"
parameter_name = "Position"
converged = 0
number_of_run_times = 0
sphinxsys = SphinxsysRegressionTest(case_name, body_name, parameter_name)


# clean_input_folder(sphinxsys.input_file_path)

while True:
    print("Now start a new run......")
    sphinxsys.run_case()
    number_of_run_times += 1
    converged = sphinxsys.read_dat_file()
    print("Please note: This is the", number_of_run_times, "run!")

    if number_of_run_times <= 200:
        if converged == "true":
            print("Converged. Stop.")
            break
        elif converged != "true":
            print("Not converged, continue...")
            continue
    else:
        print("Too many runs, still not converged.")
        break

