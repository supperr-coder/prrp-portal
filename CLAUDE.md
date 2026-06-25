Create a web-application that:
1. Allows user to key in entity_id/UEN 
2. Extracts required data from csv file (or other types of file) in Maestro S3 bucket
	- present the required income/property/tenancy listing data in tabular form (downloadable as csv or excel)
3. Includes a GST reg calculator that breaks down revenu by calendar yer basis
4. Allows user to upload required documents (formsg, contracts, sales/purchase listings, invoices)
	- generates draft reports based on the uploaded documents using llm

Use streamlit for starters.
No need for backend, hardcode the logic to enerate step 2, 3, and 4 results for now.
