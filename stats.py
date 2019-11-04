import json

def get_stats(data):
    links = set()
    subdomains = {}
    counters = {}
    total_space = 0
    total_links = 0
    
    for link in data:
        url, info = link.popitem()
        links.add(url)
        counters[info["type"]] = counters.get(info["type"], 0) + 1
        if info["type"] == "subdomain":
            subdomains[info["subdomain"]] = subdomains.get(info["subdomain"], 0) + 1
        elif info["type"] == "internal":
            total_space += info["length"]
            total_links += info["links"]
    return links, subdomains, counters, total_space, total_links

if __name__ == "__main__":
    
    files = ["spburesult.json", "msuresult.json"]
    for result_file in files:
        with open(result_file) as file:
            data = json.load(file)
        links, subdomains, counters, total_space, total_links = get_stats(data)
        print(f"Total links: {len(result)}, {total_links}")
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
        print("Subdomains use:")
        for subdomain in subdomains:
            print(f"{subdomain}: {subdomains[subdomain]}")
