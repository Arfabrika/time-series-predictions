import React from 'react';

function SimpleOutput({ data }) {
  return (
    <div>
       <p>Ряд стационарный: { data && Object.hasOwn(data, "isStat") ? data.isStat : "Нет данных"}</p>
      {data && Object.hasOwn(data, "result") ? data.result.map((item, index) => (
        <div key={index}>
          <p>Pred: {item.pred.join(', ')}</p>
          <img src={`data:image/png;base64,${item.plot}`} alt={`Plot ${index + 1}`} />
          <p>Metrics:</p>
          <ul>
            {Object.entries(item.metrics).map(([key, value]) => (
              <li key={key}>{key}: {value}</li>
            ))}
          </ul>
        </div>
      )) : ""}
    </div>
  );
}

export default SimpleOutput;
