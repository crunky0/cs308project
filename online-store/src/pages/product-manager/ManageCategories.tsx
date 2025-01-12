import React, { useState, useEffect } from "react";
import "./ManageCategories.css";

type Category = {
  categoryid: number;
  name: string; // Updated to reflect the 'name' column in the backend
};

const ManageCategories: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [newCategoryName, setNewCategoryName] = useState<string>("");
  const [error, setError] = useState<string>("");

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await fetch("http://localhost:8000/productmanagerpanel/categories");
      if (!response.ok) throw new Error("Failed to fetch categories");
      const data = await response.json();
      setCategories(data || []);
    } catch (err) {
      setError("Error fetching categories");
    }
  };

  const addCategory = async () => {
    if (!newCategoryName) {
      setError("Category name is required");
      return;
    }
    try {
      // Construct the URL with the 'name' query parameter
      const url = new URL("http://localhost:8000/productmanagerpanel/categories");
      url.searchParams.append("name", newCategoryName);
  
      const response = await fetch(url.toString(), {
        method: "POST",
      });
  
      if (!response.ok) throw new Error("Failed to add category");
  
      const newCategory = await response.json();
      setCategories([...categories, newCategory]);
      setNewCategoryName("");
    } catch (err) {
      setError("Error adding category");
    }
  };
  

  const deleteCategory = async (categoryid: number) => {
    if (!window.confirm("Are you sure you want to delete this category? This will delete all associated products.")) {
      return;
    }
    try {
      const response = await fetch(`http://localhost:8000/productmanagerpanel/categories/${categoryid}`, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error("Failed to delete category");
      setCategories(categories.filter((category) => category.categoryid !== categoryid));
    } catch (err) {
      setError("Error deleting category");
    }
  };

  return (
    <div className="manage-categories-container">
      <h1>Manage Categories</h1>
  
      {error && <p className="error">{error}</p>}
  
      <div className="add-category">
        <input
          type="text"
          value={newCategoryName}
          onChange={(e) => setNewCategoryName(e.target.value)}
          placeholder="Enter new category name"
        />
        <button onClick={addCategory}>Add Category</button>
      </div>
  
      <div className="category-list">
        {categories.length > 0 ? (
          categories.map((category) => (
            <div key={category.categoryid} className="category-item">
              <span>{category.name}</span>
              <button onClick={() => deleteCategory(category.categoryid)}>Delete</button>
            </div>
          ))
        ) : (
          <p>No categories available.</p>
        )}
      </div>
    </div>
  );  
};

export default ManageCategories;