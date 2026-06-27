import json
import sys
from pathlib import Path

# Add src folder to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from project_job_change.tools.custom_tool import MyCustomTool, PDFTextExtractorTool

def test_tool():
    tool = MyCustomTool()
    pdf_tool = PDFTextExtractorTool()
    print("--- Test Case 3: Instantiate PDF Text Extractor ---")
    print(f"PDF Tool name: {pdf_tool.name}")
    print(f"PDF Tool description: {pdf_tool.description}")
    
    workspace_root = Path("F:/project_job_change")

    
    # Mock JSON data
    mock_data = [
        {
            "company_division_name": "Division A",
            "product_name": "Product X",
            "opening_units": 100.0,
            "purchase_units": 50.0,
            "purchase_free": 5.0,
            "purchase_return": 10.0,
            "sales_units": 80.0,
            "sales_free": 2.0,
            "sales_return": 5.0,
            "closing_units": 73.0,
            "stock_code": "ST101",
            "from_date": "2026/01/01",
            "to_date": "2026/01/31",
            "ptr": 12.5,
            "formula": "=C2+D2"
        },
        {
            "company_division_name": "Division B",
            "product_name": "Product Y",
            "opening_units": 200.0,
            "purchase_units": 20.0,
            "purchase_free": 0.0,
            "purchase_return": 0.0,
            "sales_units": 150.0,
            "sales_free": 5.0,
            "sales_return": 10.0,
            "closing_units": 85.0,
            "stock_code": "ST102",
            "from_date": "2026/01/01",
            "to_date": "2026/01/31",
            "ptr": 15.0,
            "formula": ""
        }
    ]
    
    # Test case 1: With custom json_path
    print("--- Test Case 1: Custom JSON Path ---")
    json_name = "mock_output_custom.json"
    json_path_custom = workspace_root / json_name
    expected_output = workspace_root / "mock_output_custom.xlsx"
    
    with open(json_path_custom, "w") as f:
        json.dump(mock_data, f, indent=4)
    try:
        result = tool._run(json_path=str(json_path_custom), sheet_name="Custom Sales")
        print(result)
        if expected_output.exists():
            print(f"Success: Excel file created successfully at {expected_output}!")
            expected_output.unlink()
        else:
            print(f"Failure: Excel file was not created at {expected_output}.")
    finally:
        if json_path_custom.exists():
            json_path_custom.unlink()

    # Test case 2: With default parameters (no arguments passed)
    print("\n--- Test Case 2: Default Parameters ---")
    # Default is "data.json" -> resolved to F:/project_job_change/data.json
    json_path_default = workspace_root / "data.json"
    expected_output_default = workspace_root / "data.xlsx"
    
    with open(json_path_default, "w") as f:
        json.dump(mock_data, f, indent=4)
    try:
        result = tool._run()  # No arguments passed!
        print(result)
        if expected_output_default.exists():
            print(f"Success: Excel file created successfully at {expected_output_default}!")
            expected_output_default.unlink()
        else:
            print(f"Failure: Excel file was not created at {expected_output_default}.")
    finally:
        if json_path_default.exists():
            json_path_default.unlink()

if __name__ == "__main__":
    test_tool()



