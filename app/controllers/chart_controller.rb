class ChartController < ApplicationController
  def index
    @tweet = Tweet.find(820)
    @tweets = Tweet.where(comment_no: @tweet.comment_no, article_uid: @tweet.article_uid)

    @data = [['date', 'likes', 'hates']]
    @tweet.reply.histories.each do |h|
      @data << [h.created_at.to_s, h.likes, h.hates]
    end
  end

  def show
    @tweet = Tweet.find(params[:num].to_i)
    @tweets = Tweet.where(comment_no: @tweet.comment_no, article_uid: @tweet.article_uid)
    @likes = [['date', 'likes']]
    @hates = [['date', 'hates']]
    @tweet.reply.histories.each do |h|
      @likes << [h.created_at.to_s, h.likes]
      @hates << [h.created_at.to_s, h.hates]
    end
  end

end
