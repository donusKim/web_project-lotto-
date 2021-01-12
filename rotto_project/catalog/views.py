from django.shortcuts import render

# Create your views here.
from catalog.models import Round
from django.views import generic


class roundListView(generic.ListView):
    model = Round
    paginate_by = 15
    def get_queryset(self):
        return Round.objects.order_by('-round_num') # 내림차순

    def get_context_data(self, **kwargs):
        context = super(roundListView, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 15  # Display only 155 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context

class roundDetailView(generic.DetailView):
    model = Round


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_rounds = Round.objects.all().count()
    recent_round = Round.objects.filter(round_num=num_rounds)
    context = {
        'num_rounds': num_rounds,
        'winning_num': (recent_round[0].first_win_num, recent_round[0].second_win_num, recent_round[0].third_win_num,
                        recent_round[0].fourth_win_num, recent_round[0].fifth_win_num, recent_round[0].sixth_win_num),
        'bonus_num': recent_round[0].bonus_num,
        'first_win_money': recent_round[0].first_win_money,
        'win_money_each': int(recent_round[0].first_win_money/recent_round[0].num_first_winner),
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)