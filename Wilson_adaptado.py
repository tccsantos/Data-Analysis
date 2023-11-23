#!/usr/bin/python3
"""
-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*-**-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
*
*                                    "unshorten_url.py"
*                                    *****************
*                This code Un-Shorten URLs, group and sort by URL and domain
*                ***********************************************************
*
*        Developed by: Wilson  Ceron        e-mail: wilsonseron@gmail.com         Date: 15/08/2021
*
*
-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*-**-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
"""

import argparse
import codecs
import collections
import re
import sys
import pickle

from argparse import RawTextHelpFormatter
from csv import reader
from tld import get_tld
from unshortenit import UnshortenIt


def read_options():
    """
    Check for a valid input params
    Returns:
      Returns a dictonary with the inputs params
    """
    status = False

    parser = argparse.ArgumentParser(
        description="Basic Usage", formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "-i", "--input", help="CSV input File", required=True, default=""
    )
    parser.add_argument(
        "-o", "--output", help="Output file name", required=True, default=""
    )
    parser.add_argument(
        "-e", "--error", help="Number of attempts", required=False, default= 3
    )

    argument = parser.parse_args()

    if argument.input and argument.output:
        status = True

    if not status:
        print("Maybe you want to use -h for help")
        status = False

    return {"success": status, "input": argument.input, "output": argument.output, "error": argument.error}


def save_url_file(url, score, filename):
    """
    Create a csv file from the urls and ranking lists
    Arguments:
        url: a list
        score a list
        filename a string
    Returns:
        Save a csv file with the ranked urls
    """
    with codecs.open(filename + "_links.csv", "w",encoding="utf-8") as temp:
        temp.write('"URL";"Score"\n')
        for i, uri in enumerate(url):
            try:
                rank = int(score[i])
                temp.write(f'"{uri}";{rank}\n')
            except ValueError:
                temp.write(f'"{uri}";{score[i]}\n')
            except Exception as error:
                print(error)
    temp.close()
    # with codecs.open(filename + "_URL_suporte.csv", "w",encoding="utf-8") as temp:
    #     temp.write('"URL";"origem";"domain"\n')
    #     for i in range(len(origins)):
    #         temp.write(f'{origins[i][0][0]};{origins[i][0][1]};{origins[i][0][2]}\n')
    # temp.close


def save_dict(my_dict, filename):
    """
    Save a dictionary in csv format
    Arguments:
        my_dict: a dictionary
        filename a string
    Returns:
        Save a csv file with the the dictonary
    """
    with codecs.open(filename, "w",encoding="utf-8") as temp:
        temp.write('"Domain";"Score"\n')
        for key, value in my_dict.items():
            temp.write(f'"{str(key)}";{str(value)}\n')
    temp.close()

def update_dict(my_dict, key, value):
    """
    Update the value of a dictionary, if it doesn't find the key, adds the key with the value 1
    Arguments:
        my_dict: a dictionary
        key: key
        value: value
    Returns:
        return the updated dictonary
    """
    if key in my_dict:
        my_dict[key] = my_dict.get(key) + value
    else:
        my_dict[key] = value

    return my_dict


def clean_url(uri):
    """
    Remove unnecessary parameters from the URL, also normalizes different URL patterns
    from YouTube and Facebook
    Arguments:
        l: a string
    Returns:
        Returns a clean URL
    """
    uri = uri.split("?utm")[0]
    uri = uri.split("?at_")[0]
    uri = uri.split("?recruiter=")[0]
    uri = uri.split("?fbclid=")[0]
    uri = uri.split("/amp/?")[0]
    uri = uri.split("?__twitter")[0]
    uri = uri.split("?amp")[0]
    uri = uri.split("?ssm=TW_CC")[0]

    if re.search("https://youtu.be/", uri):
        uri = uri.replace("https://youtu.be/", "https://www.youtube.com/watch?v=")

    if re.search("youtube.com/watch?", uri):

        uri = uri.replace("https://m.youtube.com/", "https://youtube.com/")
        uri = uri.replace("https://www.youtube.com/", "https://youtube.com/")

        if re.search("&v=", uri):
            temp = uri.split("&v=")[1]
            uri = "https://www.youtube.com/watch?v=" + temp

        uri = uri.replace("app=desktop&", "")
        uri = uri.split("&")[0]
        uri = uri.split("?t=")[0]
        uri = uri.split("...")[0]
        uri = uri.split("?list=")[0]

    if re.search("https://www.facebook.com", uri):
        uri = uri.split("?substory_index=")[0]
        uri = uri.split("?sfnsn")[0]
        uri = uri.split("&sfnsn")[0]
        uri = uri.split("?ref")[0]
        uri = uri.split("&ref")[0]
        uri = uri.split("?set")[0]
        uri = uri.split("&sef")[0]
        uri = uri.split("?__")[0]
        uri = uri.split("?flite=")[0]
        uri = uri.split("?d=")[0]
        uri = uri.split("&scmts")[0]
        uri = uri.split("?comment_id=")[0]

    if re.search("https://www.facebook.com", uri):
        uri = uri.split("?substory_index=")[0]
        uri = uri.split("?sfnsn")[0]
        uri = uri.split("&sfnsn")[0]
        uri = uri.split("?ref")[0]
        uri = uri.split("&ref")[0]

    if uri.endswith("/amp/"):
        uri = uri.replace("/amp/", "/")

    return uri


