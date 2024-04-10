import { BrowserRouter, Route, Routes } from "react-router-dom";
import Landing from "./pages/home";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Signup from "./pages/auth/Signup";
import Login from "./pages/auth/Login";
import Profile from "./pages/my_profile/index";
// import Board from "./pages/leaderboard/index";
// import Sad from "./pages/home/sad";
// import Angry from "./pages/home/angry";
// import Happy from "./pages/home/happy";
// import Neutral from "./pages/home/neutral";
// import ResultHappy from "./pages/home/result_happy";
// import ResultDepressed from "./pages/home/result_depressed";
// import ResultAnxiety from "./pages/home/result_anxiety";
// import ResultStress from "./pages/home/result_stressed";
// import Parameters from "./pages/home/parameters";

import useAuth from "./pages/home/useAuth";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route exact path="/" element={<Landing />} />
        <Route path="/auth/signup" element={<Signup />} />
        <Route path="/auth/login" element={<Login />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/useAuth" element={<useAuth />} />
        {/* <Route path="/leaderboard" element={<Board />} /> */}        

        {/* <Route path="/sad" element={<Sad />} />
        <Route path="/angry" element={<Angry />} />
        <Route path="/happy" element={<Happy />} />
        <Route path="/neutral" element={<Neutral />} />
        <Route path="/result_happy/:calculatedSum" element={<ResultHappy />} />
        <Route path="/result_depressed/:calculatedSum" element={<ResultDepressed />} />
        <Route path="/result_anxiety/:calculatedSum" element={<ResultAnxiety />} />
        <Route path="/result_stressed/:calculatedSum" element={<ResultStress />} /> */}
        {/* <Route path="/parameters" element={<Parameters />} /> */}
        {/* <Route path="/result/:emo" element={<ResultPage />} /> */}
        
        <Route path="*" element={<h1>404 Not Found</h1>} />
      </Routes>
      <Footer />
    </BrowserRouter>
  );
}

export default App;
