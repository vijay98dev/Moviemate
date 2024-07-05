from rest_framework.pagination import PageNumberPagination,CursorPagination


class WatchListPagination(PageNumberPagination):
    page_size =10
    
    
    
class WathchListCPagination(CursorPagination):
    page_size =5
    ordering ='created'
    cursor_query_param='record'