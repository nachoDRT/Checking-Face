import subprocess
import sys

package_name = sys.argv[-1]
subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
