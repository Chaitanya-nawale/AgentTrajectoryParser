from bs4 import BeautifulSoup
import requests
import re
import json
from collections import Counter
from metrics_computation import trajectory_parser

def get_source_leaderboard(data_list, agent_mode='mini-v2'):
    bash_only = next((lb for lb in data_list if lb.get('name') == 'bash-only'), None)

    if not bash_only:
        return None

    if agent_mode == 'mini-v2':
        source_leaderboard = bash_only.copy()
        source_leaderboard['results'] = [
            r for r in bash_only.get('results', [])
            if re.match(r'^2\.', str(r.get('mini-swe-agent_version', '')))
        ]
        return source_leaderboard

    return bash_only

def get_top_five_models_with_docent():
    swebench_url = "https://www.swebench.com/"
    swebench_page = requests.get(swebench_url)
    swebench_soup = BeautifulSoup(swebench_page.content, "html.parser")

    content = swebench_soup.find(id="leaderboard-data")
    if content:
        content = content.get_text().strip()
        data = json.loads(content)
    else:
        data = {}

    top_five_sources = get_source_leaderboard(data)['results'][0:5]

    name_docent_dictionary = {}
    print(f"{'NAME':<35} {'RESOLVED':<10} {'AVG CALLS':<12} {'TOTAL COST'}")
    print("—" * 70)
    for source in top_five_sources:
        cost = f"${source['cost']:>7.2f}"
        res = f"{source['resolved']:>6.1f}%"
        name_docent_dictionary[source['name']] = source['trajs_docent']
        print(f"{source['name']:<35} {res:<12} {source['instance_calls']:<12} {cost}")

    print(f"{'NAME':<35} {'AVG_SUCCESS_COST':<17} {'AVG_FAIL_COST':<14} {'AVG_SUCCESS_CALLS':<18} {'AVG_FAIL_CALLS':<15} {'SUCCESS_COUNT':<14} {'FAIL_COUNT'}")
    print("—" * 129)
    for source in top_five_sources:
        api_fails_count = 0
        api_success_count = 0
        failure_count = 0
        success_count = 0
        failure_cost = 0
        success_cost = 0
        per_instance_details = source.get('per_instance_details', {})
        for per_instance_detail in per_instance_details.values():
            if per_instance_detail.get('resolved'):
                api_success_count += per_instance_detail.get('api_calls')
                success_cost += per_instance_detail.get('cost')
                success_count += 1
            else:
                api_fails_count += per_instance_detail.get('api_calls')
                failure_cost += per_instance_detail.get('cost')
                failure_count += 1
        if success_count > 0:
            avg_success_cost = f"${success_cost/success_count:>3.4f}"
            avg_fail_cost = f"${failure_cost/failure_count:>3.4f}"
            avg_success_calls = f"{api_success_count/success_count:>7.2f}"
            avg_fail_calls = f"{api_fails_count/failure_count:>7.2f}"
            print(f"{source['name']:<35} {avg_success_cost:<17} {avg_fail_cost:<14} {avg_success_calls:<18} {avg_fail_calls:<15} {success_count:<14} {failure_count}")

    return name_docent_dictionary

if __name__ == '__main__':

    name_docent_dict = get_top_five_models_with_docent()
    name_count_dict = {}
    for name_docent in name_docent_dict.items():
        docent_url = name_docent[1]

        agent_docent_id = ""
        agent_docent_search = re.search(r"dashboard/([^?]+)", docent_url)
        if agent_docent_search:
            agent_docent_id = agent_docent_search.group(1)

        api_url = "https://api.docent.transluce.org/rest/" + agent_docent_id + "/agent_run_ids/query"
        headers = {
            'Authorization': 'Bearer YOUR API KEY',
            'Content-Type': 'application/json'
        }
        payload = { "sort_direction": "asc", "limit": 500, "offset": 0 }
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        agent_run_ids = response.json()
        total_counts = Counter()
        for agent_run_id in agent_run_ids:
            agent_run_url = "https://docent.transluce.org/dashboard/"+ agent_docent_id + "/agent_run/" + agent_run_id
            counts = trajectory_parser(agent_run_url)
            total_counts.update(counts)
        name_count_dict[name_docent[0]] = total_counts

    print(f"{'NAME':<35} {'SYSTEM MSGS':<12} {'USER MSGS':<10} {'ASSISTANT MSGS':<15} {'TOOL MSGS'}")
    print("—" * 85)
    for name_count in name_count_dict.items():
        system = name_count[1]['system']
        tool = name_count[1]['tool']
        assistant = name_count[1]['assistant']
        user = name_count[1]['user']
        print(f"{name_count[0]:<35} {system:<12} {user:<10} {assistant:<15} {tool}")
