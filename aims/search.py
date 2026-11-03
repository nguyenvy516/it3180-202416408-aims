def search_by_title(items, keyword):
    '''Tìm kiếm danh sách DVD theo tiêu đề (không phân biệt hoa thường).'''
    if not keyword:
        return list(items)
    return [dvd for dvd in items if keyword.lower() in dvd.title.lower()]
