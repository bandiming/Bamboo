class AddSidToArticles < ActiveRecord::Migration[5.1]
  def change
    add_column :articles, :sid, :string, default: ""
    add_column :articles, :time, :string, default: ""
  end
end
