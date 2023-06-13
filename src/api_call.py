import requests
import pandas as pd
import json
import os

from requests import RequestException


def get_total_number(url):
    patient_number = 0
    try:
        #val = "LEVODOPA"

        response = requests.get(url)
        #print(type(response.json()))
        resp_dict = response.json()
        #print(response.json())

        for key in resp_dict:
            if key == "meta":
                patient_number = (resp_dict[key]["results"]["total"])
    except RequestException as err:
        print(f"Error to get patients number : {err}")

    return patient_number


def read_csv_file():
    abs_dir_path = os.path.abspath(os.curdir)
    fpath = os.path.join(abs_dir_path, '/patient_files')
    f_path = f"{abs_dir_path}\patient_files\patients.csv"
    print(f_path)
    df = pd.read_csv(f_path)
    #df1 = df.groupby('patient_id', group_keys=False).apply(lambda x: x.loc[x.ndc_number.idxmax()])
    # Using list() Function
    col_list = list(df["ndc_number"])
   # print(col_list)
    return df

def convert_package_ndc_to_ndc_number(pckg_ndc):
    ndc_pckg = ""

    spilt_val = pckg_ndc.split('-')

    if len(spilt_val[0]) < 5:
        ndc_pckg = f"0{spilt_val[0]}{spilt_val[1]}{spilt_val[2]}"
    elif len(spilt_val[1]) < 4:
        ndc_pckg = f"{spilt_val[0]}0{spilt_val[1]}{spilt_val[2]}"
    elif len(spilt_val[2]) < 2:
        ndc_pckg = f"{spilt_val[0]}{spilt_val[1]}0{spilt_val[2]}"

    return ndc_pckg


def get_max_patient():
    active_ingredients_dict = dict()
    main_url = "https://api.fda.gov/drug/ndc.json?"
    url = f"{main_url}search=_exists_:active_ingredients.name+AND+_exists_:packaging.package_ndc&limit=1"
    row_number = get_total_number(url)
    url = f"{main_url}search=_exists_:active_ingredients.name+AND+_exists_:packaging.package_ndc&limit=1000"
    response = requests.get(url)
    #print(response.json())
    resp_dict = response.json()
    res1 = (resp_dict["results"])
    #df = pd.DataFrame(resp_dict["results"])
    #print(df)
    #print(df[['active_ingredients', 'packaging']])
    #print(type(res1))
    for dict1 in res1:
        val = dict1["active_ingredients"]
        name_val = None
        ndc_number = list()
        for i in val:
            name_val = i["name"]
            print(name_val)
            break
        #print(dict1["active_ingredients"]['name'])

        val2 = dict1["packaging"]
        for y in val2:
            pckg_ndc = y["package_ndc"]
            print((pckg_ndc))
            ndc_number_val = convert_package_ndc_to_ndc_number(pckg_ndc)

            print((ndc_number))

            if name_val in active_ingredients_dict:
                ndc_number_exist_list = active_ingredients_dict[name_val]
                ndc_number_exist_list.append(ndc_number_val)
            else:
                ndc_number.append(ndc_number_val)
                active_ingredients_dict[name_val] = ndc_number
            break

    print(active_ingredients_dict)
    df = read_csv_file()
    for key in active_ingredients_dict:
        list2 = active_ingredients_dict[key]
        print(list2)
        output = df['ndc_number'].isin(list2)
        print(output)

def get_missing_drugs():
    main_url = "https://api.fda.gov/drug/ndc.json?"
    url = f"{main_url}search=_missing_:active_ingredients.name+AND+_exists_:packaging.package_ndc&limit=1000"
    response = requests.get(url)
    #print(response.json())
    data = response.json()
    entries = data["results"]
    df = pd.json_normalize(entries)
    print(df["packaging"].head())















    #print(fpath)

#convert_package_ndc_to_ndc_number()
#read_csv_file()
#get_max_patient()
#get_max_patient()
get_missing_drugs()