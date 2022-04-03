from django.urls import path

from fundraisers.views import Fundraiser, Comment, Transaction


urlpatterns = [
    path('', Fundraiser.List.as_view(), name='fundraiser_list'),
    path('my-list/', Fundraiser.MyList.as_view(), name='fundraiser_my_list'),
    path('category/<slug:slug>/', Fundraiser.CategoryList.as_view(), name='fundraiser_category_list'),
    path('<int:pk>/', Fundraiser.Detail.as_view(), name='fundraiser_detail'),
    path('create/', Fundraiser.Create.as_view(), name='fundraiser_create'),
    path('update/<int:pk>/', Fundraiser.Update.as_view(), name='fundraiser_update'),
    path('<int:fundraiser_id>/comment/add/', Comment.Add.as_view(), name='fundraiser_comment_add'),
    path('<int:fundraiser_id>/vote/', Fundraiser.Vote.as_view(), name='fundraiser_vote'),
    path('<int:fundraiser_id>/transaction/add/', Transaction.Add.as_view(), name='fundraiser_transaction_add'),
]
