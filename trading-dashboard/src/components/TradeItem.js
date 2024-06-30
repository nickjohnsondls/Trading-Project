import React from 'react';

const TradeItem = ({ trade }) => {
  return (
    <div>
      <p>Date: {trade.date}</p>
      <p>Asset: {trade.asset}</p>
      <p>Price: {trade.price}</p>
      <p>Quantity: {trade.quantity}</p>
    </div>
  );
};

export default TradeItem;
