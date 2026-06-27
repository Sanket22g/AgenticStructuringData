#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from project_job_change.crew import ProjectJobChange

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    Pass the path to the PDF file to process.
    """
    inputs = {
        'pdf_path': 'F:/project_job_change/pharma_stock.pdf'  # <-- update this to your PDF file path
    }   

    try:
        ProjectJobChange().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


