import yaml
from yaml.loader import SafeLoader
import pandas as pd
import time 

# New Dictionary for selected parameters from Checks
parsed_checks = dict()

# Specify path to ComplianceCheckResult file
path_to_OpenShift_Audit_File = "/add/path/to/file/here/Complianceresultcheck.yaml"

# Open the YAML file and load the YAML file
with open(path_to_OpenShift_Audit_File) as f:
    data = list(yaml.load_all(f, Loader=SafeLoader))


    # Counting total Checks
    numberOfChecks = len(data[0]["items"])   

    number = 0

    while number < numberOfChecks:
        parsed_checks.update({number: [
            data[0]["items"][number]["id"].upper(),
            data[0]["items"][number]["description"],
            data[0]["items"][number]["severity"],
            data[0]["items"][number]["status"]]})
        number = number + 1

# Columns Creation
df = pd.DataFrame([v for k, v in parsed_checks.items()], columns =['Name', 'Description', 'Severity', 'Status'])

# Setting sort by value order
df['Severity'] = pd.Categorical(df['Severity'], ['high', 'medium', 'low'])

# Changing data_frames order from high to low
df = df.sort_values('Severity')

# Filtering out only the hardening values that have registry keys & values
df_pass = df[df['Status'].str.contains("PASS")]
df_fail = df[df['Status'].str.contains("FAIL")]

df = df_pass.merge(right=df_fail, how='outer')

# print(df)

# Write to CSV file
df.to_csv('output.csv')
