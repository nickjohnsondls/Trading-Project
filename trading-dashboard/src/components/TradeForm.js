import React, { useState } from 'react';

const TradeForm = ({ addTrade }) => {
  const [trade, setTrade] = useState({ date: '', asset: '', price: '', quantity: '' });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setTrade({ ...trade, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    addTrade(trade);
    setTrade({ date: '', asset: '', price: '', quantity: '' });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="date" value={trade.date} onChange={handleChange} placeholder="Date" required />
      <input name="asset" value={trade.asset} onChange={handleChange} placeholder="Asset" required />
      <input name="price" value={trade.price} onChange={handleChange} placeholder="Price" required />
      <input name="quantity" value={trade.quantity} onChange={handleChange} placeholder="Quantity" required />
      <button type="submit">Add Trade</button>
    </form>
  );
};

export default TradeForm;
