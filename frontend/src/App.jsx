import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [users, setUsers] = useState([]); // Base state is a clean array

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/users`);
      
      // Defensively check if the response data is actually an array before saving it
      if (Array.isArray(response.data)) {
        setUsers(response.data);
      } else {
        console.error("API returned data that is not an array:", response.data);
        setUsers([]); // Fallback to an empty array to prevent map crashes
      }
    } catch (error) {
      console.error("Failed to fetch users from API:", error);
      setUsers([]); // Fallback to safe array on network errors
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_BASE_URL}/login`, {
        username,
        password
      });
      setUsername('');
      setPassword('');
      fetchUsers();
    } catch (error) {
      console.error("Login/Signup error:", error);
    }
  };

  return (
    <div className="container">
      <h1>User Manager</h1>
      
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          placeholder="Username" 
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input 
          type="password" 
          placeholder="Password" 
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Create User</button>
      </form>

      <div className="user-list">
        <h2>Users</h2>
        {/* Guard rails: check if users exists and has length before calling map */}
        <ul>
          {Array.isArray(users) && users.length > 0 ? (
            users.map((user) => (
              <li key={user.id}>{user.username}</li>
            ))
          ) : (
            <li>No users found or backend loading...</li>
          )}
        </ul>
      </div>
    </div>
  );
}

export default App;