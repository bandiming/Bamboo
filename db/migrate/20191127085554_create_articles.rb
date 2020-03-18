class CreateArticles < ActiveRecord::Migration[5.1]
  def change
    create_table :articles do |t|

      t.string :title
      t.string :uid
      t.string :aid
      t.string :oid
      t.string :section
      t.string :date

      t.timestamps
    end
  end
end
