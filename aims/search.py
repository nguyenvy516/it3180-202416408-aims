def search_by_title(items, keyword):
    '''Tìm kiếm danh sách DVD theo tiêu đề.'''
    if not keyword:
        return list(items)
    return [dvd for dvd in items if keyword in dvd.title]
