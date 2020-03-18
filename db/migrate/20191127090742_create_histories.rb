class CreateHistories < ActiveRecord::Migration[5.1]
  def change
    create_table :histories do |t|
      t.string :article_uid
      t.string :comment_no

      t.integer :likes
      t.integer :hates
      t.timestamps
    end
  end
end
