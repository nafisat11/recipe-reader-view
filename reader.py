from bs4 import BeautifulSoup
from bs4.element import NavigableString
import requests
import json
import argparse
import nltk
import re
from pprint import pprint


def get_parsed_html():
    parser = argparse.ArgumentParser()
    parser.add_argument("--website")
    args = parser.parse_args()
    data = requests.get(args.website)
    soup = BeautifulSoup(data.text, 'html.parser')
    return soup


# TODO: Convert html entities to ascii using BeautifulSoup
def html_entity_converter(text):
    text = BeautifulSoup(text, features="html.parser")
    return text


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


def parse_microdata(field):
    '''Search for tags with itemprop=""'''
    pass


def parse_RDFa(field):
    '''Search for tags with property=""'''
    pass


def dfs(tree, ingreds, instr):
    units = ["cup", "lb", "oz", "tsp", "tbsp", "ml"]
    food_items = ["salt", "pepper", "butter", "oil", "eggs"]
    for node in tree.children:
        if isinstance(node, NavigableString):
            s = str(node).strip()
            if len(s) < 100:
                if any(x in s for x in food_items) or any(x in s for x in units):
                    ingreds[node.parent] = ""

            elif len(s) < 400:
                words = ["mix", "heat", "sprinkle",
                         "bake", "cut", "serve", "whisk"]
                if s[0].isdigit():
                    new_s = re.sub(r"^[\d-]*", "", s).lstrip()
                    if any(x in new_s for x in words):
                        instr[node.parent] = ""
                elif any(x in s for x in words):
                    instr[node.parent] = ""
            continue
         # Compute LCA node and get class attr for tag
        dfs(node, ingreds, instr)


def lca():
    pass


def parse_arbitrary_html():
    '''html that doesn't follow recipe schema'''
    pass


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

    def description(self):
        pass

    def cooktime(self):
        data = get_parsed_html().find_all(type="application/ld+json")
        for item in data:
            extracted_ingredients = jsonldschema(
                json.loads(item.string), "recipeIngredient")
            if not extracted_ingredients:
                pass

    def servings(self):
        pass

    def ingredients(self):
        data = get_parsed_html().find_all(type="application/ld+json")
        for item in data:
            extracted_ingredients = jsonldschema(
                json.loads(item.string), "recipeIngredient")
            if not extracted_ingredients:
                pass
        # Further processing
        processed = []
        for ingredient in extracted_ingredients[0]:
            ingredient = html_entity_converter(ingredient)
            processed.append(ingredient)
        return processed

    def instructions(self):  # conditionals for nested dicts
        data = get_parsed_html().find_all(type="application/ld+json")
        for item in data:
            extracted_instructions = jsonldschema(
                json.loads(item.string), "recipeInstructions")
            if not extracted_instructions:
                pass
        # Further processing
        processed = []
        for instruction in extracted_instructions[0]:
            if isinstance(instruction, dict):
                for k, v in instruction.items():
                    if k == "text":
                        processed.append(v)
            else:
                processed.append(instruction)
        return processed


def main():
    ingreds = {}
    instr = {}
    dfs(get_parsed_html().body, ingreds, instr)
    print(ingreds)
    print(instr)


if __name__ == "__main__":
    main()
