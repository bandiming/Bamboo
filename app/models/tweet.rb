class Tweet < ApplicationRecord
  def article
    Article.where(uid: article_uid).take(1)[0]
  end

  def reply
    Reply.where(article_uid: self.article_uid, comment_no: self.comment_no).first
  end

end
