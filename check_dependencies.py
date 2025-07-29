"""
Script to check if all required dependencies for the Schrödinger solver are installed.
"""

import sys
import importlib
import pkg_resources

def check_package(package_name, min_version=None):
    """
    Check if a package is installed and meets the minimum version requirement.
    
    Parameters
    ----------
    package_name : str
        Name of the package to check.
    min_version : str, optional
        Minimum version required. If None, only checks if the package is installed.
        
    Returns
    -------
    bool
        True if the package is installed and meets the version requirement, False otherwise.
    """
    try:
        # Try to import the package
        package = importlib.import_module(package_name)
        
        # Get the installed version
        try:
            installed_version = pkg_resources.get_distribution(package_name).version
        except pkg_resources.DistributionNotFound:
            # Some packages have different distribution names
            if package_name == "PIL":
                installed_version = pkg_resources.get_distribution("Pillow").version
            else:
                print(f"⚠️ Warning: Could not determine version for {package_name}")
                return True  # Package is importable but version can't be determined
        
        # Check version if required
        if min_version:
            if pkg_resources.parse_version(installed_version) < pkg_resources.parse_version(min_version):
                print(f"❌ {package_name} version {installed_version} is installed, but version {min_version} or higher is required")
                return False
            else:
                print(f"✅ {package_name} version {installed_version} is installed (minimum required: {min_version})")
                return True
        else:
            print(f"✅ {package_name} version {installed_version} is installed")
            return True
            
    except ImportError:
        print(f"❌ {package_name} is not installed")
        return False

def check_schrodinger_solver():
    """
    Check if the schrodinger_solver package is properly installed.
    
    Returns
    -------
    bool
        True if the package is installed and all modules can be imported, False otherwise.
    """
    try:
        # Try to import the main package
        import schrodinger_solver
        print(f"✅ schrodinger_solver package is installed")
        
        # Try to import specific modules
        modules_to_check = [
            "schrodinger_solver.core",
            "schrodinger_solver.potentials",
            "schrodinger_solver.solver_1d",
            "schrodinger_solver.solver_2d",
            "schrodinger_solver.main"
        ]
        
        all_modules_ok = True
        for module in modules_to_check:
            try:
                importlib.import_module(module)
                print(f"  ✅ {module} can be imported")
            except ImportError as e:
                print(f"  ❌ {module} cannot be imported: {str(e)}")
                all_modules_ok = False
        
        return all_modules_ok
    except ImportError:
        print(f"❌ schrodinger_solver package is not installed or not in the Python path")
        return False

def main():
    """
    Check all required dependencies for the Schrödinger solver.
    """
    print("Checking Python version...")
    python_version = sys.version.split()[0]
    if pkg_resources.parse_version(python_version) < pkg_resources.parse_version("3.8"):
        print(f"❌ Python version {python_version} is installed, but version 3.8 or higher is required")
    else:
        print(f"✅ Python version {python_version} is installed")
    
    print("\nChecking required packages...")
    required_packages = {
        "numpy": "1.23.0",
        "scipy": "1.9.0",
        "matplotlib": "3.6.0",
        "streamlit": "1.13.0",
        "PIL": "9.2.0"  # Pillow
    }
    
    all_packages_ok = True
    for package, min_version in required_packages.items():
        if not check_package(package, min_version):
            all_packages_ok = False
    
    print("\nChecking schrodinger_solver package...")
    schrodinger_solver_ok = check_schrodinger_solver()
    
    print("\nSummary:")
    if all_packages_ok and schrodinger_solver_ok:
        print("✅ All dependencies are correctly installed!")
        print("If you're still experiencing issues with the Streamlit app, please refer to TROUBLESHOOTING.md")
    else:
        print("❌ Some dependencies are missing or have incorrect versions.")
        print("Please install the required dependencies using:")
        print("pip install -r requirements.txt")
        print("\nFor more detailed troubleshooting, please refer to TROUBLESHOOTING.md")

if __name__ == "__main__":
    main()