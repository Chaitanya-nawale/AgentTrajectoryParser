import argparse
from collections import Counter
import re
import requests

def trajectory_parser(url: str):
    dashboard_id =""
    dashboard_search = re.search(r"dashboard/([^/]+)", url)
    if dashboard_search:
        dashboard_id = dashboard_search.group(1)

    agent_run_id =""
    agent_run_search = re.search(r"agent_run/([^?]+)", url)
    if agent_run_search:
        agent_run_id = agent_run_search.group(1)

    transcript_id =""
    transcript_search = re.search(r"transcript_id=([^&]+)", url)
    if transcript_search:
        transcript_id = transcript_search.group(1)

    api_url = "https://api.docent.transluce.org/rest/"+ dashboard_id +"/agent_run_with_tree?agent_run_id=" + agent_run_id + "&full_tree=false"

    # TODO: Change the API key
    headers = {
        'Authorization': 'Bearer YOUR API KEY'
    }
    try:
        response = requests.get(api_url, headers=headers)
        transcripts = response.json()[0]['transcripts']
        for transcript in transcripts:
            if transcript['id'] == transcript_id or transcript_id == "":
                messages = transcript['messages']
                counts = Counter(msg['role'] for msg in messages)
                print(f"System messages:      {counts['system']}")
                print(f"User messages:        {counts['user']}")
                print(f"Assistant messages:  {counts['assistant']}")
                print(f"Tool messages:       {counts['tool']}")
                print("=======================")
                print(f"Total messages:      {sum(counts.values())}")
                return counts
    except (KeyError, IndexError, TypeError) as e:
        print(f"API Structure Error: Please check the url or data format provided by api. ({e})")
    except Exception as e:
        print(f"Unexpected Error: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    args = parser.parse_args()
    trajectory_parser(args.url)

if __name__ == '__main__':
    main()