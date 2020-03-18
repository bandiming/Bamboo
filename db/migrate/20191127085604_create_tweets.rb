class CreateTweets < ActiveRecord::Migration[5.1]
  def change
    create_table :tweets do |t|
      t.string :comment_no
      t.string :article_uid

      t.string :tweet_uid
      t.string :username
      t.text :content
      t.string :date

      t.timestamps
    end
  end
end
