from pathlib import Path
from typing import Type

from crewai.tools import BaseTool
from langchain_community.document_loaders import PyPDFLoader
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from pydantic import BaseModel, Field


class MyToolForexcelInputRow(BaseModel):
    """One row of data to write into the Excel sheet."""

    company_division_name: str = Field(..., description="Company division name")
    product_name: str = Field(default="", description="Product name")
    opening_units: float = Field(default=0, ge=0, description="Opening units")
    purchase_units: float = Field(default=0, ge=0, description="Purchase units")
    purchase_free: float = Field(default=0, ge=0, description="Purchase free units")
    purchase_return: float = Field(default=0, ge=0, description="Purchase return units")
    sales_units: float = Field(default=0, ge=0, description="Sales units")
    sales_free: float = Field(default=0, ge=0, description="Sales free units")
    sales_return: float = Field(default=0, ge=0, description="Sales return units")
    closing_units: float = Field(default=0, ge=0, description="Closing units")
    stock_code: str = Field(default="", description="Stock code")
    from_date: str = Field(default="", description="Start date in YYYY/MM/DD format")
    to_date: str = Field(default="", description="End date in YYYY/MM/DD format")
    ptr: float = Field(default=0, ge=0, description="PTR value")
    formula: str = Field(default="", description="Formula text")

class SaveToExcelInput(BaseModel):
    """Input schema for saving records directly to an Excel file."""

    records: list[dict] = Field(
        ...,
        description=(
            "List of records to write into Excel. Each record is a dict with keys: "
            "company_division_name, product_name, opening_units, purchase_units, "
            "purchase_free, purchase_return, sales_units, sales_free, sales_return, "
            "closing_units, stock_code, from_date, to_date, ptr, formula."
        ),
    )
    output_path: str = Field(
        default="F:/project_job_change/output.xlsx",
        description=(
            "Full path where the .xlsx file will be saved. "
            "Agent can choose any filename, e.g. 'F:/project_job_change/report.xlsx'."
        ),
    )
    sheet_name: str = Field(
        default="Sheet1",
        description="Worksheet name inside the workbook.",
    )


class MyCustomTool(BaseTool):
    name: str = "json_to_excel"
    description: str = (
        "Save a list of product/division records directly into an Excel (.xlsx) file. "
        "Pass the records as a list of dicts and an optional output_path for the file name. "
        "No JSON file required — the agent passes the data inline."
    )
    args_schema: Type[BaseModel] = SaveToExcelInput

    _columns = [
        "company_division_name",
        "product_name",
        "opening_units",
        "purchase_units",
        "purchase_free",
        "purchase_return",
        "sales_units",
        "sales_free",
        "sales_return",
        "closing_units",
        "stock_code",
        "from_date",
        "to_date",
        "ptr",
        "formula",
    ]

    def _run(
        self,
        records: list[dict],
        output_path: str = "F:/project_job_change/output.xlsx",
        sheet_name: str = "Sheet1",
    ) -> str:
        # Validate each row
        validated = []
        for i, item in enumerate(records):
            try:
                row = MyToolForexcelInputRow(**item)
                validated.append(row)
            except Exception as e:
                return f"Error validating record at index {i}: {e}"

        if not validated:
            return "Error: No valid records provided."

        # Create Excel workbook
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = sheet_name[:31]

        # Write column headers
        headers = [col.replace("_", " ").title() for col in self._columns]
        worksheet.append(headers)
        self._format_header(worksheet)

        # Write data rows
        for row in validated:
            worksheet.append([getattr(row, col) for col in self._columns])

        self._auto_size_columns(worksheet)

        # Save file
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            workbook.save(output_file)
        except Exception as e:
            return f"Error saving Excel file to {output_path}: {e}"

        return f"Excel file successfully saved at {output_file.resolve()} with {len(validated)} row(s)."

    @staticmethod
    def _format_header(worksheet) -> None:
        for cell in worksheet[1]:
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center")
        worksheet.freeze_panes = "A2"

    @staticmethod
    def _auto_size_columns(worksheet) -> None:
        for column_cells in worksheet.columns:
            column_letter = column_cells[0].column_letter
            max_length = 0
            for cell in column_cells:
                value = "" if cell.value is None else str(cell.value)
                max_length = max(max_length, len(value))
            worksheet.column_dimensions[column_letter].width = min(max_length + 2, 40)




class PDFExtractorInput(BaseModel):
    """Input schema for PDF text extraction."""

    pdf_path: str = Field(
        ...,
        description="Full or relative path to the PDF file to extract text from.",
    )


class PDFExtractorTool(BaseTool):
    name: str = "pdf_extractor"
    description: str = (
        "Extract plain text from a PDF file using LangChain's PyPDFLoader. "
        "Pass the path to the PDF file and receive the full extracted text page by page."
    )
    args_schema: Type[BaseModel] = PDFExtractorInput

    def _run(self, pdf_path: str) -> str:
        # Resolve paths
        file_path = Path(pdf_path)
        if not file_path.is_absolute():
            workspace_root = Path("F:/project_job_change")
            resolved_file = workspace_root / pdf_path
            if resolved_file.exists():
                file_path = resolved_file

        if not file_path.exists():
            return f"Error: PDF file does not exist at {pdf_path}."

        try:
            loader = PyPDFLoader(str(file_path))
            docs = loader.load()

            if not docs:
                return "The PDF is empty or does not contain extractable text."

            pages = []
            for i, doc in enumerate(docs):
                pages.append(f"--- Page {i + 1} ---\n{doc.page_content}")

            return "\n\n".join(pages)
        except Exception as e:
            return f"Error extracting text from PDF: {e}"





