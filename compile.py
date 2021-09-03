# import subprocess
# import sys

# # result = subprocess.run([sys.executable, "-c", "print('ocean')"])
# # result = subprocess.run([sys.executable, "-c", "print('ocean')"])
# # result = subprocess.run(["ls", "-l", "/Users/ben/projects/vegaswap"], capture_output=True, text=True)
# subprocess.run(["cd", "contracts-vy"])
# result = subprocess.run(["vyper", "Bucket.vy", "-o" ,"../build", "-f", "abi"], capture_output=True, text=True)
# # print("stdout:", result.stdout)
# # print("stderr:", result.stderr)

# print(type(result.stdout))
# i = 0
# for x in result.stdout.split("\n"):
#     print(i,x)
#     i+=1