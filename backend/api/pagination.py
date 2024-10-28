from rest_framework.pagination import PageNumberPagination


class UsersPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 6


class SubsPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = 6
    max_page_size = 2
