import React, { useState, useEffect } from "react";
import TradeForm from "./components/TradeForm";
import TradeList from "./components/TradeList";
import "./App.css";

const App = () => {
  const [trades, setTrades] = useState(() => {
    const savedTrades = localStorage.getItem("trades");
    return savedTrades ? JSON.parse(savedTrades) : [];
  });

  useEffect(() => {
    localStorage.setItem("trades", JSON.stringify(trades));
  }, [trades]);

  const addTrade = (trade) => {
    setTrades([...trades, trade]);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Trading Dashboard</h1>
      </header>
      <main>
        <TradeForm addTrade={addTrade} />
        <TradeList trades={trades} />
      </main>
    </div>
  );
};

export default App;
