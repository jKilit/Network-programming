import re


s = "123.415.23.58809"
print(re.findall(r"\d{3,5}", s))

j = "123.415.23.30933"
print(re.findall(r"[123]+", j))