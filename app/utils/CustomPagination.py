from django.core.paginator import InvalidPage
from rest_framework import pagination
from rest_framework.response import Response
from app.utils.ErrorJsonRender import PageNotFound


class CustomPagination(pagination.PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'prev': self.get_previous_link(),
                'next': self.get_next_link(),
                'count': self.page.paginator.per_page,
                'total_record': self.page.paginator.count,
            },
            'data': data
        })

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise PageNotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)
