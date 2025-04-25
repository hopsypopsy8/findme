import argparse
import requests
from bs4 import BeautifulSoup

def main():
    parser = argparse.ArgumentParser(description ='Provided User Info')

    parser.add_argument('-fn', '--firstname')
    parser.add_argument('-ln', '--lastname')
    parser.add_argument('-mn', '--middlename')
    parser.add_argument('-e', '--email')
    parser.add_argument('-p', '--phonenumber')

    args = parser.parse_args()
    
    data = [args.firstname, args.lastname, args.middlename, args.email, args.phonenumber]
    print(data)
    internet_dork(data)

def internet_dork(data: list):

    # SETUP QUERY

    query_parts = [item for item in data if item]  # fix if no mid last or fistname yk
    query = " ".join(query_parts)

    print(f"\nSearching DuckDuckGo for: {query}")

    # SEARCH QUERY

    platforms = ['instagram', 'facebook', 'twitter', 'snapchat'] #add if you want diff platforms

    for platform in platforms:

        print(f"\nSearching {platform.capitalize()} for: {query}")

        url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)} site:{platform}.com"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch search results for {platform}.")
                continue
            
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.select(".result__a")  

            # seperate file for results
            platform_results = []
            if results:
                for i, link in enumerate(results[:10], 1):  # do only top 10 results
                    platform_results.append(f"{i}. {link.text.strip()}\n{link.get('href')}\n")
                
                # save to txt file
                with open(f"{platform}_search_results.txt", "w", encoding="utf-8") as file:
                    file.write(f"### {platform.capitalize()} Results ###\n\n")
                    for result in platform_results:
                        file.write(result + "\n")
                
                print(f"Results for {platform.capitalize()} saved to '{platform}_search_results.txt'.")
            
            else:
                with open(f"{platform}_search_results.txt", "w", encoding="utf-8") as file:
                    file.write(f"### {platform.capitalize()} Results ###\n\n")
                    file.write("No results found.\n")
                print(f"No results found for {platform}.")
        
        except Exception as e:
            print(f"Error searching {platform}: {e}")

if __name__ == "__main__":
    main()