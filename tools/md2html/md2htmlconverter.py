import os
import requests
import re


class head_info:
    def __init__(self, head_type, head_id, head_content):
        self.head_type = head_type
        self.head_id = head_id
        self.head_content = head_content

    def __repr__(self):
        return f"{self.head_type}, {self.head_id}, {self.head_content}"


# input is a file, output is a path
def convert_file(input_file, output_path, header_template_url, header_template_active, navbar_template_url, navbar_template_active):
    input_file_info = input_file.split("\\")
    _file_name = input_file_info[len(input_file_info) - 1].split(".")
    input_file_name = _file_name[0]
    input_file_type = _file_name[1]
    input_file_path = input_file_info[len(input_file_info) - 2]

    print(f"converting file {input_file}\n to path {output_path}")
    out_content = ""
    out_content = head_converter(out_content, input_file_path, input_file_name)

    with open(input_file, encoding="utf8") as in_f:
        data = in_f.read()
        out_content = body_content_converter(out_content, data, header_template_url, header_template_active, navbar_template_url, navbar_template_active)
        out_content = end_file(out_content)

        # write content to new html
        with open(os.path.join(output_path, f"{input_file_name}.html"), "wt", encoding="utf8") as out_f:
            out_f.write(out_content)
            print("done")


def head_converter(out_content, input_file_path, out_file_name):
    title = os.path.join(input_file_path, out_file_name)
    s_f = requests.get("https://zheminggu.github.io/myheadtemplate.html")
    script_data = s_f.text
    script_data = "<!doctype html> \n" + "<html lang=\"en\"> \n" + "<head> \n" + script_data

    script_data = script_data.replace("TemplateTitle", f"{title}")

    out_content += script_data + "</head> \n\n"
    # print(head)
    return out_content


def end_file(out_content):
    out_content += "</html>\n"
    return out_content


def start_body():
    return "<body>\n"


def body_header():
    header = "\t<!--header--> \n"
    header += "\t<div id =\"header\"></div>\n\n"
    return header


def body_content_start():
    return "\t<!--content-->\n\t<div class=\"container-fluid\">\n\t\t<div class=\"row\">\n"


def body_nav_bar():
    return "\t\t\t<!--navbar-->\n\t\t\t<div id = \"navbar\"></div>\n\n"