def get_domain(url):
    """
    Extrat the domain of a URL
    Arguments:
        url: a string
    Returns:
        return the domain
    """
    try:
        res = get_tld(url, as_object=True)
        if res.subdomain and res.subdomain != "www":
            return {
                "sub": True,
                "subdomain": res.subdomain + "." + res.fld,
                "domain": res.fld,
            }
        return {"sub": False, "domain": res.fld}
    except Exception as error:
        print(error)

    return {}


def main():
    """
    	Main function
    """

    result = read_options()

    if not result.get("success"):
        sys.exit(1)

    inputfile = result.get("input")
    outputfile = result.get("output")
    attempts = result.get("error")

    with open(inputfile, "r",encoding="utf-8") as read_obj:
        csv_reader = reader(read_obj, delimiter=';')
        #next(csv_reader, None)
        data = list(csv_reader)

    url = []
    #origens = []
    score = []

    url_db = {}
    url_error = {}
    domains = {}

    unshortener = UnshortenIt(default_timeout=30, default_headers={})
    for row in data:
        try:
            uri = row[0]
        except IndexError:
            continue
        if not uri.startswith("http"):
            uri = "http://" + uri
        origin = uri
        if len(uri) <= 30:
            # Check if the URL exists in the database
            if uri in url_db:
                uri = url_db.get(uri)
                print("\tshorten_url:\t" + origin)
                print("\tunshorten_url:\t" + uri)
                print()
            #check if the url exists in the error database 
            elif uri in url_error:
                uri = url_error.get(uri)
                print("\tshorten_url:\t" + origin)
                print("\tunshorten_url:\t" + uri)
                print()
            else:
                try:
                    # Unshorten the url
                    long_url = unshortener.unshorten(uri)
                    print("\tshorten_url:\t" + uri)
                    uri = clean_url(long_url)

                    # Add the URL into the database
                    url_db[origin] = uri
                    print("\tunshorten_url:\t" + uri)
                    print()
                except ValueError:
                    print(uri)
                except Exception as error:
                    url_error[origin] = origin
                    print(error)
        else:
            uri = clean_url(uri)
            url_db[origin] = uri
            print(uri)

        print()

        # Get the domain of the URL and store in a dictionary
        uri = str(uri).lower()
        domain = get_domain(uri).get("domain")
        domains = update_dict(domains, domain, 1)
        url.append(uri)
        #origens.append((uri, origin, domain))

    #retry the url that were unshortened
    print('retrying errors\n')
    for i in range(attempts):
        print('attempt' + str(i + 1) + '\n')
        suporte = []
        for key, value in url_error.items():
            try:
                # Unshorten the url
                long_url = unshortener.unshorten(key)
                print("\tshorten_url:\t" + key)
                long_url = clean_url(long_url)

                # Add the URL into the database
                url_db[key] = long_url
                print("\tunshorten_url:\t" + long_url)
                print()
                suporte.append(key)
            except ValueError:
                print(key)
            except Exception as error:
                print(error)
            print()

        #exclude the links from the errors database
        for i in suporte:
            url_error.pop(i)

    #save the database dictionary
    with open('./Dados/urlDict.pickle', 'wb') as file:
        pickle.dump(url_db, file)
    
    # group and save the URLs
    my_dict = collections.Counter(url)
    values = my_dict.most_common()
    url, score = list(zip(*values))
    #sup = collections.Counter(origens)
    #ap = sup.most_common()
    save_url_file(url, score, outputfile)

    # sort and save the domains
    domains = dict(sorted(domains.items(), key=lambda x: x[1], reverse=True))
    save_dict(domains, outputfile + "_domains.csv")


if __name__ == "__main__":
    main()