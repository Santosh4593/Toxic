import React, { useState } from "react";
import { Link } from "react-router-dom";
import { ArrowUpRight } from "lucide-react";

const Signup = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [mobileNo, setMobileNo] = useState("");
  const [email, setEmail] = useState("");
  const [registrationStatus, setRegistrationStatus] = useState(null);

  const handleSignup = async (e) => {
    e.preventDefault();

    const userData = {
      username,
      password,
      mobileNo,
      email,
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      console.log(response);

      if (response.status === 200) {
        setRegistrationStatus("success");
      } else {
        setRegistrationStatus("error");
      }
    } catch (error) {
      console.error("An error occurred:", error);
      setRegistrationStatus("error");
    }
  };

  return (
    <div className="bg-cover bg-center flex items-center justify-center h-screen px-4 py-10 sm:px-6 sm:py-16 lg:px-8 lg:py-24">

       {/* <div className="absolute inset-0 overflow-y-auto" style={{backgroundImage: "url('emotion_bg.png')", backgroundSize: "cover"}}> */}
      <div className="xl:mx-auto xl:w-full xl:max-w-sm 2xl:max-w-md">
       <div className="mb-2 flex justify-center"></div>
        <h2 className="text-center text-2xl font-bold leading-tight text-black">
          Sign up to create account
        </h2>
        <p className="mt-2 text-center text-base text-gray-600">
          Already have an account?{" "}
          <Link
            to="/auth/login"
            title=""
            className="font-medium text-black transition-all duration-200 hover:underline"
          >
            Log In
          </Link>
        </p>
        <form onSubmit={handleSignup} className="mt-8">
          <div className="space-y-5">
            <div>
              <label
                htmlFor="username"
                className="text-base font-medium text-gray-900"
              >
                Username
              </label>
              <div className="mt-2">
                <input
                  className="flex h-10 w-full rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-gray-400 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50"
                  type="text"
                  placeholder="Username"
                  id="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>
            </div>
            <div>
              <label
                htmlFor="password"
                className="text-base font-medium text-gray-900"
              >
                Password
              </label>
              <div className="mt-2">
                <input
                  className="flex h-10 w-full rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-gray-400 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50"
                  type="password"
                  placeholder="Password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>
            <div>
              <label
                htmlFor="mobileNo"
                className="text-base font-medium text-gray-900"
              >
                Mobile Number
              </label>
              <div className="mt-2">
                <input
                  className="flex h-10 w-full rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-gray-400 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50"
                  type="text"
                  placeholder="Mobile Number"
                  id="mobileNo"
                  value={mobileNo}
                  onChange={(e) => setMobileNo(e.target.value)}
                />
              </div>
            </div>
            <div>
              <label
                htmlFor="email"
                className="text-base font-medium text-gray-900"
              >
                Email
              </label>
              <div className="mt-2">
                <input
                  className="flex h-10 w-full rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-gray-400 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50"
                  type="email"
                  placeholder="Email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
            </div>
            <div>
              <button
                type="submit"
                className="inline-flex w-full items-center justify-center rounded-md bg-cyan-500 px-3.5 py-2.5 font-semibold leading-7 text-black"
              >
                Create Account <ArrowUpRight className="ml-2" size={16} />
              </button>
            </div>
            {registrationStatus === "success" && (
              <p className="text-green-600 text-center">
                Registration successful!
              </p>
            )}
            {registrationStatus === "error" && (
              <p className="text-red-600 text-center">
                Registration failed. Please try again.
              </p>
            )}
          </div>
        </form>
      </div>
      
    </div>
  );
};

export default Signup;
