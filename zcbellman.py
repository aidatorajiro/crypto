# bellman lib wrapper for Python.
# To run this script:
#  1. clone bellman, ff, group, pairing from https://github.com/zkcrypto/bellman to the same directory
#  2. add following to bellman library's Cargo.toml
#     [lib]
#     crate-type = ["dylib"]
#  3. compile bellman library
#  4. copy bellman/target/debug/libbellman.dylib (MacOS) or
#          bellman/target/debug/libbellman.so (Linux) to the current directory

import ctypes
import os
import subprocess
import re

if os.path.exists("./libbellman.dylib"):
    libpath = "./libbellman.dylib"
elif os.path.exists("./libbellman.so"):
    libpath = "./libbellman.so"
else:
    raise Exception("libbellman not found")

lib = ctypes.cdll.LoadLibrary(libpath)

nm_result = subprocess.run(["nm", libpath], capture_output=True).stdout.decode()

def call(*args):
    sep = "[^\$\n]+"
    match_func = sep + sep.join(args) + sep
    match_result = re.search("^[0-9a-f]+ . _(" + match_func + ")$",
        nm_result, flags=re.MULTILINE)
    
    if match_result == None:
        return None
    
    return getattr(lib, match_result[1])

# example code
if __name__ == "__main__":
    call("bellman", "gadgets", "sha256")()


