import setuptools as st

packages = st.find_packages()

print(f"{packages = }")

st.setup(
    name="scontrol_parser",
    version="1.0",
    py_modules=packages,
)