def body_content(input_data):
    spy_headers = []
    spy_map = {}
    content = ""
    indent = 3
    content = add_string(content, indent, "<div class=\"col-8 markdown-body\">")
    indent += 1
    lines = input_data.split("\n")
    is_code_line = False
    is_table_line = False
    is_table_header = True
    for line in lines:
        if "#code" in line:
            is_code_line = True
            indent += 1
            content = add_string(content, indent, f"<pre class=\"line-left\" style=\"background-color: rgb(239, 240, 241); border-radius: 3px; padding-left: 12px; padding-right: 8px;\">")
            indent += 1
            content = add_string(content, indent, f"<code>")
            continue

        if "code#" in line:
            is_code_line = False
            content = add_string(content, indent, f"</code>")
            indent -= 1
            content = add_string(content, indent, f"</pre>")
            indent -= 1
            continue

        if is_code_line:
            line = line.replace("<", "&lt")
            line = line.replace(">", "&gt")

            # comment
            if "// " in line:
                comment_position = line.find("// ")
                line = line[0:comment_position] + f"<span style=\"color: green;\">{line[comment_position:]}</span>"
                # content = add_string(content, 0, f"<span style=\"color: green;\">{line}</span>")
                # continue
            if line.find("# ") == 0:
                content = add_string(content, 0, f"<span style=\"color: green;\">{line}</span>")
                continue
            
            # define function and other keywords
            line = line.replace("False ", "<span style=\"color: blue;\">False</span> ")
            line = line.replace("True ", "<span style=\"color: blue;\">True</span> ")
            line = line.replace("def ", "<span style=\"color: blue;\">def</span> ")
            line = line.replace("self.", "<span style=\"color: blue;\">self</span>.")
            # for cpp
            line = line.replace("void ", "<span style=\"color: blue;\">void</span> ")
            line = line.replace("float ", "<span style=\"color: blue;\">float</span> ")
            line = line.replace("int ", "<span style=\"color: blue;\">int</span> ")
            line = line.replace("double ", "<span style=\"color: blue;\">double</span> ")
            line = line.replace("char ", "<span style=\"color: blue;\">char</span> ")
            line = line.replace("string ", "<span style=\"color: blue;\">string</span> ")
            line = line.replace("bool ", "<span style=\"color: blue;\">bool</span> ")
            line = line.replace("float*", "<span style=\"color: blue;\">float</span>*")
            line = line.replace("int*", "<span style=\"color: blue;\">int</span>*")
            line = line.replace("double*", "<span style=\"color: blue;\">double</span>*")
            line = line.replace("char*", "<span style=\"color: blue;\">char</span>*")
            line = line.replace("string*", "<span style=\"color: blue;\">string</span>*")
            line = line.replace("bool*", "<span style=\"color: blue;\">bool</span>*")

            line = line.replace("class ", "<span style=\"color: blue;\">class</span> ")
            line = line.replace("const ", "<span style=\"color: blue;\">const</span> ")
            line = line.replace("static ", "<span style=\"color: blue;\">static</span> ")
            line = line.replace("inline ", "<span style=\"color: blue;\">inline</span> ")
            line = line.replace("false ", "<span style=\"color: blue;\">false</span> ")
            line = line.replace("true ", "<span style=\"color: blue;\">true</span> ")
            line = line.replace("this.", "<span style=\"color: blue;\">this</span>.")

            # flow control key words
            line = line.replace("in ", "<span style=\"color: rgb(228, 27, 218);\">in</span> ")
            line = line.replace("with ", "<span style=\"color: rgb(228, 27, 218);\">with</span> ")
            line = line.replace("as ", "<span style=\"color: rgb(228, 27, 218);\">as</span> ")
            line = line.replace("from ", "<span style=\"color: rgb(228, 27, 218);\">from</span> ")
            line = line.replace("import ", "<span style=\"color: rgb(228, 27, 218);\">import</span> ")
            line = line.replace("for(", "<span style=\"color: rgb(228, 27, 218);\">for</span>(")
            line = line.replace("if(", "<span style=\"color: rgb(228, 27, 218);\">if</span>(")
            line = line.replace("while(", "<span style=\"color: rgb(228, 27, 218);\">while</span>(")
            line = line.replace("else(", "<span style=\"color: rgb(228, 27, 218);\">else</span>(")
            line = line.replace("else ", "<span style=\"color: rgb(228, 27, 218);\">else</span> ")
            line = line.replace("if:", "<span style=\"color: rgb(228, 27, 218);\">if</span>:")
            line = line.replace("while:", "<span style=\"color: rgb(228, 27, 218);\">while</span>:")
            line = line.replace("elif:", "<span style=\"color: rgb(228, 27, 218);\">elif</span>:")
            line = line.replace("else:", "<span style=\"color: rgb(228, 27, 218);\">else</span>:")
            line = line.replace("include ", "<span style=\"color: rgb(228, 27, 218);\">include</span> ")
            line = line.replace("return ", "<span style=\"color: rgb(228, 27, 218);\">return</span> ")
            line = line.replace("continue ", "<span style=\"color: rgb(228, 27, 218);\">continue</span> ")
            line = line.replace("break ", "<span style=\"color: rgb(228, 27, 218);\">break</span> ")

            # standard library
            line = line.replace("std::", "<span style=\"color: rgb(228, 27, 218);\">std</span>::")
            line = line.replace("ios::", "<span style=\"color: rgb(228, 27, 218);\">ios</span>::")

            content = add_string(content, 0, f"{line}")
            continue

        if "#table" in line: 
            is_table_line = True
            is_table_header = True
            indent += 1
            content = add_string(content, indent, f"<table class=\"table table-bordered table-hover\">")
            indent += 1
            continue

        if "table#" in line:
            is_table_line = False
            indent -= 1
            content = add_string(content, indent, f"</tbody>")
            indent -= 1
            content = add_string(content, indent, f"</table>")
            indent -= 1
            continue

        if is_table_line:
            if is_table_header:
                content = add_string(content, indent, f"<thead style=\"background-color: #6c757d; color: azure;\">")
                indent += 1
                content = add_string(content, indent, f"<tr>")
                indent += 1
                table_header = line.split("|")
                for h in table_header:
                    temp_h = h.rstrip()
                    temp_h = temp_h.lstrip()
                    temp_h = temp_h.capitalize()
                    content = add_string(content, indent, f"<th scope=\"col\">{temp_h}</th>")
                indent -= 1
                content = add_string(content, indent, f"</tr>")
                indent -= 1
                content = add_string(content, indent, f"</thead>")
                content = add_string(content, indent, f"<tbody>")
                indent += 1 
                is_table_header = False
                continue
            else:
                content = add_string(content, indent, f"<tr>")
                indent += 1
                table_body = line.split("|")
                for i, b in enumerate(table_body):
                    temp_b = b.rstrip()
                    temp_b = temp_b.lstrip()
                    if i == 0:
                        content = add_string(content, indent, f"<th scope =\"row\">{temp_b}</th>")
                    else:
                        content = add_string(content, indent, f"<td>{temp_b}</td>")
                indent -= 1
                content = add_string(content, indent, f"</tr>")
                continue
            
        if line == "":
            continue
       
        # check images
        while "#img " in line:
            indent += 1
            # print(f"previous line \n {line}")
            img_index = line.find("#img ")
            img_index_end = len(line)
            for i in range(img_index + len("#img "), len(line)):
                if line[i] == ')':
                    img_index_end = i + 1
                    break
  
            img_info = line[img_index + len("#img "): img_index_end]
            new_img_info = img_info.split(",")
            img_name = new_img_info[0]
            img_name = img_name.lstrip()
            img_name = img_name.rstrip()
            img_name = img_name.replace("(", "")
            img_url = new_img_info[-1]
            img_url = img_url.lstrip()
            img_url = img_url.rstrip()
            img_url = img_url.replace(")", "")
            # print(f"image name is {img_name}")
            # print(f"image url is {img_url}")
            new_img_line = "\n" + add_indent(f"<figure class=\"figure\">\n", indent)
            indent += 1
            new_img_line = new_img_line + add_indent(f"<img src=\"{img_url}\" alt=\"{img_name}\">\n", indent)
            new_img_line = new_img_line + add_indent(f"<figcaption class=\"figure-caption text-center\">{img_name}.</figcaption>\n", indent)
            indent -= 1
            new_img_line = new_img_line + add_indent(f"</figure>", indent)
            line = line[0: img_index] + new_img_line + line[img_index_end: len(line)]
            indent -= 1

        while "#video " in line:
            indent += 1
            video_index = line.find("#video ")
            video_index_end = len(line)
            for i in range(video_index + len("#video "), len(line)):
                if line[i] == ')':
                    video_index_end = i + 1
                    break
            video_info = line[video_index + len("#video "): video_index_end]
            new_video_info = video_info.split(",")
            video_aspect = new_video_info[0]
            video_aspect = video_aspect.lstrip()
            video_aspect = video_aspect.rstrip()
            video_aspect = video_aspect.replace("(", "")
            video_aspect = video_aspect.split(":")

            video_url = new_video_info[-1]
            video_url = video_url.lstrip()
            video_url = video_url.rstrip()
            video_url = video_url.replace(")", "")

            new_video_line = "\n" + add_indent(f"<div class=\"embed-responsive embed-responsive-{video_aspect[0]}by{video_aspect[-1]}\">\n", indent)
            indent += 1
            new_video_line = new_video_line + add_indent(f"<iframe class=\"embed-responsive-item\" src=\"{video_url}\" allowfullscreen></iframe>\n", indent)
            indent -= 1
            new_video_line = new_video_line + add_indent(f"</div>", indent)
            line = line[0: video_index] + new_video_line + line[video_index_end: len(line)]
            indent -= 1

        while "#url " in line:
            indent += 1
            url_index = line.find("#url ")
            url_index_end = len(line)
            for i in range(url_index + len("#url "), len(line)):
                if line[i] == ')':
                    url_index_end = i + 1
                    break
            url_info = line[url_index + len("#url "): url_index_end]
            new_url_info = url_info.split(",")
            url_text = new_url_info[0]
            url_text = url_text.lstrip()
            url_text = url_text.rstrip()
            url_text = url_text.replace("(", "")

            url_url = new_url_info[-1]
            url_url = url_url.lstrip()
            url_url = url_url.rstrip()
            url_url = url_url.replace(")", "")

            new_url_line = f"<a href = \"{url_url}\">{url_text}</a>"
            line = line[0: url_index] + new_url_line + line[url_index_end: len(line)]
            indent -= 1

        #check title
        if "#### " in line:
            line_content = line.replace("#### ", "")
            content = add_string(content, indent, f"<h4>{line_content}</h4>")
        elif "### " in line:
            line_content = line.replace("### ", "")
            line_content = line_content.rstrip()
            id_number = line_content.replace(" ", "_")
            id_number = re.sub('[^0-9a-zA-Z_]+', '', id_number)
            
            if id_number in spy_map.keys():
                spy_map[id_number] += 1
                id_number = id_number + str(spy_map[id_number])
            else:
                spy_map[id_number] = 0
            content = add_string(content, indent, f"<h3 id=\"{id_number}\">{line_content}</h3>")
            spy_headers.append(head_info("h3", id_number, line_content))
        elif "## " in line:
            line_content = line.replace("## ", "")
            line_content = line_content.rstrip()
            id_number = line_content.replace(" ", "_")
            id_number = re.sub('[^0-9a-zA-Z_]+', '', id_number)
            if id_number in spy_map.keys():
                spy_map[id_number] += 1
                id_number = id_number + str(spy_map[id_number])
            else:
                spy_map[id_number] = 0
            content = add_string(content, indent, f"<h2 id=\"{id_number}\">{line_content}</h2>")
            spy_headers.append(head_info("h2", id_number, line_content))
        elif "# " in line:
            line_content = line.replace("# ", "")
            content = add_string(content, indent, f"<h1>{line_content}</h1>")
        else:
            indent += 1
            line_content = line
            content = add_string(content, indent, f"<p>{line_content}</p>")
            indent -= 1

    content = add_string(content, indent, "</div>\n")
    return content, spy_headers


