class Reply < ApplicationRecord
  def histories
    History.where(article_uid: self.article_uid, comment_no: self.comment_no)
  end

  def tweets
    Tweet.where(article_uid: self.article_uid, comment_no: self.comment_no)
  end

  def article
    Article.where(uid: self.article_uid).take(1)
  end

  def likes
    self.histories.each do |h|
      puts "likes: #{h.likes} hates: #{h.hates} when #{h.created_at.to_s}"
    end
    nil
  end
end
