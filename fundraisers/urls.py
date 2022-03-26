from django.urls import path

from fundraisers import views


urlpatterns = [
    path('', views.FundraiserListView.as_view(), name='fundraiser_list'),
    path('my-list/', views.FundraiserMyListView.as_view(), name='fundraiser_my_list'),
    path('category/<slug:slug>/', views.FundraiserCategoryListView.as_view(), name='fundraiser_category_list'),
    path('<int:pk>/', views.FundraiserDetailView.as_view(), name='fundraiser_detail'),
    path('create/', views.FundraiserCreateView.as_view(), name='fundraiser_create'),
    path('update/<int:pk>/', views.FundraiserUpdateView.as_view(), name='fundraiser_update'),
    path('<int:fundraiser_id>/comment/add/', views.CommentAddView.as_view(), name='fundraiser_comment_add'),
    path('<int:fundraiser_id>/vote/', views.FundraiserVoteView.as_view(), name='fundraiser_vote'),
]
