Rails.application.routes.draw do
  get 'replies/show/:num' => 'replies#show'
  get 'articles/show/:num' => 'articles#show'
  get 'articles/index'

  get 'articles/target' => 'articles#target'

  get 'home/index'
  get 'chart/index'
  get 'chart/show/:num' => 'chart#show'

  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
