import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
// login screens
import Login from "./components/Login/Login";
import Signup from "./components/Login/Signup";
import ForgotPassword from "./components/Login/ForgotPassword";
import ResetPassword from "./components/Login/ResetPassword"

// dashboard screens
import Home from "./components/dashboard/Home"
import AdminReports from "./components/dashboard/AdminReports";
import UserManagement from "./components/dashboard/UserManagement";



function App() {
  return (
    <Router>
      <Routes>
        { /* login screens */ }
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />

        { /* dashboard screens */ }
        <Route path="/home" element={<Home />} />
        <Route path="/admin-reports" element={<AdminReports />} />
        <Route path="/user-management" element={<UserManagement />} />
      </Routes>
    </Router>
  );
}

export default App;