def body_spy(spy_headers):
    # for e in spy_headers:
    #     print(e)
    indent = 3
    spy = ""
    spy = add_string(spy, indent, "<div class=\"col\">")
    indent += 1
    spy = add_string(spy, indent, "<div class=\"line-left blog-content-nav\">")
    indent += 1
    spy = add_string(spy, indent, "<nav class=\"navbar navbar-light bg-light\">")
    indent += 1
    spy = add_string(spy, indent, "<nav class=\"nav nav-pills flex-column\">")
    indent += 1
    i = 0
    while i < len(spy_headers):
        if spy_headers[i].head_type == "h2":
            spy_href = spy_headers[i].head_id
            spy_head_content = spy_headers[i].head_content
            spy_head_content = spy_head_content.replace("_", " ")
            spy = add_string(spy, indent, f"<a class=\"smoothscroll\" href=\"#{spy_href}\">{spy_head_content}</a>")
            i += 1
        elif spy_headers[i].head_type == "h3":
            spy = add_string(spy, indent, "<nav class=\"nav nav-pills flex-column\">")
            indent += 1
            while spy_headers[i].head_type == "h3":
                spy_href = spy_headers[i].head_id
                spy_head_content = spy_headers[i].head_content
                spy_head_content = spy_head_content.replace("_", " ")
                spy = add_string(spy, indent, f"<a class=\" ml-3 my-1 smoothscroll\" href=\"#{spy_href}\">{spy_head_content}</a>")
                i += 1
                if i == len(spy_headers):
                    break

            spy = add_string(spy, indent, "</nav>")
            indent -= 1

    spy = add_string(spy, indent, "</nav>")
    indent -= 1
    spy = add_string(spy, indent, "</nav>")
    indent -= 1
    spy = add_string(spy, indent, "</div>")
    indent -= 1
    spy = add_string(spy, indent, "</div>\n")
    return spy


