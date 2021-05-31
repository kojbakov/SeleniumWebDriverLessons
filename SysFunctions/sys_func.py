def get_all_href_from_ul(ul):
    item_links = []
    for elem in ul:
        for item in elem.find_elements_by_tag_name('a'):
            if item.get_attribute('href') not in item_links:
                item_links.append(item.get_attribute('href'))
    return item_links


def is_list_in_alphabet_order(l: list):
    copy_l = l.copy()
    copy_l.sort()
    return l == copy_l


