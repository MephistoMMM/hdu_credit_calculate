#!/usr/bin/env python3
"""
This cli program is used to calculate credit, then compare it with requirement

Author: Mephis Pheies
Email: mephistommm@gmail.com
"""

import re

from collections import namedtuple

COURSECATEGORY = namedtuple("COURSECATEGORY", 
                            ("name", "basis_key", "requirement", "valid_value", "items"))

def get_datas(filename):
    """
    get data from filename, then parse it
    """
    result = []
    space_re = r"\b +\b"
    with open(filename, "r") as f_descriptor:
        for data in f_descriptor.readlines():
            # replace spaces which used as borders
            # so, you should not write spaces into the not empty item!
            data = re.sub(space_re, "\t", data).strip()
            if len(data) == 0 or data.startswith("#"):
                continue

            # strip each item in data list expect space item
            # filter "", they may be exist at the end of list
            data = list(
                filter(lambda x: x != "",
                       map(lambda x: x.strip() if x != " " else x,
                           data.split("\t"))))
            # data should contain 13 items, the items of left end will not lack
            # so we should add additional space items to right end
            if len(data) < 13:
                spaces = [" " for i in range(13)]
                spaces[:len(data)] = data[:]
                data = spaces

            assert len(data) == 13
            result.append({
                "course_code": data[2],
                "course_name": data[3],
                "course_property": data[4],
                "course_from": data[10],
                "credit": float(data[6])})

    return result

def get_course_categories(filename):
    """
    get the categories of courses, hence we could classify the courses
    """
    result = []
    current_category = None
    type_line_re = r"Type\b.*"
    with open(filename, "r") as f_descriptor:
        for data in f_descriptor.readlines():
            data = data.strip()
            if len(data) == 0 or data.startswith("#"):
                continue

            if re.match(type_line_re, data, re.I):
                if current_category is not None:
                    result.append(current_category)

                type_list = list(
                    filter(lambda x: x != "",
                           map(lambda x: x.strip(), 
                               data.split(" "))))

                if len(type_list) < 4:
                    raise ValueError("invild line:\n\t'{}'".format(data))

                current_category = COURSECATEGORY(
                    type_list[1], type_list[2], float(type_list[3]), [], [])
                continue

            current_category.valid_value.append(data)

    result.append(current_category)
    return result

def check_data_in_category(data, category):
    """
    check data in category
    use re.match compare all regExg in category.valid_value with data[category.basis_key]
    """
    key = category.basis_key
    result = False
    for valid_re in category.valid_value:
        if re.match(valid_re, data[key], re.I):
            result = True
            break

    return result

def sum_of_credit(datas):
    """
    calculate the sum of credit of datas, 
    datas could be list or iterables
    """
    return sum(map(lambda x: x["credit"], datas))

def sum_of_require(categories):
    """
    calculate the sum of requirement of categories
    """
    return sum(map(lambda x: x.requirement, categories))


def main():
    """
    * get and parse data
    """
    course_categories = get_course_categories("courses_categorise.datas")
    student_credit_datas = get_datas("credit.data")

    failed_to_classify_datas = []

    for data in student_credit_datas:
        for category in course_categories:
            if check_data_in_category(data, category):
                category.items.append(data)
                break
        else:
            failed_to_classify_datas.append(data)

    if len(failed_to_classify_datas) != 0:
        print("Some datas are failed to classify:")
        for data in failed_to_classify_datas:
            print(("{course_code} {course_name}"
                   " {course_property} {course_from} {credit}").format(**data))

    is_in_course_requirement = lambda x: re.match("课外", x.name) is None
    is_in_course = lambda x: re.match("课外", x["course_property"]) is None
    total_requirement = sum_of_require(course_categories)
    total = sum_of_credit(student_credit_datas)
    in_course_requirement = sum_of_require(
        filter(is_in_course_requirement, course_categories))
    in_course = sum_of_credit(
        filter(is_in_course, student_credit_datas))
    out_course_requirement = sum_of_require(
        filter(lambda x: not is_in_course_requirement(x), course_categories))
    out_course = sum_of_credit(
        filter(lambda x: not is_in_course(x), student_credit_datas))

    print("total: {}/{}    in_course: {}/{}   out_course: {}/{}".format(
        total, total_requirement,
        in_course, in_course_requirement,
        out_course, out_course_requirement))
    print("")

    for category in course_categories:
        category_total = sum_of_credit(category.items)
        print("Type name:{}     {}/{}".format(
            category.name, category_total, category.requirement))
        for data in category.items:
            print(("\t{course_code} {course_name}"
                   " {course_property} {course_from} {credit}").format(**data))
        print("")

try:
    main()
except ValueError as err:
    print(err)
