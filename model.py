from pydantic import BaseModel, Field

class Data(BaseModel):
	company_name: str = Field(description='Name of the company')
	company_description: str = Field(description='One line company description from comp_task')
	company_retail: str = Field(description='"Yes" or "No" from retail_task')
	company_payments: str = Field(description='Payment method used from payment_task')
	company_lp_gl: str = Field(description='Global landing page of the company from landing_page_task')
	company_lp_eu: str = Field(description='European landing page of the company from landing_page_task')
	company_lp_uk: str = Field(description='UK landing page of the company from landing_page_task')
	company_hq_c: str = Field(description='Company Headquarter city from hq_task')
	company_hq_s: str = Field(description='Company Headquarter UN member state from hq_task')
	company_hq_gpc: str = Field(description='Company Headquarter Google Plus code from hq_task')