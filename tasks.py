from crewai import Task
from tools import search_tool, scrape_tool
from agents import comp_res, reviewer
from model import Data
# Research task
comp_task = Task(
  description=(
       """Using the search tool provided, you identify the company name and its core activities from the following url: {url}, and then summarizes this information in a single sentence.
       You then evaluate the content against the provided definition of a retailer—one that sells directly to consumers, 
       manages the sale process, handles post-purchase issues, and acts as the merchant of record—while excluding specific non-retail categories.
       Using search or scrape tools provided, you visits the product page provided via the following URL: {url} and examines the payment processing method. 
       You then categorizes the payment method(s) as either “List price,” “Bid/auction,” or “Subscription” (or a combination thereof) and nothing else, no extra text.
       Leveraging the tools provided you search the regional landing pages of the company using context of company details and the following url: {url}. 
       You have to identify three key URLs: the most-global landing page, the most-visited landing page within Europe (covering the EEA, GB, and CH), 
       and the most-visited landing page specific to the UK market.
       You search or scrape and extract the city where the headquarters is located, identify the corresponding UN member state, 
       and retrieve the Google Plus Code associated with the headquarter location, all based on the provided company details and url: {url}.
       Finally, you collect all the data and save it in a json file."""
  ),
  expected_output="""Strictly a json file with the following keys:
    Company_URL: The URL provided as input
    Company_Name: From comp_task
    Company_Description: One line company description from comp_task
    Company_Retail: 'Yes' or 'No' from retail_task
    Company_Payments: Payment method used should be only either “List price,” “Bid/auction,” or “Subscription” (or a combination thereof).
    Company_LP_GL: Global landing page of the company if not available put 'NA'
    Company_LP_EU: European landing page of the company if not available put 'NA'
    Company_LP_UK: UK landing page of the company if not available put 'NA'
    Company_HQ_C: Company Headquarter city from hq_task if not available put 'NA'
    Company_HQ_s: Company Headquarter UN member state from hq_task if not available put 'NA'
    Company_HQ_GPC: Only the Google Plus code of the company headquarters if not available put 'NA'""",
  tools=[search_tool, scrape_tool],
  agent=comp_res,
  output_json=Data,
  output_file='output/data.json'
)

texit = Task(
    description="The only action required is to exit.",
    agent=reviewer,
    expected_output="Exit.",
)