import React, {useState, useEffect} from 'react';
import AlgoOutItem from './algooutitem';
import { findBestAlgo } from '../findBestAlgo';

function AlgoOut({ data }) {

  const [bestInd, setBestInd] = useState(null);

  useEffect(() => {
    if (data && data.result) {
      const result = findBestAlgo(data);
      setBestInd(result);
    }
  }, [data]);

  return (
    <div sx={{ paddingLeft: 0}}>
        <p>{data && Object.hasOwn(data, "isStat") ? "Ряд стационарный: " + (data.isStat ? "Да" : "Нет") : ""}</p>
        {bestInd !== null && data && Object.hasOwn(data, "isStat") ?
        <div>
          <div style={{display: "inline-flex"}}>
          <AlgoOutItem data={data.result[bestInd]} isBest={true} />
          </div>
          <br />
          <br />
          <h4>Все прогнозы</h4>
        </div> 
        : ""}
      {data && Object.hasOwn(data, "result") ? data.result.map((item, index) => (
        <div key={index} style={{display: "inline-flex"}}>
         <AlgoOutItem data={item} isBest={false}/>
        </div>
      )) : ""}
    </div>
  );
}

export default AlgoOut;