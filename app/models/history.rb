class History < ApplicationRecord
  def reply
    Reply.where(article_uid: self.article_uid, comment_no: self.comment_no).take(1).last
  end
end
