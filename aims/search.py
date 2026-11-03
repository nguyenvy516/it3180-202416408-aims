def search_by_category(items, category):
    '''Tìm kiếm danh sách DVD theo thể loại (không phân biệt hoa thường).'''
    if not category:
        return list(items)
    return [dvd for dvd in items if category.lower() in dvd.category.lower()]


def search_by_title(items, keyword):
    '''Tìm kiếm danh sách DVD theo tiêu đề.'''
    if not keyword:
        return list(items)
    return [dvd for dvd in items if keyword in dvd.title]
