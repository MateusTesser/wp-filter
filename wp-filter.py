import requests
import json
import html
import argparse
import os
#Developed to Wordfence Research

parser = argparse.ArgumentParser(
                    prog='WP-Filter',
                    description='Search plugins to Wordfence Bug Bounty Program',
                    epilog='Wordfence Bug Bounty Program')
parser.add_argument('-j', '--json',action='store',required=False)
args = parser.parse_args()

base_url = "https://api.wordpress.org/plugins/info/1.2/?action=query_plugins&request[page]={}&request[per_page]=100"

page = 1
plugins_data={}

while True:
    response = requests.get(base_url.format(page))
    if response.status_code == 200:
        plugin_inf = json.loads(response.text)['info']
        total_results = plugin_inf['results']
        print("Info: Total de resultados ->", total_results)
        plugins = json.loads(response.text)['plugins']
        for plugin in plugins:
            if int(plugin["downloaded"]) > 50000:
                print("Name:", html.unescape(plugin["name"]), "-> Downloads:", plugin["downloaded"], "-> Download link:", plugin["download_link"])
                plugin_data = {
                    "downloads": plugin["downloaded"],
                    "link": plugin["download_link"]
                }
                plugins_data[html.unescape(plugin["name"])] = plugin_data
                if args.json:
                    with open(args.json, 'w') as json_file:
                        json.dump(plugins_data, json_file, indent=4)
        if total_results <= page * 100:
            break
        else:
            page += 1
    else:
        print("Finished!")
        break