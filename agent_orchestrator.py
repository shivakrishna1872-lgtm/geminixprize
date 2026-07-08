
import json
import os
from datetime import datetime

# Import the Google Cloud AI Platform library.
# This is the core library for interacting with Vertex AI and Gemini models.
# The 'vertexai' library is the main entry point, and we use 'GenerativeModel'
# to access Gemini 1.5 Pro.
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part
except ImportError:
    print("Google Cloud AI Platform library not found.")
    print("Please install it using: pip install google-cloud-aiplatform")
    exit()

# --- AGENT ORCHESTRATION FRAMEWORK ---
# This script demonstrates a multi-agent system for a hackathon submission.
# The core idea is to show "autonomous operation" through a chain of specialized agents.
#
# Agent 1: The "Creative Agent"
#   - Responsibility: Generates a creative and compelling product description.
#   - Implementation: The first part of the 'generate_product_json' function.
#
# Agent 2: The "Structuring Agent"
#   - Responsibility: Takes unstructured text and converts it into a structured JSON
#     object that a machine can read (e.g., for an e-commerce API).
#   - Implementation: The second part of the 'generate_product_json' function,
#     where we instruct Gemini to return a JSON object.
#
# Agent 3: The "E-commerce Agent"
#   - Responsibility: Takes the structured JSON and interacts with an external service.
#   - Implementation: The 'push_to_shopify' function.
#
# This chained, modular design allows each agent to perform a specialized task,
# handing off its output to the next agent in the sequence. This is a foundational
# pattern for building more complex autonomous systems.

# --- Configuration ---
# It's a best practice to externalize configuration.
# For a real application, these would come from environment variables or a config file.
PROJECT_ID = os.environ.get("GCP_PROJECT")
LOCATION = os.environ.get("GCP_REGION", "us-central1")
MODEL_NAME = "gemini-1.5-pro-001"
LOG_FILE = "AGENT_LOGS.json"


def log_agent_activity(agent_name: str, reasoning: str, api_response: dict):
    """
    Logs the reasoning and API response of an agent to a file for audit purposes.

    This function is crucial for transparency and debugging in an autonomous system.
    By logging the "thoughts" (reasoning) and actions (API response) of each agent,
    we can trace the decision-making process.

    Args:
        agent_name: The name of the agent being logged.
        reasoning: A description of the agent's goal or "thought process".
        api_response: The JSON response received from the API call.
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent_name": agent_name,
        "reasoning": reasoning,
        "api_response": api_response,
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry, indent=2))
        f.write("
")


def generate_product_json(product_idea: str) -> dict:
    """
    Orchestrates the "Creative" and "Structuring" agents to generate a product JSON.

    This function first calls Gemini to brainstorm a creative product description (Agent 1),
    then makes a second call to structure that output into a clean JSON object (Agent 2).

    Args:
        product_idea: A simple theme or idea for the product (e.g., "retro-futuristic lamp").

    Returns:
        A dictionary containing the structured product data.
    """
    # --- Agent 1: Creative Agent ---
    creative_reasoning = f"Generate a detailed, compelling product description for the idea: '{product_idea}'."
    
    # Initialize Vertex AI. This should be done once per session.
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel(MODEL_NAME)

    # First call: Generate a creative description.
    creative_prompt = f"""
    You are a world-class copywriter for a trendy e-commerce store.
    Your task is to write a compelling, imaginative, and detailed product description
    for the following concept: '{product_idea}'.

    Make it exciting and desirable. Include a product title, a tagline, and a 2-paragraph description.
    """
    
    creative_response = model.generate_content([creative_prompt])
    creative_text = creative_response.text

    log_agent_activity(
        agent_name="Creative Agent",
        reasoning=creative_reasoning,
        api_response={"generated_text": creative_text},
    )

    # --- Agent 2: Structuring Agent ---
    structuring_reasoning = "Transform the creative text into a structured JSON for a Shopify-like API."
    
    # Second call: Convert the free-form text into a structured JSON.
    json_prompt = f"""
    You are a data transformation specialist. Your job is to convert unstructured product
    information into a strict JSON format. Do not add any extra text or explanations.
    Only output the JSON object.

    Use the following product description:
    ---
    {creative_text}
    ---

    Convert it into a JSON object with the following structure:
    - "product_title": string
    - "product_tagline": string
    - "description_html": string (formatted as HTML with paragraphs)
    - "category": string (infer a suitable category)
    - "price_usd": float (choose a reasonable price)
    - "tags": array of strings
    """

    json_response = model.generate_content([json_prompt])
    
    # The model might wrap the JSON in markdown, so we need to clean it.
    raw_json_text = json_response.text.strip().replace("```json", "").replace("```", "")
    
    try:
        product_json = json.loads(raw_json_text)
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the model's response.")
        product_json = {"error": "Failed to parse JSON", "raw_response": raw_json_text}

    log_agent_activity(
        agent_name="Structuring Agent",
        reasoning=structuring_reasoning,
        api_response=product_json,
    )
    
    return product_json


def push_to_shopify(product_json: dict):
    """
    (Placeholder) Pushes the structured product JSON to the Shopify API.

    This function represents the final step in the agent chain (Agent 3). It takes the
    machine-readable JSON and performs an action in an external system. For this
    hackathon, we are just printing the data, but in a real system, this is where
    the API call to Shopify would happen.

    Args:
        product_json: The dictionary of product data.
    """
    agent_name = "E-commerce Agent"
    reasoning = "Uploading the structured product data to the Shopify API."

    print(f"--- Running {agent_name} ---")
    print(reasoning)

    if "error" in product_json:
        print("Skipping Shopify push due to an error in the previous step.")
        log_agent_activity(agent_name, "Upload skipped due to error.", product_json)
        return

    # In a real implementation, you would use a library like 'requests'
    # to POST this JSON to the Shopify Admin API.
    #
    # Example:
    # shopify_url = "https://your-store.myshopify.com/admin/api/2023-10/products.json"
    # headers = {"X-Shopify-Access-Token": "your-api-key", "Content-Type": "application/json"}
    # response = requests.post(shopify_url, json={"product": product_json}, headers=headers)
    
    print("
Product JSON to be sent to Shopify:")
    print(json.dumps(product_json, indent=2))
    
    print("
(Simulating API call... Data not actually sent.)")

    # Log the successful (simulated) action.
    log_agent_activity(agent_name, reasoning, {"status": "simulated_success", "product_title": product_json.get("product_title")})


def main():
    """
    Main orchestration function.
    """
    print("--- Starting AI Agent Orchestrator ---")
    
    if not PROJECT_ID:
        print("
ERROR: GCP_PROJECT environment variable is not set.")
        print("Please set it to your Google Cloud Project ID.")
        print("Example: export GCP_PROJECT='your-gcp-project-id'")
        return

    # This is the initial input that kicks off the agent chain.
    product_idea = "a scented candle that smells like old books"
    
    # Run the first two agents to get structured data.
    structured_product_data = generate_product_json(product_idea)
    
    # Run the third agent to push the data to the e-commerce platform.
    push_to_shopify(structured_product_data)

    print("
--- Orchestration Complete ---")
    print(f"Audit logs have been written to {LOG_FILE}")


if __name__ == "__main__":
    main()
