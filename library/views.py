from django.views.generic import ListView, DetailView
from .models import Brand, Guitar, GuitarType


class GuitarListView(ListView):
    model = Guitar
    template_name = 'library/guitar_list.html'
    context_object_name = 'guitars'
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        brand_id = self.request.GET.get('brand')
        type_id = self.request.GET.get('type')

        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        if type_id:
            queryset = queryset.filter(guitar_type_id=type_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['types'] = GuitarType.objects.all()
        context['selected_brand'] = self.request.GET.get('brand', '')
        context['selected_type'] = self.request.GET.get('type', '')
        return context


class GuitarDetailView(DetailView):
    model = Guitar
    template_name = 'library/guitar_detail.html'
    context_object_name = 'guitar'
