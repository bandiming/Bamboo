class Article < ApplicationRecord
  def replies
    Reply.where(article_uid: self.uid)
  end

  def tweets
    Tweet.where(article_uid: self.uid)
  end

  def link
    "https://news.naver.com/main/ranking/read.nhn?rankingType=popular_day&oid=#{self.oid}&aid=#{self.aid}"
  end

  def histories
    History.where(article_uid: self.uid).last(10)
  end
end
