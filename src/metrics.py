def append_to_output(str_to_append, filename):
    with open(filename, "w") as f:
        f.write(str_to_append)

def get_metrics(root):
    currentID = 0
    for child in root:
        if child.tag == "filename":
            filename = child.text
        elif child.tag == "class":
            for classChild in child:
                if classChild.tag == "className":
                    classname = classChild.text
                elif classChild.tag == "method":
                    nb_ifs = 0
                    nb_while = 0
                    nb_break = 0
                    nb_local_vars = 0
                    for methodChild in classChild:
                        if methodChild.tag == "methodName":
                            methodName = methodChild.text
                        elif methodChild.tag == "if":
                            nb_ifs += 1
                        elif methodChild.tag == "while":
                            nb_while += 1
                        elif methodChild.tag == "break":
                            nb_break += 1
                        elif methodChild.tag == "var":
                            nb_local_vars += 1
                    output_line = "{},{},{},{},{},{},{},{}".format(
                        currentID,
                        filename,
                        classname,
                        methodName,
                        nb_ifs,
                        nb_while,
                        nb_break,
                        nb_local_vars
                    )
                    currentID += 1
                    append_to_output(output_line, "metrics.txt")
