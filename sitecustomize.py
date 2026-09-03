# Temporary build-safety shim for GitHub Actions inline Python blocks.
# Makes the standard regex module available via builtins so a missed local import
# cannot abort the final multilingual deployment.
import builtins
import re

builtins.re = re
