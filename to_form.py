import re

def main(filename):
    """
    get data from filename, then parse it
    """
    results = []
    space_re = r"[ \t]"
    with open(filename, "r") as f_descriptor:
        for data in f_descriptor.readlines():
            # replace spaces which used as borders
            # so, you should not write spaces into the not empty item!
            data = re.sub(space_re, " ", data).strip()
            if data.startswith("#"):
                continue

            # strip each item in data list expect space item
            # filter "", they may be exist at the end of list
            results.append("\t".join(filter(lambda x: x != "", data.split(" "))))

    return "\n".join(results)

print(main("credit.data"))
