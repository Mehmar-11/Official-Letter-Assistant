import { useState } from "react";
import LandingPage from "./pages/LandingPage";
import Dashboard from "./pages/Dashboard";

export default function App() {
  const [screen, setScreen] = useState("landing");

  return (
    <>
      {screen === "landing" ? (
        <LandingPage onStart={() => setScreen("dashboard")} />
      ) : (
        <Dashboard onBack={() => setScreen("landing")} />
      )}
    </>
  );
}