def body_content_end():
    return "\t\t</div>\n\t</div>\n\n"


def scroll_up():
    return "<!--scroll up-->\n<div class=\"scrollup\">\n<a href=\"#\"><i class=\"fa fa-chevron-up\"></i></a>\n</div>"


def body_script(header_template_url, header_template_active, navbar_template_url, navbar_template_active):
    active = "steam"
    s_f = requests.get("https://zheminggu.github.io/myscripttemplete.html")
    script_data = s_f.text
    script_data = script_data.replace("https://zheminggu.github.io/myheadertemplete.html", f"{header_template_url}")
    script_data = script_data.replace("#HeaderBlogs", f"#{header_template_active}")
    script_data = script_data.replace("https://zheminggu.github.io/myblognavbartemplete.html", f"{navbar_template_url}")
    script_data = script_data.replace("#steam", f"#{navbar_template_active}")
    script_data += "\n"
    return script_data


def end_body():
    return "</body>\n"


def body_content_converter(out_content, input_data, header_template_url, header_template_active, navbar_template_url, navbar_template_active):
    print("converting body content")

    content, spy_headers = body_content(input_data)
    spy = body_spy(spy_headers)

    body = start_body()
    body += body_header()
    body += body_content_start()
    body += body_nav_bar()
    body += content
    body += spy
    body += body_content_end()
    body += scroll_up()
    body += body_script(header_template_url, header_template_active, navbar_template_url, navbar_template_active)
    body += end_body()

    out_content += body
    return out_content


def add_string(add_string, indent_number, add_content):
    add_content = add_indent(add_content, indent_number)
    add_string += add_content + "\n"
    return add_string


def add_indent(add_string, indent_number):
    temp_string = ""
    for i in range(indent_number):
        temp_string += "\t"
    add_string = temp_string + add_string
    return add_string


if __name__ == "__main__":

    print("main md to html converter")
    # pass
    test_input_path = "C:\\Users\\zhemi\\Desktop\\DontStarveModBasics.md"
    test_output_path = "C:\\Users\\zhemi\\Desktop"

    convert_file(test_input_path, test_output_path)
