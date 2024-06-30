import React from 'react';
import TradeItem from './TradeItem';

const TradeList = ({ trades }) => {
  return (
    <div>
      {trades.map((trade, index) => (
        <TradeItem key={index} trade={trade} />
      ))}
    </div>
  );
};

export default TradeList;
