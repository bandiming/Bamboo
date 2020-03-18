class CreateReplies < ActiveRecord::Migration[5.1]
  def change
    create_table :replies do |t|
      t.string :article_uid
      t.string :comment_no
      t.text :content
      t.string :nickname
      t.string :date

      t.timestamps
    end
  end
end
