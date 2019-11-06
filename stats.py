import json
import sys

def get_stats(data):
    links = set()
    subdomains = {}
    counters = {}
    status = {}
    total_space = 0
    total_links = 0
    
    for link in data:
        url, info = link.popitem()
        links.add(url)
        counters[info["type"]] = counters.get(info["type"], 0) + 1
        if info["type"] == "subdomain":
            subdomains[info["subdomain"]] = subdomains.get(info["subdomain"], 0) + 1
        elif info["type"] == "internal":
            total_space += info.get("length", 0)
            total_links += info.get("links", 0)
            status[info["status"]] = status.get(info["status"], 0) + 1
    return links, subdomains, counters, total_space, total_links, status

if __name__ == "__main__":
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        files = ["spburesult.json", ]
    
    for result_file in files:
        print(f"\nProcessing {result_file}...\n")
        with open(result_file) as file:
            data = json.load(file)
        links, subdomains, counters, total_space, total_links, statuses = get_stats(data)
        print(f"Total links: {total_links}")
        print(f"Unique links: {len(links)}\n")
        for link_type in counters:
            print(f"{link_type} links: {counters[link_type]}")
        print(f"\nTotal space: {total_space} bytes")
        if counters.get("internal", 0):
            avg_space = total_space/counters["internal"]
            avg_links = total_links/counters["internal"]
        else:
            avg_space = 0
            avg_links = 0
        print(f"Average space by page: {avg_space} bytes")
        print(f"Average links by page: {avg_links}")
        print(f"\nSubdomains: {len(subdomains)}")
        print("Popular subdomains:")
        sorted_subdomains = sorted(subdomains, key=lambda x: -subdomains[x])
        sorted_subdomains = sorted_subdomains[:min(5, len(sorted_subdomains))]
        for subdomain in sorted_subdomains:
            print(f"{subdomain}: {subdomains[subdomain]}")
        print("\nStatuses:")
        for status in statuses:
            print(f"{status}: {statuses[status]}")
