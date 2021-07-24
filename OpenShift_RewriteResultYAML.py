# Run with at least Python 3.8
import yaml
from yaml.loader import SafeLoader
import pandas as pd


def compliance_check_result_parse(input_file: str, output_file: str):
    
    # New Dictionary for selected parameters from Checks
    parsed_checks = dict()
       
    # Open the YAML file and load the YAML file
    with open(input_file) as f:
        data = list(yaml.load_all(f, Loader=SafeLoader))
    
        # Counting total Checks
        number_of_checks = len(data[0]["items"])
    
        number = 0
    
        # Walrus :)
        while (number := number + 1) < number_of_checks:
            parsed_checks.update({number: [
                data[0]["items"][number]["id"].upper()[34:],  # Cutting portion of a name that is not relevant
                data[0]["items"][number]["description"],
                data[0]["items"][number]["severity"],
                data[0]["items"][number]["status"]]})
    
    # Creating DataFrame and Filling it out with parsed data
    # Columns Creation
    df = pd.DataFrame([v for k, v in parsed_checks.items()], columns=['Name', 'Description', 'Severity', 'Status'])
    
    # Setting sort by value order
    df['Severity'] = pd.Categorical(df['Severity'], ['high', 'medium', 'low'])
    
    # Changing data_frames order from high to low
    df = df.sort_values('Severity')
    
    # Filtering out only the hardening values that have registry keys & values
    df_pass = df[df['Status'].str.contains("PASS")]
    df_fail = df[df['Status'].str.contains("FAIL")]
    
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    
    # Write each DataFrame to a specific sheet
    df_pass.to_excel(writer, sheet_name='PASS')
    df_fail.to_excel(writer, sheet_name='FAIL')
    writer.save()


compliance_check_result_parse(
    input_file="path/to/input/compliancecheckresult.yaml", 
    output_file="path/to/input/compliancecheckresult_parsed.xlsx")
