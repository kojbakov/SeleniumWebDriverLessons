def get_all_href_from_ul(ul):
    item_links = []
    for elem in ul:
        for item in elem.find_elements_by_tag_name('a'):
            item_links.append(item.get_attribute('href'))
    return item_links
