from bs4 import BeautifulSoup
import requests
import json
import argparse
# import re


def get_parsed_html():
    parser = argparse.ArgumentParser()
    parser.add_argument("--website")
    args = parser.parse_args()
    data = requests.get(args.website)
    soup = BeautifulSoup(data.text, 'html.parser')
    return soup


# TODO: Convert html entities to ascii using BeautifulSoup
def jsonldschema(search_dict, field):
    found_field = []
    for k, v in search_dict.items():
        if k == field:
            found_field.append(v)

        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    results = jsonldschema(item, field)
                    found_field.extend(results)
                else:
                    break

        elif isinstance(v, dict):
            more_results = jsonldschema(v, field)
            for result in more_results:
                found_field.append(result)
    return found_field


class Recipe:
    def __init__(self):
        self.parsed_html = get_parsed_html()

    def title(self):
        title = self.parsed_html.find(
            "meta", property="og:title", content=True)
        if title:
            return title["content"]
        else:
            return self.parsed_html.title.text

    def cooktime(self):
        pass

    def servings(self):
        pass

    def ingredients(self):
        print(self.parsed_html.findChild())


def main():
    data = json.loads(get_parsed_html().find(
        "script", type="application/ld+json").string)
    # with open("recipe.json", "w") as json_file:
    #     json.dump(data, json_file, indent=4, separators=(",", ": "))
    print(jsonldschema(data, "recipeInstructions"))


if __name__ == "__main__":
    main()
