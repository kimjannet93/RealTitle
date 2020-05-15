from django.core.paginator import Paginator
import math

def get_pagination(data, page):

    # pagination
    paginator = Paginator(data, 10)
    posts = paginator.get_page(page)
    total_count = paginator.count

    page_range = 5
    current_block = math.ceil(int(page) / page_range)
    start_block = (current_block - 1) * page_range
    end_block = start_block + page_range
    p_range = paginator.page_range[start_block : end_block]

    return posts, total_count, p_range