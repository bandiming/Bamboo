class RepliesController < ApplicationController
  def show
    @reply = Reply.find(params[:num].to_i)
    @data = [['date', 'likes', 'hates']]
    @reply.histories.each do |h|
      @data << [h.created_at.to_s, h.likes, h.hates]
    end
    @tweets = []
    tweets = Tweet.where(article_uid: @reply.article_uid)
    prev_uid = nil
    tweets.each do |tweet|
      if prev_uid != tweet.tweet_uid
        @tweets << tweet
        prev_uid = tweet.tweet_uid
      end
    end
  end
end
