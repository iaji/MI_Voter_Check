import requests
import json
from pprint import pprint
from serpapi import GoogleSearch
import re

first_name = 'Eleanor'
last_name = 'Guest'
birth_year = 1900
zip_code = 48239

zip_regex = r"\d{5}(?:[-\s]\d{4})? U"


def reg_scrape(year):
    collected_voters = {}
    search = GoogleSearch({
    "q": f"site:https://michiganvoters.info was born in {year}", 
    "location": "Detroit,Michigan",
    "api_key": "GET_A_KEY_FROM_HERE:https://serpapi.com/manage-api-key"
    })
    results = search.get_json()
    google_results = results['organic_results']
    for voter in google_results:
        snippet = voter['snippet']
        name_match = snippet.split(' was born in ')
        birth_year = name_match[1].split(' and')[0]
        full_name = name_match[0].split(', ')
        first_name = full_name[1]
        last_name = full_name[0]
        zip_match = re.search(zip_regex, snippet, re.MULTILINE)
        if zip_match != None:
            zipstr = str(zip_match.group(0))
            zipcode = zipstr.strip(' U')
            if ' ' in first_name:
                first_name = first_name.split(' ')[1]
            collected_voters[f"{last_name}_{first_name}"] = {'first': first_name, 'last': last_name, 'zipcode':zipcode, 'birth_year': birth_year}
    return(collected_voters)
    

def vote_check(first_name='Eleanor', last_name='Guest', birth_year=1900, zip_code=48239):

    for i in range(12):
        payload = {
            'FirstName': first_name,
            'LastName': last_name,
            'NameBirthMonth': i + 1,
            'NameBirthYear': birth_year,
            'ZipCode': zip_code,
            'Dln': '',
            'DlnBirthMonth': 0,
            'DlnBirthYear': '',
            'DpaID': 0,
            'Month': '',
            'VoterNotFound': 'false',
            'TransitionVoter': 'false'
        }

        response = requests.post('https://vote.michigan.gov/Voter/SearchByName', data=payload)

        if 'Yes, you are registered!' in response.text:
            out = 'found registration in month {}'.format(i + 1)
            return(out)
        else:
            return('Not Found')

if __name__ == "__main__":
    collected_voters = reg_scrape(1900)
    for person, info in collected_voters.items():
        checked_yo = vote_check(first_name=info['first'], last_name=info['last'], birth_year=info['birth_year'], zip_code=info['zipcode'])
        collected_voters[person]['vote_check'] = checked_yo
    pprint(collected_voters)