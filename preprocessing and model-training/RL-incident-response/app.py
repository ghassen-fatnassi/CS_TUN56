from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import concurrent.futures
from pathlib import Path
import logging

# Import your existing functions and modules
from policy_eval import different_graphs

app = FastAPI()

# Set up logging for better debugging
logging.basicConfig(level=logging.INFO)

@app.post("/run-simulation/")
def run_simulation(red_agent: str):
    # Validate the red agent parameter
    if red_agent not in ["meander", "b_line"]:
        raise HTTPException(status_code=400, detail="Invalid red agent. Choose 'meander' or 'b_line'.")

    # Define the output CSV file
    output_csv = "actions_list.csv"

    # This function will execute the different_graphs function and generate the CSV file
    def generate_csv(red_agent):
        logging.info(f"Starting CSV generation for {red_agent}...")
        different_graphs(red_agent)
        logging.info(f"CSV generation for {red_agent} completed.")

    # Run the CSV generation in a separate thread to avoid blocking
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Execute the function and wait for it to finish
        future = executor.submit(generate_csv, red_agent)
        future.result()  # Wait for the result

    # After the CSV is generated, return it as a response
    if Path(output_csv).exists():
        logging.info(f"CSV file {output_csv} exists, sending file...")
        response = FileResponse(output_csv, media_type='text/csv', filename=output_csv)
        
        # Empty the CSV file after sending the response
        with open(output_csv, 'w', newline='', encoding='utf-8') as file:
            pass  # Just open and close the file to clear its contents
        
        return response
    else:
        logging.error(f"CSV file {output_csv} not found after generation attempt.")
        raise HTTPException(status_code=500, detail="Error generating the CSV file.")
