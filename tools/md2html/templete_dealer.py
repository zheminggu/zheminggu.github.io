
import requests


def get_ids(website_url=""):
    ids = []
    template_file = requests.get(website_url)
    template_data = template_file.text
    # print(template_data)
    while "id=" in template_data:
        position = template_data.find("id=")
        start_position = position + 4
        end_position = 0
        for i in range(start_position, len(template_data)):
            if template_data[i] == "\"":
                end_position = i
                break
        current_id = template_data[start_position: end_position]
        ids.append(current_id)
        template_data = template_data[end_position: len(template_data)]
    return ids


if __name__ == "__main__":
    ids = get_ids("https://zheminggu.github.io/myheadertemplete.html")
    print(ids)