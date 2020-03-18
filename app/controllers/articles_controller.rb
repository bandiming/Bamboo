class ArticlesController < ApplicationController

  def index
    # sections = {'politics': 100, 'economy': 101, 'society': 102}
    # @user = Users.select(:username).limit(2).offset(1)
    @politics = Article.where(section: "100").last(10)
    @economies = Article.where(section: "101").last(10)
    @societies = Article.where(section: "102").last(10)
  end

  def show
    # @article = Article.find(params[:num].to_s)
    @article = Article.where(uid: params[:num].to_s).last
  end

  def target
    @articles = []
    tweets = Tweet.last(500).reverse
    uids = []
    tweets.each do |tweet|
      article = tweet.article
      if article == nil
        next
      end
      unless uids.include? article.uid
        @articles << article
        uids << article.uid
        if uids.count > 15
          break
        end
      end
    end

  end
end
