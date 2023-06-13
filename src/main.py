import api_call as app

main_url = "https://api.fda.gov/drug/ndc.json?"
def get_patients_number_for_active_ingredient():
    active_ingredient = "LEVODOPA"
    url = f"{main_url}search=active_ingredients.name:{active_ingredient}&limit=1"
    patient_number = app.get_total_number(url)
    print(f"Total patients number : {patient_number}")



#get_patients_number_for_active_ingredient()

#get total no of records in FDA database
def get_total_row_number():
    row_number = app.get_total_number(main_url)
    print(f"Total row number : {row_number}")

def get_missing_package_ndc():
    url = f"{main_url}search=_missing_:packaging.package_ndc&limit=1"
    row_number = app.get_total_number(url)
    print(f"Total missing ndc packages : {row_number}")


def get_members():
    url = f"{main_url}search=_exists_:active_ingredients.name+AND+_exists_:packaging.package_ndc&limit=1"
    row_number = app.get_total_number(url)
    print(f"Total missing ndc packages : {row_number}")

def get_max_patient_for_ten_active_ingredients():
    output = app.get_max_patient_for_ten_active_ingredients(main_url)

def get_missing_drugs():
    output = app.get_max_patient_for_ten_active_ingredients(main_url)


get_patients_number_for_active_ingredient()
get_total_row_number()
get_missing_package_ndc()
get_members()
