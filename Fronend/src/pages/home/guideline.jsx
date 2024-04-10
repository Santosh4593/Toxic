import React, { useState, useEffect } from 'react';
import useAuth from "./useAuth";
import cokkie from 'js-cookie';
import { useNavigate } from 'react-router-dom';

// Mock data for random posts
const mockPosts = [
  { id: 1, username: 'parrot_king', imageUrl: 'data:image/jpeg;base64,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', caption: 'Look at my parrot!' },
  { id: 2, username: 'MI_Fan_Page', imageUrl: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQsXBrKickOyDJ-l-VYyLXjfQmf2FSxLKNkh7wiYjOSwPwojSGjm2MIFYC1Ng&s', caption: 'This team is an emotion' },
  { id: 3, username: 'Monkey D. Luffy', imageUrl: 'data:image/jpeg;base64,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', caption: 'Pirate King' },
  // Add more mock posts as needed
];

const Guidelines = () => {
  const navigate = useNavigate();
  const [posts, setPosts] = useState([]);
  const [caption, setCaption] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [toxicComment, setToxicComment] = useState(false);
  const [username, setUsername] = useState(""); 
  useAuth();

  useEffect(() => {
    // Fetch username from your authentication system or localStorage
    const storedUsername = localStorage.getItem('username');
    setUsername(storedUsername);
  
    // Simulate fetching random posts from a server
    // In a real app, you would fetch data from an API
    const fetchRandomPosts = () => {
      // Here you can implement logic to fetch random posts
      // For simplicity, let's just select a random subset of mock posts
      const randomSubset = mockPosts.sort(() => 0.5 - Math.random()).slice(0, 5);
      setPosts(randomSubset);
    };
  
    fetchRandomPosts();
  }, []);
  

  const handleScoreComment = async () => {
    try {
        setToxicComment(false); // Reset toxicComment state

        const token = cokkie.get('bearerToken');

        // Fetch initial count from backend
        const initialCountResponse = await fetch('http://127.0.0.1:8000/count', {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

        let initialCount = 0;
        if (initialCountResponse.ok) {
            const initialCountData = await initialCountResponse.json();
            initialCount = initialCountData.total_score;
            console.log("Initial Count:", initialCount);
        } else {
            console.error('Failed to fetch initial count:', initialCountResponse.statusText);
        }

        // Score the comment
        const response = await fetch('http://127.0.0.1:8000/score_comment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ comment_text: caption }),
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data);

            // Update count based on the values received from the backend
            const hasTrueValue = Object.values(data).some(value => value === true);
            console.log(hasTrueValue);

            // Fetch updated count from backend after scoring the comment
            const updatedCountResponse = await fetch('http://127.0.0.1:8000/count', {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            let updatedCount = 0;
            if (updatedCountResponse.ok) {
                const updatedCountData = await updatedCountResponse.json();
                updatedCount = updatedCountData.total_score;
                console.log("Updated Count:", updatedCount);

                // If the count is updated by 1, it means the comment is toxic
                if (updatedCount === initialCount + 1) {
                    setToxicComment(true);
                }

                // If the count remains the same and the caption is not toxic, update the post
                if (updatedCount === initialCount && !hasTrueValue) {
                    // Replace the image and caption of the first post with the uploaded image and caption
                    const updatedPosts = [...posts];
                    updatedPosts[0] = { ...updatedPosts[0], imageUrl: URL.createObjectURL(selectedImage), caption: caption };
                    setPosts(updatedPosts);
                }
            } else {
                console.error('Failed to fetch updated count:', updatedCountResponse.statusText);
            }

            if (updatedCount > 3) {
                // Display message
                alert('You have been blocked');
                // Redirect user after 5 seconds
                setTimeout(() => {
                    cokkie.remove('bearerToken');
                    navigate('/auth/login');
                }, 3000);
            }
        }
    } catch (error) {
        console.error('Error scoring comment:', error);
    }
};


  return (
    <div className="container mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold ml-10 mt-3">Social-Media</h1>
        <div className="flex space-x-4">
          <a href="#" className="text-lg font-semibold">Home</a>
          <a href="#" className="text-lg font-semibold">Search</a>
          <a href="#" className="text-lg font-semibold">Explore</a>
          <a href="#" className="text-lg font-semibold">Messages</a>
          <a href="#" className="text-lg font-semibold">Profile</a>
        </div>
      </div>
      <div className="flex justify-center">
        <div className="w-full max-w-lg">
          <div className="flex flex-col space-y-4">
            {/* Render random posts */}
            {posts.map(post => (
              <div key={post.id} className="border rounded p-4">
                <div className="flex items-center mb-2">
                  <div className="w-10 h-10 rounded-full bg-gray-300 mr-2"></div>
                  <span className="font-bold">{post.username}</span>
                </div>
                <img src={post.imageUrl} alt="Post" className="w-full mb-2" />
                <p>{post.caption}</p>
                <div className="flex justify-between mt-2">
                  <button className="text-blue-500">Like</button>
                  <button className="text-blue-500" onClick={() => handleScoreComment()}>Comment</button>
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="w-full max-w-lg ml-8">
          <div className="mt-8">
            <h2 className="text-2xl font-bold mb-4">Create a New Post</h2>
            <input type="file" onChange={(e) => setSelectedImage(e.target.files[0])} className="mb-4" />
            <textarea placeholder="Write a caption..." value={caption} onChange={(e) => setCaption(e.target.value)} className="w-full h-24 p-2 border rounded mb-4"></textarea>
            <button onClick={handleScoreComment} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Post</button>
            {toxicComment && <p className="text-red-500">This comment is toxic</p>}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Guidelines;
